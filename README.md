# Karaoke Media 1

Media-only satellite for the existing [Harvey karaoke library](https://gmyoung.github.io/karaoke.html). The player, song catalog, subtitles and interface stay in `GMyoung/GMyoung.github.io`. This repository supplies additional versioned video/audio at `https://gmyoung.github.io/karaoke-media-1/`, on the same origin as the player.

Only `public/` is published. `public/index.html` links back to the player; `robots.txt` and the page's robots meta tag request no indexing. These requests do not provide access control: repository contents and deployed media are public.

## Files and source boundaries

- `public/media/streams-v5/`: BIRDBRAIN and Forever HLS masters, renditions, fragments and compact compatibility MP4s.
- `public/media/streams-v6/`: 马 (Ma), with the supplied Japanese-version picture aligned to the Chinese-song timeline, separate Chinese original/instrumental tracks, and 360p/720p/1080p HLS plus a compatibility MP4.
- `public/audio/`: aligned, prepared AAC/M4A soundtracks referenced by the main catalog.
- `scripts/check-public.py`: read-only validation of public file boundaries and sizes; emits JSON.
- `.github/workflows/pages.yml`: pinned GitHub Actions workflow that validates and deploys only `public/`.

Source downloads, full-quality masters, source-catalog snapshots, timing/alignment work, logs and private records remain outside `public/` and preferably outside this repository. Production currently lives under `E:\CodeX\outputs`, with source downloads under `C:\Users\Harvey\Downloads\karaoke`. Do not copy keys, tokens, credentials, environment files or source manifests into public assets.

Keep all playlist references valid relative to their published path. In the main catalog, use the full same-origin URLs, for example `https://gmyoung.github.io/karaoke-media-1/media/streams-v5/<song>/video-only.m3u8` and `https://gmyoung.github.io/karaoke-media-1/audio/<song>.m4a`. Never point a satellite playlist at an unavailable local path or an unshipped rendition. The main repository's publisher skips external URL resources; publish this satellite successfully before updating those main-catalog references.

## Publish

Prerequisites: Python 3.10+ for the local size check, Git, and an existing authorized GitHub/Git credential manager. No Node build, npm dependency, API key, persistent environment variable or custom stored deployment secret is needed. GitHub Actions uses the runner's Python and short-lived GitHub token/OIDC with `contents: read`, `pages: write`, and `id-token: write`.

1. Place finalized versioned assets in `public/media/` and `public/audio/`.
2. From this repository run `py -3.12 scripts/check-public.py` on Windows, or `python3 scripts/check-public.py` elsewhere. The check rejects symlinks, unexpected top-level public paths, individual files of 100 MiB or more, and a complete artifact of 1,000,000,000 bytes or more. It only reads saved files; it is not a playback test.
3. Review and commit the prepared files, then push `main`. The repository's GitHub Pages source must be **GitHub Actions**. The **Publish Karaoke Media 1** workflow validates, uploads `public/`, and deploys it. A manual run can use `gh workflow run pages.yml --ref main` after the remote repository and Pages configuration exist.
4. Confirm the exact deployment and read back the published playlist/audio file metadata before switching the main catalog to those URLs. Playback, visual quality, lyric timing and mixing are manually reviewed by the user; do not launch functional tests or automatically open the built-in browser.

The remote repository is `GMyoung/karaoke-media-1`, with GitHub Pages configured to use GitHub Actions. Media preparation and main-catalog updates remain separate from this publishing workflow.

## Maintenance

Keep versioned URLs stable and retain accepted masters and previous versions in local/Git history. Account for the complete `public/` directory before each release; move future additions to another same-origin satellite before reaching the cap. Media delivery remains subject to GitHub Pages and venue connectivity, so this layout does not guarantee uninterrupted playback under every network condition.

Update the existing karaoke tool record and `E:\CodeX\tool-records\index.json` when URLs, commands, publishing configuration, credentials or asset workflows change. Record the satellite URL, repository and production source locations without credential values. All music and video rights belong to their respective creators.
