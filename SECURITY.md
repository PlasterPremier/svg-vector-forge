# Security Policy — svg-vector-forge

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.9.x   | yes       |
| < 0.9   | no        |

## Threat model

`svg-vector-forge` loads third-party Python plugins from the
`vectorforge.plugins` entry-point group and from `%APPDATA%\vectorforge\plugins`.
Plugins execute with the full privileges of the host process. Treat a plugin
directory the same way you would treat a `pip install` from an untrusted
index.

## Hardening

- The loader refuses to import plugins whose manifest lacks a `sha256` field
  when `require_signed_plugins = true` in `config/plugins.toml`.
- SVG output is sanitized by `vectorforge.utils.svg_writer` — `<script>`,
  `<foreignObject>`, and `on*` attributes are stripped before disk write.
- The model cache writes weights under `%LOCALAPPDATA%\vectorforge\models` and
  never executes anything from that directory.

## Reporting a vulnerability

Email `security@svg-vector-forge.invalid` with a PoC. Do not open a public
issue. We aim to respond within 72 hours and to ship a fix within 14 days.