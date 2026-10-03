"""Rename Python bindings and mask strings before packing or native compilation."""
import ast
import hashlib
import python_minifier


def protect(source, preserve=(), mask=True):
    tree = ast.parse(source)
    helpers = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id.endswith('_PY') and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            helpers.append(node.targets[0].id)
            node.value = ast.Constant(protect(node.value.value))
    if mask:
        class Strings(ast.NodeTransformer):
            def visit_Assign(self, node):
                if any(isinstance(t, ast.Name) and t.id in helpers for t in node.targets):
                    return node
                return self.generic_visit(node)

            def visit_JoinedStr(self, node):
                # Literal segments must remain literals in the f-string AST.
                # Python before 3.12 cannot unparse bytes containing backslashes
                # inside formatted expressions. Keep the full f-string intact.
                return node

            def visit_Constant(self, node):
                if not isinstance(node.value, str) or len(node.value) < 3 or node.value == '__main__':
                    return node
                raw = node.value.encode()
                key = hashlib.sha256(raw).digest()[0] or 173
                encoded = bytes(v ^ key for v in raw)
                return ast.copy_location(ast.Call(func=ast.Name(id='_jx_decode', ctx=ast.Load()), args=[ast.Constant(encoded), ast.Constant(key)], keywords=[]), node)
        # Strip docstrings before their literal nodes become expressions.
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body.pop(0)
                if not node.body: node.body.append(ast.Pass())
        tree = Strings().visit(tree)
        decoder = ast.parse('from functools import lru_cache as _jx_cache\n@_jx_cache(maxsize=None)\ndef _jx_decode(data, key):\n    return bytes(v ^ key for v in data).decode()\n')
        tree.body[0:0] = decoder.body
    return python_minifier.minify(ast.unparse(ast.fix_missing_locations(tree)), rename_globals=True, rename_locals=True, preserve_globals=list(preserve)+helpers, remove_literal_statements=True, hoist_literals=False, remove_annotations=False, convert_posargs_to_args=False)
