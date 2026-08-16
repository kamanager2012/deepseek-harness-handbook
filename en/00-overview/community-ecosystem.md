# DeepSeek Harness Community ecosystem

> Project handoff and product-entry map. Baseline date: 2026-08-16.

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
        ├── Desktop
        └── Terminal / TUI
```

The formal download entry is
[`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest).
Read the current versions as three separate layers: code line `0.1.2`, Stable
`v0.1.2`, and `v0.1.2-preview` as an older Preview retained for regression comparison.
The three-platform assets are published in `v0.1.2`; detailed evidence and upstream
version-source distinctions are recorded in the [current release status](../11-operations/community-release-status.md).
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

Current evidence snapshot: 9 third-party plugins have been install/compose-tested on
`0.1.0-rc.6`. Shape, npm existence, `dist.integrity`, repository reachability, and
provenance are automated checks; runtime smoke remains per-plugin manual evidence. The
Marketplace implementation is 11/11 green, displays digest/provenance in `info`, and
prints a digest verification command in `install` before invoking the official chain.

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
