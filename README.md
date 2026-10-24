# Nuvio — unofficial AltStore / SideStore source

Tracks IPA releases published by [NuvioMedia/NuvioMobile](https://github.com/NuvioMedia/NuvioMobile). Downloads go directly to the upstream release assets. This repository is an independent source listing, maintained by gilma0.

[![Add source to LiveContainer](https://img.shields.io/badge/Add_source_to-LiveContainer-7057D9?style=for-the-badge)](https://gilma0.github.io/nuvio_ipa_source/?action=livecontainer)
[![Add source to SideStore](https://img.shields.io/badge/Add_source_to-SideStore-1677FF?style=for-the-badge)](https://gilma0.github.io/nuvio_ipa_source/?action=sidestore)

Open the buttons on your iPhone or iPad with LiveContainer or SideStore already installed. The HTTPS page opens the selected app; if prompted, tap its add-source button.

LiveContainer must already be installed and configured.

**Source URL:** `https://gilma0.github.io/nuvio_ipa_source/source.json`

You can also paste this URL into SideStore or AltStore manually. Both buttons subscribe to the source for future updates. LiveContainer must support AltStore sources (LiveContainer 3.7 or later).

## Automatic updates and GitHub Pages

The workflow in [`.github/workflows/update-source.yml`](.github/workflows/update-source.yml) checks upstream releases every 15 minutes, on relevant pushes to `main`, and when run manually. GitHub may delay scheduled runs. It regenerates `source.json`, commits changes, and deploys `source.json` plus the source page to GitHub Pages in the same run. No IPA is built or mirrored.

Pages must use **GitHub Actions** as its build source (Settings → Pages → Build and deployment). The workflow uses the built-in `GITHUB_TOKEN`; no personal token or signing secrets are needed. The update job has `contents: write`; the deploy job has `pages: write` and `id-token: write`. An upstream failure or missing IPA stops the run and preserves the published source.

GitHub can disable scheduled workflows after 60 days of repository inactivity. Re-enable the workflow in Actions if needed. Run **Update and publish source** manually for the first deployment or to refresh immediately.

## Configuration

Edit `config.json` to change source/app metadata or the upstream release asset pattern. Release mode includes published prereleases with matching IPA assets, preserving Nuvio's beta release behavior. Static mode accepts an explicit `versions` array.

To regenerate locally with Python 3.12 or later:

```sh
python scripts/generate_source.py
```

Links use the [SideStore source URL scheme](https://docs.sidestore.io/docs/advanced/url-schema) (`sidestore://source?url=…`) and [LiveContainer source URL scheme](https://github.com/LiveContainer/LiveContainer/blob/main/LiveContainerSwiftUI/Views/LCAltStoreSourcesView.swift) (`livecontainer://source?url=…`). Both receive this repository’s `source.json` URL. The HTTPS landing page allows the README buttons to open these app URL schemes.
