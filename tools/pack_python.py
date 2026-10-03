"""Usage: python tools/pack_python.py ORIGINAL_DIRECTORY OUTPUT_DIRECTORY."""
import base64
import hashlib
from pathlib import Path
import sys
import zlib
from protect_python import protect

source_dir, output_dir = map(Path, sys.argv[1:])
output_dir.mkdir(parents=True, exist_ok=True)
for filename in ('bootstrap.py', 'genpaths.py'):
    source = protect((source_dir / filename).read_text()).encode()
    compile(source, filename, 'exec')
    key = hashlib.sha256(source).digest()
    data = zlib.compress(source, 9)
    payload = base64.b85encode(bytes(v ^ key[i % len(key)] for i, v in enumerate(data))).decode()
    (output_dir / filename).write_text(
        '# Super JinX Panel — Copyright (c) 2026 Super JinX. See LICENSE.\n'
        'import base64 as _b,zlib as _z\n_p=' + repr(payload) + '\n_k=' + repr(key.hex()) +
        '\n_d=_b.b85decode(_p);_k=bytes.fromhex(_k)\n'
        'exec(compile(_z.decompress(bytes(v^_k[i%len(_k)] for i,v in enumerate(_d))),__file__,"exec"),globals())\n')
