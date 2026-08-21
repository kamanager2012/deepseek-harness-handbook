# Current Community release status

> Evidence snapshot: 2026-08-21. The `v0.1.2` exact-artifact smoke passed on real Windows, macOS, and Linux runners; installer/Runtime first-ready evidence is `[PARTIAL]`, while the full user loop remains `[待复核]`. This page does not replace the GitHub Release, Actions result, or installer smoke test.

## Three-layer version model

| Layer | Current value | Meaning |
|---|---|---|
| Codebase trunk | `0.1.0-rc.8-community.1` | Current `main` community version; not published as a user Release |
| Official core | `@deepseek-ai/dsh@0.1.0-rc.8` | Official core baseline; the community suffix identifies a community-owned fix |
| Published Latest | `v0.1.2` | Current published Stable; exact-artifact smoke is partial and the full user loop still requires review |
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
`[PARTIAL]`; first-launch/missing-key smoke passed, but the full user loop still requires
review. Official Web is the official `~/.dsh`-sharing compatibility entry, not a Community
endpoint.

## Three-platform Release Gate

Observed for this snapshot; the full user loop remains `[待复核]`:

| Gate | Status | Evidence boundary |
|---|---|---|
| Normal `dsh-community` CI | `[待复核]` | Passing main CI does not prove installer readiness |
| Release assets | `[REAL]` | `v0.1.2` has an AppImage, dmg, and Windows Setup, each with SHA256 |
| artifact-smoke | `[PARTIAL]` | [Run 32470195309](https://github.com/kamanager2012/dsh-community/actions/runs/32470195309) passed resolve, Windows, macOS, and Linux jobs |
| Official Runtime staging / installer | `[PARTIAL]` | Real v0.1.2 Windows/macOS assets installed and reached Runtime readiness; the full lifecycle is not covered |
| Three-OS release gate | `[PARTIAL]` | Real-asset checksum, desktop first-ready, and Linux TUI failure paths passed; the full user loop remains open |

```text
tag
  → Linux / Windows / macOS build
  → artifact + SHA256
  → publish GitHub Release
```

`v0.1.2` is the current published Latest. The next goal is not another version number:
add Session, plugin, upgrade/reinstall, network-failure, and first-conversation evidence
beyond the exact-artifact smoke; keep `0.1.0-rc.8-community.1` as a source line until then.

## Stable release baseline vs current main

`v0.1.2` is the current Stable baseline. The code/package line is
`0.1.0-rc.8-community.1`, based on official core `@deepseek-ai/dsh@0.1.0-rc.8`.
A main-source smoke test or CI result cannot replace Release-asset and installation review,
so this draft must not say that the installer has been verified.

## Distribution Reality Gate

The project is now entering the user-reality gate rather than expanding the Build Gate.
Completed first-launch smoke is `[PARTIAL]`; uncovered full-loop evidence remains `[待复核]`:

| Scenario | Status | Must prove |
|---|---|---|
| Windows clean VM + `DSH.Community.Setup.0.1.2.exe` | `[PARTIAL]` | [Run 32470195309](https://github.com/kamanager2012/dsh-community/actions/runs/32470195309) downloaded, checked, silently installed, launched, and reached Runtime HTTP readiness |
| macOS clean host + `dsh-community-0.1.2.dmg` | `[PARTIAL]` | The same run downloaded, checked, mounted, launched, and reached Runtime HTTP readiness |
| WSL/Linux clean host + `dsh-community` / `pnpm tui` | `[PARTIAL]` | The same run passed TUI help/version, missing-key doctor, sessions, and no-TTY refusal paths |
| Session loop | `[待复核]` | New, resume, and the same `~/.dsh` Session across Official Web ↔ Windows/macOS Desktop ↔ WSL/Linux TUI |
| Plugin / restart | `[待复核]` | Official `dsh plugin add`, restart persistence, and explicit failure output |
| Lifecycle recovery | `[待复核]` | Uninstall/reinstall, upgrade, bad network, missing key, and interrupted extraction |
| Official Runtime staging / installer | `[PARTIAL]` | Real Windows/macOS assets reached first-ready; do not claim the full installation lifecycle is verified |

This gate must use the packages downloaded from the Release page and the result of the
staging redesign. Main-source smoke, ordinary CI, or README claims cannot substitute for
it. [Run 32470195309](https://github.com/kamanager2012/dsh-community/actions/runs/32470195309)
passed the real-asset Windows, macOS, and WSL/Linux smoke jobs `[PARTIAL]`; that subset
does not prove Session sharing, plugin restart, lifecycle recovery, or a successful first
conversation.

## Current project phases

| Phase | Estimate | Current evidence |
|---|---:|---|
| Phase 1 · Suite Reality Gate | about 80–90% `[待复核]` | Shell compound/metacharacter fail-closed, typed `SessionEvent.data` adapter, pre-enqueue fallback guard, and tests have advanced; true SDK runtime E2E remains unproven and upstream probe CI remains red |
| Phase 2 · Edition → Community | 100% `[待复核]` | Session selector, `new`, `resume last`, `sessions`, and `doctor` have merged; Edition code is frozen, the GitHub repository is archived, and its description points to Community |
| Phase 3 · Cross-platform Release | `[PARTIAL]` | `v0.1.2` assets and SHA256 files are published and exact-artifact smoke passed; the full lifecycle remains open |
| Phase 4 · Distribution Reality Gate | `[PARTIAL]` | The four-job artifact-smoke run passed, but Session, plugin, lifecycle, and full user-loop evidence remain open |
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
