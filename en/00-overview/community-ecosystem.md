# DeepSeek Harness Community ecosystem

> Project handoff and product-entry map. Baseline date: 2026-08-21.

The community project is not a fork of DeepSeek Harness and not another Agent Runtime.
The official [DeepSeek Harness Runtime](https://github.com/deepseek-ai/deepseek-harness)
remains the only execution core. Community repositories add distribution, compatibility,
plugins, knowledge, diagnostics, and experiments around it.

## Three conclusions

1. **The official Runtime is the engine.** It owns the Agent loop, model execution,
   tool execution, official Session persistence, and core lifecycle.
2. **`dsh-community` is the only canonical product.** Normal users download, install,
   and use it.
3. **Suite is a laboratory.** `deepseek-harness-suite` capabilities must pass Reality
   Gate, real E2E, security checks, and cross-platform smoke before promotion to
   `dsh-community` Canary, Preview, or Stable.

## Where users start

```text
Official DeepSeek Harness Runtime
            │
            ▼
       dsh-community
        ├── WSL/Linux Terminal
        ├── Windows Desktop
        └── macOS Desktop
```

The formal download entry is
[`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest).
The currently published GitHub Latest is `v0.1.2`. Its Release assets include the Linux
AppImage, macOS dmg, and Windows `DSH.Community.Setup.0.1.2.exe`, each with a matching
`.sha256` sidecar. The current source / next release line is
`0.1.0-rc.8-community.1`, based on official core `@deepseek-ai/dsh@0.1.0-rc.8`, and
has not been published as a user Release. `v0.1.6` is a draft/pre-release with checksum
assets only, not a download entry. Installer and full user-loop evidence remain
`[UNVERIFIED]`; use the [current release status](../11-operations/community-release-status.md)
and the [release runbook](../11-operations/community-release-runbook.md) for the boundary.
The three Community endpoints are **WSL/Linux Terminal, Windows Desktop, and macOS
Desktop** `[待复核]`. Official Web is the official `~/.dsh`-sharing compatibility entry,
not our endpoint. The Linux AppImage is a release artifact shape, not a fourth Community
endpoint `[待复核]`.
Do not ask users to choose between Community, Suite, Edition, Marketplace, and Plugins:
those names describe product-support roles, not competing clients.

## Six repositories, six responsibilities

| Repository | Role | Audience | Formal download entry? |
|---|---|---|---|
| [`dsh-community`](https://github.com/kamanager2012/dsh-community) | Canonical Product: Desktop, TUI, diagnostics, compatibility, and releases | All users and maintainers | **Yes; the only one** |
| [`deepseek-harness-suite`](https://github.com/kamanager2012/deepseek-harness-suite) | Community Labs: SDK transport, security, checkpoints, Bridge, and experimental UX | Maintainers and experimenters | No |
| [`deepseek-harness-handbook`](https://github.com/kamanager2012/deepseek-harness-handbook) | Knowledge / Evidence: installation, operations, acceptance, and version facts | Users, maintainers, and Agents | No |
| [`dsh-community-plugins`](https://github.com/kamanager2012/dsh-community-plugins) | Compatibility Registry: plugin metadata, versions, and verification lines | Plugin authors and maintainers | No |
| [`dsh-marketplace`](https://github.com/kamanager2012/dsh-marketplace) | Discovery / Distribution UX: browse, search, and install entry | Users and plugin authors | No; not a Runtime |
| [`dsh-community-edition`](https://github.com/kamanager2012/dsh-community-edition) | Merge & Archive: code frozen, useful UX merged, and the GitHub repository archived with a Community pointer | Maintainers | No; historical reference only |

## Official and community boundaries

| Official Runtime owns | Community layer owns |
|---|---|
| Agent loop and model execution | Desktop / TUI distribution experience |
| Tool execution and Runtime lifecycle | Lifecycle wrapping, diagnostics, and compatibility |
| Official Session persistence and events | Reading, resuming, and presenting official Sessions |
| Official profiles, CLI, and plugin surface | Bridge normalization, registry metadata, packaging, and safe integration |

The community layer must not reimplement the Agent loop, maintain a second equivalent
Session source of truth, fork the official event vocabulary, or vendor official core
packages. Use an official capability when it exists; add a community extension only for
a verified gap.

## Registry and Marketplace

```text
dsh-community-plugins
        │ catalog / testedDsh / verification
        ▼
dsh-marketplace
        │ browse / search / install UX
        ▼
official dsh plugin add chain
```

The registry records compatibility evidence. The marketplace presents it and invokes the
official installation path. Neither repository owns the Runtime or replaces the official
plugin manager.

Current evidence snapshot `[待复核]`: the registry has 9 verified plugins. CI checks
shape, npm existence/version, `dist.integrity`, provenance, and repository reachability;
the compose workflow runs the official `dsh plugin add` chain and a composition assertion
per plugin. The Marketplace CLI provides `list`, `search`, `info`, and `install`; `info`
displays digest/provenance and installation remains on the official chain.

Current release boundary `[UNVERIFIED]`: `v0.1.2` is the published Latest, but installer,
Runtime staging, and full user-loop evidence still require review. Do not call a build,
published asset, or smoke output a “verified installer”. Recorded artifact-smoke is only
a Windows, macOS, and WSL/Linux first-launch subset; `v0.1.6` draft is not a user download.

## Reality language

Use explicit labels:

| Label | Meaning |
|---|---|
| `[REAL]` | Code, tests, and reproducible runtime evidence exist |
| `[PARTIAL]` | Some implementation exists but a known gap remains |
| `[LABS]` | Community Labs only; not promoted to the product |
| `[PROBE]` | A probe observed behavior; stability is not established |
| `[FAIL-CLOSED]` | Unknown or high-risk behavior is rejected or requires approval |
| `[WORKSPACE-JAIL]` | Workspace containment and escape tests are present |
| `[BLOCKED_BY_UPSTREAM]` | The official Runtime or SDK lacks a required loop |
| `[UNVERIFIED]` | Real E2E, cross-platform, or failure-path evidence is missing |
| `[NOT_IMPLEMENTED]` | The capability does not currently exist |

Do not use “production-ready”, “fully secure”, or “100% compatible” without evidence.

## Maintainer links

- [Chinese ecosystem page](../../content/00-overview/community-ecosystem.md)
- [Current release status](../11-operations/community-release-status.md)
- [Community Labs handoff](../11-operations/community-labs-handoff.md)
- [Release checklist](../../content/11-operations/release-checklist.md)
- [Handbook repository guide](https://github.com/kamanager2012/deepseek-harness-handbook/blob/main/README.en.md)
