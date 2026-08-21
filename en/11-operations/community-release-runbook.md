# Community release runbook

> Draft status: every current-status statement keeps the `[待复核]` marker. This page records reviewable code, Release, and workflow procedures; README prose is not runtime evidence.

Links: [Current release status](community-release-status.md) · [Release checklist](../../content/11-operations/release-checklist.md) · [Ecosystem map](../00-overview/community-ecosystem.md) · [dsh-community Release](https://github.com/kamanager2012/dsh-community/releases/latest)

## Current fact boundary

- The currently published Latest is `v0.1.2`, with `dsh-community-0.1.2.AppImage`, `dsh-community-0.1.2.dmg`, and `DSH.Community.Setup.0.1.2.exe`; every asset has a `.sha256` sidecar.
- The current source / next release line is `0.1.0-rc.8-community.1`, based on official core `@deepseek-ai/dsh@0.1.0-rc.8`; `v0.1.6` is a draft/pre-release with checksum assets only, not a user download.
- Desktop/TUI must show: `DeepSeek Harness Community v0.1.0-rc.8-community.1 [Official Core: @deepseek-ai/dsh@0.1.0-rc.8]`.
- The three Community endpoints are WSL/Linux Terminal, Windows Desktop, and macOS Desktop `[待复核]`. Official Web is the official `~/.dsh`-sharing compatibility entry.
- Installer, Runtime staging, and the full user loop remain `[待复核]`. Do not write “installer verified” in a Release note, web page, or handbook.
- One round of `v0.1.2` artifact-smoke completed Windows, macOS, and WSL/Linux clean-machine first-launch checks `[待复核]`. This is an install/first-ready/missing-key subset, not a full user loop.
- The `v0.1.4` lesson is that missing official Runtime dependencies require an immediate Latest rollback before a corrected Release `[待复核]`. Do not move or overwrite a published tag.

## 1. Freeze before release

Before invoking the release script, confirm:

- the working tree is clean;
- `CHANGELOG.md` has a section for the target version;
- the target tag does not already exist;
- artifact names and SHA256 sidecars match the workflow/source;
- only `dsh-community` is the release channel; Suite, Edition, Marketplace, and Plugins are not release channels;
- if staging is not ready, keep the result explicitly `[待复核]` and do not claim a Stable install loop.

## 2. The real `release.mjs` flow

The script is `dsh-community/scripts/release.mjs`. Its source-fixed tag syntax is:

```text
node scripts/release.mjs <vX.Y.Z[-prerelease]>
```

For example, a community-owned fix can use `v0.1.0-rc.8-community.1`. When the official
core changes, the community version first mirrors that core and may then add `-community.N`.
The placeholder is not a request to rerun the published `v0.1.2` tag. Never rerun an existing tag.

The script then:

1. checks tag syntax, a clean tree, an unused tag, the matching `CHANGELOG.md` section, and a push remote for `kamanager2012/dsh-community`;
2. runs `pnpm install --frozen-lockfile`, `pnpm typecheck`, and `pnpm test`;
3. runs `pnpm desktop:package -- --appimage` as the local Linux/AppImage sanity check;
4. creates and pushes the tag, which starts the GitHub `release` workflow.

Stop on any failure. Do not use `--force`, move a tag, or overwrite a published Release to repair a bad artifact.

## 3. Three-OS release workflow

The workflow builds and publishes; it does not replace user-reality acceptance:

| Job | Artifact / check |
|---|---|
| Linux | typecheck, test, AppImage, SHA256 |
| Windows | NSIS `DSH Community Setup <version>.exe`, SHA256 (historical `v0.1.2` asset: `DSH.Community.Setup.0.1.2.exe`) |
| macOS | dmg, SHA256 |
| publish | collect all three jobs and create a GitHub Release; refuse to replace an existing Release |

Only after assets and sidecars are actually uploaded may the publish result be recorded as “Release publish happened” `[待复核]`. This still does not prove Runtime staging or installer readiness.

## 4. SHA256 checks

Check the original files downloaded from the Release page, not a main build or a locally repackaged file:

```sh
sha256sum -c dsh-community-0.1.2.AppImage.sha256
shasum -a 256 dsh-community-0.1.2.dmg
```

Windows PowerShell:

```powershell
Get-FileHash 'DSH.Community.Setup.0.1.2.exe' -Algorithm SHA256
```

Record the actual filename, sidecar content, environment, and result. A matching hash proves file integrity only; it does not prove Runtime staging or a successful first conversation.

## 5. artifact-smoke gate

The workflow accepts an explicit tag. To review a published version, use the real tag:

```sh
gh workflow run artifact-smoke.yml --repo kamanager2012/dsh-community --field tag=v0.1.2
gh run list --repo kamanager2012/dsh-community --workflow artifact-smoke.yml --limit 1
```

The smoke subset covers:

- download of the exact Windows Setup, macOS dmg, and WSL/Linux Terminal entry;
- SHA256 verification for each downloaded asset;
- Windows silent install, macOS mount/launch, and Linux Terminal launch;
- official Runtime first-ready and missing-key/failure checks;
- process exit and no leftover smoke process.

It is not full user acceptance. Separately review new/resume, the same `~/.dsh` Session across Official Web and the three Community endpoints, plugin install/restart, upgrade, uninstall/reinstall, proxy/offline behavior, and interrupted extraction.

## 6. Latest promotion and rollback

### Promotion

Before promoting a Release to Latest, require Release assets, SHA256 files, all three workflow jobs, artifact-smoke, the staging conclusion, and a human user-loop record `[待复核]`. If any item is `NOT_READY` or `[待复核]`, keep the channel explicitly marked and do not write that Stable is verified.

### Rollback

If an installer is missing official Runtime dependencies (the `v0.1.4` lesson) `[待复核]`:

1. immediately stop promotion, download buttons, and automatic install guidance;
2. immediately roll the bad version back from the Latest promotion slot, preserving the Release, logs, hashes, and failure-environment evidence;
3. do not move, overwrite, or force-push a published tag;
4. cut a new patch/Release after repair, then rerun the three-OS workflow, SHA256, and artifact-smoke;
5. keep all statements `[待复核]` until staging and the user loop are reviewed again.

## 7. Handoff record

```text
Release tag:
Stable / Preview:
Assets and SHA256:
Three-OS workflow:
artifact-smoke:
Official Runtime staging: UNVERIFIED / READY [待复核]
User loop:
Known failure:
Rollback decision:
Next review:
```
