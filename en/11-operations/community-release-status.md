# Current Community release status

> Evidence snapshot: 2026-08-16. This page separates code, Release layers, and CI evidence; it does not replace the latest GitHub Release, Actions result, or installer smoke test.

## Three-layer version model

| Layer | Current value | Meaning |
|---|---|---|
| Codebase trunk | `0.1.2` | The current `dsh-community` code/package line; not a Stable Release tag |
| Preview Release | `v0.1.2-preview` | The current test-oriented preview; fixes Web startup, system-Node preference, `DSH_COMMUNITY_BIN`, readiness polling, 502 warm-up, plugin child-process teardown, `doctor`, and the official plugin install/remove path |
| Stable Release | `v0.1.1` | Current Stable; the Linux AppImage has a known issue where official `dsh web` may fail to bind its port |

README and product pages should say “Stable / Preview / code line” instead of reducing
the product to `0.1.1`.

## User choice

The formal entry remains [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest).
Stable users should be told about the `v0.1.1` Desktop Web issue. Test users should use
[`v0.1.2-preview`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.2-preview),
which is closer to usable, while remembering that the visible assets are still mainly
the Linux AppImage and Windows/macOS are not proven just because workflows exist.

## Three-platform Release Gate

Observed for this snapshot:

| Gate | Status | Evidence boundary |
|---|---|---|
| Normal `dsh-community` CI | `[REAL]` / GREEN | Code, type, and ordinary tests pass |
| Linux packaging | `[REAL]` / GREEN | AppImage and SHA256 asset generation pass |
| Windows packaging | `[REAL]` / GREEN | The NSIS job succeeded in the latest Actions run `31930380661` |
| macOS packaging | `[REAL]` / GREEN | The dmg job succeeded in the latest Actions run `31930380661` |
| Release publish | `PENDING TAG` | The manual workflow skipped publish; a tag is still required to turn artifacts into GitHub Release downloads |
| Three-OS packaging gate | `[REAL]` / GREEN | Linux, Windows, and macOS builds passed; the user-facing tagged Release loop is still pending |

```text
tag
  → Linux / Windows / macOS build
  → artifact + SHA256
  → publish GitHub Release
```

The target chain exists; the successful chain does not yet. The next goal is a real
three-platform `0.1.2` Stable, not more `0.1.3` features.

## Current project phases

| Phase | Estimate | Current evidence |
|---|---:|---|
| Phase 1 · Suite Reality Gate | about 80–90% | Shell compound/metacharacter fail-closed, typed `SessionEvent.data` adapter, pre-enqueue fallback guard, and tests have advanced; true SDK runtime E2E remains unproven and upstream probe CI remains red |
| Phase 2 · Edition → Community | 100% | Session selector, `new`, `resume last`, `sessions`, and `doctor` have merged; Edition code is frozen, the GitHub repository is archived, and its description points to Community |
| Phase 3 · Cross-platform Release | packaging green | Linux, Windows, and macOS builds are green; tagged Release publishing is not closed |
| Phase 4 · Plugin supply chain | Not formally started | Keep the 7 rc.6-verified plugins and deepen existence/install/compose/runtime smoke/digest/provenance evidence first |
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
