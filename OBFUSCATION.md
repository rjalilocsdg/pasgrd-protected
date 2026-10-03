# Obfuscated distribution

Super JinX branding, credits, and LICENSE remain applicable.
Deploy using the Dockerfile and existing Railway settings.

## Protection applied

Python inputs have local and global bindings renamed before packing. Ordinary
string literals of three or more characters are masked and decoded through a
cached helper. F-string segments, import paths, external method names, and protocol
contracts retain required meanings. Four embedded database scripts receive the
same transformations. Packing remains reversible and does not provide encryption.

A separate Docker stage uses Cython 3.1.8 to compile six native modules, including
those database helpers. The final image receives compiled modules and minimal
launchers. Generated C, decoded source, packed inputs, and compiler tools stay in
the build stage. Linux debugging symbols are stripped. Rebuild for each Python
version and architecture. Strings, native control flow, and runtime behavior can
still be examined.

Shell scripts in the checkout contain compressed payloads. The Docker builder
converts them into native launchers containing masked Bash payloads. The final
image receives those executables rather than Python shell decoders. The launchers
preserve Bash arguments and exit status. Bash receives readable commands at runtime;
this does not prevent a person controlling the container from extracting them.

The QR encoder and subscription application share one private scope. Their
shared QR implementation is no longer exposed on window. Dashboard and subscription
code use javascript-obfuscator 4.1.1 with renamed bindings, masked string arrays,
control flow flattening, split strings, numeric expressions, and injected code.
No source maps are emitted. Object properties used by browser and server APIs
remain compatible. The output remains recognizable as obfuscated JavaScript.

The generated JavaScript is larger and more expensive to initialize. HTML, CSS,
user-visible branding, and server-rendered subscription data remain readable.
Upstream PasarGuard and Xray binaries come from the existing base images.

## Source exposure

This repository starts with a fresh history containing only the protected distribution.
Earlier source commits, remotes, and fork metadata are not included. Original code
published elsewhere and prior downloads remain available independently of this
repository. The packed files here can also be decoded and inspected. Native
compilation improves the distributed image's resistance to casual extraction;
it cannot make publicly distributed code confidential. Required author credits
and licensing notices are retained.

## Regeneration

Use original files in a separate source directory; never obfuscate generated output
again. Keep source and deployed configuration backups for maintenance.

Install tools/requirements.txt in an isolated Python environment and install the
Node dependencies in tools/package.json. Run:

```sh
python tools/pack_python.py ORIGINAL_DIRECTORY OUTPUT_DIRECTORY
node tools/obfuscate_web.cjs ORIGINAL_DIRECTORY OUTPUT_DIRECTORY
```

The Dockerfile runs tools/build_native.py in the panel image's build stage.

## Checks

Six native modules and two launchers compiled on macOS with Python 3.11. Fresh,
legacy, and repeated path generation passed. Bootstrap configuration and rate
limiting matched original behavior. Native helper import routing was checked.
The native health launcher matched the original's success and failure status in
five mocked cases.

A jsdom harness compared subscription rendering, language switching, QR drawing
pixels, and dialog behavior for five subscription statuses in English and Persian.
Dashboard initialization and JavaScript syntax passed. These checks do not replace
real browser performance checks. Full Linux Docker deployment, live database helper
execution, and complete service startup remain unverified.
