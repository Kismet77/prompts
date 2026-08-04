# The Sceptic's Desk — hosted prompt library

The pages the QR codes in *AI Trading, Demystified* land on.

## What's here

```
index.html              Landing page
404.html                Fallback for old or mistyped links
.nojekyll               Stops GitHub Pages running Jekyll over the files
assets/style.css        All styling, one file
prompts/index.html      Prompt library index
prompts/p/1/index.html  → guide page 11, "learn any concept"
prompts/p/16/index.html → guide page 14, position size
prompts/p/19/index.html → guide page 14, journal review
```

The three prompt paths match the QR payloads exactly, so **existing printed copies keep working**. Don't rename these folders.

## Deploying

Copy the contents of `site/` into the root of the repository serving `kismet77.github.io`, commit, and push. GitHub Pages picks it up within a minute or two.

If the existing repo has other files you want to keep, copy in `assets/`, `prompts/`, `index.html`, `404.html`, and `.nojekyll` and leave the rest alone.

## Checks worth doing once it's live

1. Open `/prompts/p/1/` on a phone and tap **Copy prompt**. It should copy and the button should confirm.
2. Scan each of the three codes in the guide with a phone camera and confirm each lands on the right page.
3. Load a nonsense path such as `/prompts/p/99/` and confirm the 404 page appears.

## Moving to a custom domain

Everything internal uses relative links, so the site works unchanged on any domain. When the new domain is ready:

1. Add a file named `CNAME` at the repository root containing only the domain, for example `scepticsdesk.co.uk`.
2. Point a CNAME DNS record at `kismet77.github.io`, or A records at GitHub's IPs for an apex domain.
3. In the repo, under Settings → Pages, set the custom domain and tick **Enforce HTTPS**.

GitHub then redirects the old `kismet77.github.io` URLs to the new domain, so **codes already printed continue to work**. Only after that is confirmed should you change `DOMAIN` at the top of `build_qr.py` and rebuild the guide, so future print runs carry the new address.

## Adding more prompts

Edit `PROMPTS` in `build_site.py` and re-run it. Pages, the index, and navigation all follow. Keep the numbering consistent with the **guide's** scheme, which is separate from the Prompt Vault's 1 to 42.

## Fonts

Space Grotesk and JetBrains Mono load from Google Fonts. If you'd rather not depend on a third party, self-host the two families in `assets/` and swap the `<link>` in `build_site.py` for a local `@font-face` block. The pages degrade to system fonts if the request fails, so nothing breaks either way.
