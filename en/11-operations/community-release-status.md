# Current Community release status

> Evidence snapshot: 2026-08-16. This page separates code, Release layers, and CI evidence; it does not replace the latest GitHub Release, Actions result, or installer smoke test.

## Three-layer version model

| Layer | Current value | Meaning |
|---|---|---|
| Codebase trunk | `0.1.4` | The current `dsh-community` code/package line; not a Stable Release tag |
| Stable Release | `v0.1.4` | Current Stable; the GitHub Release publishes the Linux AppImage, Windows NSIS installer, macOS dmg, and matching SHA256 files |
| Preview Release | `v0.1.3` | Latest Preview; not the current Stable download target |

README and product pages should say “Stable / Preview / code line” instead of collapsing
the old Preview, code line, and Stable into one version number.

## User choice

The formal entry remains [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest).
Stable users should download [`v0.1.4`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.4).
The `v0.1.1` Web-startup issue is historical and should not remain the current download advice.
Use [`v0.1.3`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.3) when
testing the latest Preview. `v0.1.2-preview` is retained only as an older regression record.

The current `v0.1.4` assets are:

- `dsh-community-0.1.4.AppImage` + `.sha256` (optional/secondary Linux artifact)
- `DSH.Community.Setup.0.1.4.exe` + `.sha256` (Windows Desktop)
- `dsh-community-0.1.4.dmg` + `.sha256` (macOS Desktop)

The primary Linux Community endpoint is WSL/Linux Terminal; Official Web is an upstream
companion, not a Community download endpoint.

## Three-platform Release Gate

Observed for this snapshot:

| Gate | Status | Evidence boundary |
|---|---|---|
| Normal `dsh-community` CI | `[REAL]` / GREEN | Code, type, and ordinary tests pass |
| Linux packaging | `[REAL]` / GREEN | AppImage and SHA256 asset generation pass |
| Windows packaging | `[REAL]` / GREEN | The NSIS installer and SHA256 file are published in `v0.1.4` |
| macOS packaging | `[REAL]` / GREEN | The dmg and SHA256 file are published in `v0.1.4` |
| Release publish | `[REAL]` / GREEN | The [`v0.1.4` GitHub Release](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.4) is public and downloadable |
| Three-OS release gate | `[REAL]` / GREEN | `v0.1.4` closes the Linux, Windows, and macOS asset-plus-checksum loop |

```text
tag
  → Linux / Windows / macOS build
  → artifact + SHA256
  → publish GitHub Release
```

`v0.1.4` has completed the three-platform Stable chain. The next goal is to maintain
release assets, installation evidence, and version-drift detection rather than stack
new version numbers before the facts are closed.

## Stable release baseline vs current main

`v0.1.4` is the current three-platform Stable baseline. Current `main` remains on the
`0.1.4` code/package line; a main-source smoke test or CI result cannot replace validation
of the published installer. `v0.1.2` is retained only as the historical first
three-platform baseline. To validate Stable, download the actual files from the
[v0.1.4 Release](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.4)
and record the filename and SHA256.

## Distribution Reality Gate

The project is now entering the user-reality gate rather than expanding the Build Gate.
The following exact-release-artifact evidence is still `[UNVERIFIED]` until it runs on
clean environments:

| Scenario | Status | Must prove |
|---|---|---|
| Windows clean VM + `DSH.Community.Setup.0.1.4.exe` | `[UNVERIFIED]` | Install, first launch, key setup, Runtime extraction, and clean exit |
| macOS clean host + `dsh-community-0.1.4.dmg` | `[UNVERIFIED]` | Install, first launch, permission prompts, Runtime boot, and clean exit |
| WSL/Linux clean host + `dsh-community` / `pnpm tui` | `[UNVERIFIED]` | Terminal launch, key setup, new/resume, and clean exit |
| Linux optional artifact + `dsh-community-0.1.4.AppImage` | `[UNVERIFIED]` | AppImage launch and Runtime boot; not the primary Linux endpoint |
| Session loop | `[UNVERIFIED]` | New, resume, and the same `~/.dsh` Session across Official Web ↔ Windows/macOS Desktop ↔ WSL/Linux TUI |
| Plugin / restart | `[UNVERIFIED]` | Official `dsh plugin add`, restart persistence, and explicit failure output |
| Lifecycle recovery | `[UNVERIFIED]` | Uninstall/reinstall, upgrade, bad network, missing key, and interrupted extraction |

This gate must use the packages downloaded from the Release page. Main-source smoke,
ordinary CI, or README claims cannot substitute for it.
The latest `artifact-smoke` run [31935679026](https://github.com/kamanager2012/dsh-community/actions/runs/31935679026)
passed its macOS exact job but failed its Windows exact job, so the user-reality gate
remains `[UNVERIFIED]`.

## Current project phases

| Phase | Estimate | Current evidence |
|---|---:|---|
| Phase 1 · Suite Reality Gate | about 80–90% | Shell compound/metacharacter fail-closed, typed `SessionEvent.data` adapter, pre-enqueue fallback guard, and tests have advanced; true SDK runtime E2E remains unproven and upstream probe CI remains red |
| Phase 2 · Edition → Community | 100% | Session selector, `new`, `resume last`, `sessions`, and `doctor` have merged; Edition code is frozen, the GitHub repository is archived, and its description points to Community |
| Phase 3 · Cross-platform Release | 100% | `v0.1.4` publishes Linux, Windows, and macOS installers plus SHA256 files |
| Phase 4 · Distribution Reality Gate | In progress | Start with exact `v0.1.4` assets: Windows/macOS Desktop, WSL/Linux Terminal, plugins, restart, upgrade, and failure paths |
| Phase 4 workstream · Plugin supply chain | Main work complete | The registry has 9 third-party plugins install/compose-tested on rc.6; shape, npm existence, `dist.integrity`, repository reachability, and provenance are in CI, while runtime smoke remains per-plugin manual evidence |
| Phase 4 workstream · Marketplace UX | 100% | `info` displays digest/provenance, `install` prints the registry digest and an `npm view ... dist.integrity` verification command; the current suite is 11/11 green |
| Phase 5 · Handbook drift CI | Not started | This page is currently the manual fact entry |

## Runtime version-source distinction

```text
Official GitHub main release commit: 47f9438 / rc.5
Community published-package target:  @deepseek-ai/dsh@0.1.0-rc.6
```

This is not automatically a contradiction: a published package can move ahead of the
visible GitHub release commit. For CLI, Session, Event, SDK, and plugin claims, check the
published/installed package, current `--help`, exported configuration, contract snapshots,
and real runtime output.

References:

- [Official upstream commit `47f9438`](https://github.com/deepseek-ai/deepseek-harness/commit/47f9438)
- [`dsh-community` release workflow](https://github.com/kamanager2012/dsh-community/blob/main/.github/workflows/release.yml)
- [`dsh-community` changelog](https://github.com/kamanager2012/dsh-community/blob/main/CHANGELOG.md)
- [`dsh-community` contract snapshots](https://github.com/kamanager2012/dsh-community/tree/main/contracts)
- [`deepseek-harness-suite` Actions](https://github.com/kamanager2012/deepseek-harness-suite/actions)
- [`dsh-community-edition` freeze commit `09eb1c0`](https://github.com/kamanager2012/dsh-community-edition/commit/09eb1c0)
