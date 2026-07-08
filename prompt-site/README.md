# The Trading Blueprint — Prompt Library

Static companion site for *AI Trading, Demystified*. No build step, no dependencies.

## Deploy on GitHub Pages

1. Create a new **public** repository named `prompts`
2. Upload everything in this folder to the repository root (keep the `p/` folder structure)
3. Repository → Settings → Pages → Source: **Deploy from a branch** → Branch: `main`, folder `/ (root)` → Save
4. After a minute or two the site is live at `https://YOUR-USERNAME.github.io/prompts/`

Individual prompts live at `https://YOUR-USERNAME.github.io/prompts/p/16/` etc.
These are the URLs to encode in the guide's QR codes.

## Adding a custom domain later

Settings → Pages → Custom domain. Set it on this same repository and existing
QR codes keep working if you encode the github.io URLs with a redirect, or
re-encode once the domain is final.
