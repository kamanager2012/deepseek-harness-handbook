# Current Community release status

> Evidence snapshot: 2026-08-21. GitHub Release metadata is checked; installer, staging, and full user-loop claims remain `[待复核]`. This page does not replace the GitHub Release, Actions result, or installer smoke test.

## Three-layer version model

| Layer | Current value | Meaning |
|---|---|---|
| Codebase trunk | `0.1.0-rc.8-community.1` | Current `main` community version; not published as a user Release |
| Official core | `@deepseek-ai/dsh@0.1.0-rc.8` | Official core baseline; the community suffix identifies a community-owned fix |
| Published Latest | `v0.1.2` | Current published Stable; installer/user-loop evidence still requires review |
| Draft / pre-release | `v0.1.6` | Draft/pre-release; checksum assets only, not a download entry |

README and product pages should say “Stable / Preview / code line” instead of collapsing
the old Preview, code line, and Stable into one version number.

Desktop and TUI must show the same identity badge:

```text
DeepSeek Harness Community v0.1.0-rc.8-community.1 [Official Core: @deepseek-ai/dsh@0.1.0-rc.8]
```

## User choice

The formal entry remains [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest).
Stable users should download the published [`v0.1.2`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.2)
from [`releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest).
Do not download draft `v0.1.6` or promote the `0.1.0-rc.8-community.1` source line or staging output as Stable.

The published `v0.1.2` assets are:

- `dsh-community-0.1.2.AppImage` + `.sha256`
- `DSH.Community.Setup.0.1.2.exe` + `.sha256` (historical published filename)
- `dsh-community-0.1.2.dmg` + `.sha256`

The three Community endpoints are WSL/Linux Terminal, Windows Desktop, and macOS Desktop
`[待复核]`. Official Web is the official `~/.dsh`-sharing compatibility entry, not a
Community endpoint.

## Three-platform Release Gate

Observed for this snapshot `[待复核]`:

| Gate | Status | Evidence boundary |
|---|---|---|
| Normal `dsh-community` CI | `[待复核]` | Passing main CI does not prove installer readiness |
| Release assets | `[REAL]` | `v0.1.2` has an AppImage, dmg, and Windows Setup, each with SHA256 |
| artifact-smoke | `[待复核]` | One Windows, macOS, and WSL/Linux clean-machine first-launch round is recorded |
| Official Runtime staging / installer | `[待复核]` | Exact-artifact installation evidence is not closed; do not write “installer verified” |
| Three-OS release gate | `[待复核]` | Published assets and a smoke subset exist, but the full user loop is not closed |

```text
tag
  → Linux / Windows / macOS build
  → artifact + SHA256
  → publish GitHub Release
```

`v0.1.2` is the current published Latest. The next goal is not another version number:
recheck the exact artifact, installation path, Runtime staging, and full user-loop evidence;
keep `0.1.0-rc.8-community.1` as a source line until then.

## Stable release baseline vs current main

`v0.1.2` is the current Stable baseline. The code/package line is
`0.1.0-rc.8-community.1`, based on official core `@deepseek-ai/dsh@0.1.0-rc.8`.
A main-source smoke test or CI result cannot replace Release-asset and installation review,
so this draft must not say that the installer has been verified.

## Distribution Reality Gate

The project is now entering the user-reality gate rather than expanding the Build Gate.
The following exact-release-artifact evidence remains `[待复核]` while staging is not
ready and the facts are not finalized:

| Scenario | Status | Must prove |
|---|---|---|
| Windows clean VM + `DSH.Community.Setup.0.1.2.exe` | `[待复核]` | One artifact-smoke first-launch round is recorded; this is not an installer/staging verification claim |
| macOS clean host + `dsh-community-0.1.2.dmg` | `[待复核]` | One artifact-smoke first-launch round is recorded; this is not an installer/staging verification claim |
| WSL/Linux clean host + `dsh-community` / `pnpm tui` | `[待复核]` | One artifact-smoke first-launch round is recorded; the full user loop remains open |
| Session loop | `[待复核]` | New, resume, and the same `~/.dsh` Session across Official Web ↔ Windows/macOS Desktop ↔ WSL/Linux TUI |
| Plugin / restart | `[待复核]` | Official `dsh plugin add`, restart persistence, and explicit failure output |
| Lifecycle recovery | `[待复核]` | Uninstall/reinstall, upgrade, bad network, missing key, and interrupted extraction |
| Official Runtime staging / installer | `[待复核]` | Do not claim the installer is verified |

This gate must use the packages downloaded from the Release page and the result of the
staging redesign. Main-source smoke, ordinary CI, or README claims cannot substitute for
it. One round of `v0.1.2` artifact-smoke completed Windows, macOS, and WSL/Linux clean-
machine first-launch checks `[待复核]`, but that subset does not prove the installer is verified.

## Current project phases

| Phase | Estimate | Current evidence |
|---|---:|---|
| Phase 1 · Suite Reality Gate | about 80–90% `[待复核]` | Shell compound/metacharacter fail-closed, typed `SessionEvent.data` adapter, pre-enqueue fallback guard, and tests have advanced; true SDK runtime E2E remains unproven and upstream probe CI remains red |
| Phase 2 · Edition → Community | 100% `[待复核]` | Session selector, `new`, `resume last`, `sessions`, and `doctor` have merged; Edition code is frozen, the GitHub repository is archived, and its description points to Community |
| Phase 3 · Cross-platform Release | `[待复核]` | `v0.1.2` assets and SHA256 files are published; this is not an installer-verification claim |
| Phase 4 · Distribution Reality Gate | `[待复核]` | One Win/mac/Linux first-launch smoke round is recorded, but installer/staging evidence and the full loop remain open |
| Phase 4 workstream · Plugin supply chain | `[待复核]` | 9 verified plugins; CI covers shape, npm existence/version, `dist.integrity`, provenance, repository reachability, and compose |
| Phase 4 workstream · Marketplace UX | `[待复核]` | CLI is `list/search/info/install`; `info` displays digest/provenance |
| Phase 5 · Handbook drift CI | Not started `[待复核]` | This page is currently the manual fact entry |

## Runtime version-source distinction

```text
Official GitHub / package source: @deepseek-ai/dsh@0.1.0-rc.8
Community source line: 0.1.0-rc.8-community.1
Published Latest: v0.1.2
Draft/pre-release: v0.1.6 (not a user download)
```

For CLI, Session, Event, SDK, and plugin claims, check the published/installed package,
current `--help`, exported configuration, contract snapshots, and real runtime output;
do not infer the current version from an old snapshot.

References:

- [`dsh-community` release workflow](https://github.com/kamanager2012/dsh-community/blob/main/.github/workflows/release.yml)
- [`dsh-community` changelog](https://github.com/kamanager2012/dsh-community/blob/main/CHANGELOG.md)
- [`dsh-community` contract snapshots](https://github.com/kamanager2012/dsh-community/tree/main/contracts)
- [`deepseek-harness-suite` Actions](https://github.com/kamanager2012/deepseek-harness-suite/actions)
- [`dsh-community-edition` freeze commit `09eb1c0`](https://github.com/kamanager2012/dsh-community-edition/commit/09eb1c0)
