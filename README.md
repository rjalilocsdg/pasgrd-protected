# Super JinX — protected distribution

A public distribution with a fresh Git history, transformed Python and browser code,
and native modules and launchers generated during the Docker build.

Copyright (c) 2026 [Super JinX](https://t.me/+WvKFv0lU_i5lNGE0).
Required author credits and branding are retained. See [LICENSE](LICENSE).

Deploy using the included Dockerfile. On Railway, attach a persistent volume at
`/var/lib/pasarguard` and route the service domain to port `8080`.
See [INSTALL.md](INSTALL.md) for configuration and [OBFUSCATION.md](OBFUSCATION.md)
for protection details, completed checks, and limitations.

Obfuscation is reversible. Full Linux Docker startup remains unverified.
