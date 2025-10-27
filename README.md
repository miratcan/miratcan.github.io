# Mirat.dev (Lektor)

Personal site and blog powered by [Lektor](https://www.getlektor.com/).  
This branch (`source`) holds the editable project files; the `master` branch only keeps the generated static output that GitHub Pages serves.

## Requirements
- Python 3.8+ (the project is developed with Python 3.13 via `pipx`)
- Lektor CLI: `pipx install lektor` or `pip install --user lektor`
- Network access for the first run so that Lektor can download the plugins listed in `mysite.lektorproject` (`lektor-tags`, `lektor-minify`, `lektor-atom`, `lektor-markdown-highlighter`)

### Install/update plugins
```bash
lektor plugins reinstall
```
> If you are offline the command will fail; rerun it when you have network access so the plugins are cached locally.

## Run locally
```bash
lektor server -p 5000
```
Then browse to http://localhost:5000.  
You can change the port or run with `-h 0.0.0.0` to expose it on your LAN.

## Build & Deploy
```bash
# Produce static output under ./build
lektor build -O build

# Deploy to GitHub Pages (configured in mysite.lektorproject)
lektor deploy ghpages
```
`lektor build` will overwrite the contents of `build/`. Commit the updated `build/` directory (or push the `master` branch) after a successful build.

## Project layout
- `content/` – All page content (`contents.lr` files) plus static attachments.  
  For example `content/carpim.html` is Miray's multiplication game that ends up at `/carpim.html` in the built site; keep this file if you rebuild.
- `templates/` – Jinja2 templates used by the blog, listing pages, etc.
- `models/` – Lektor models that describe fields for entries.
- `configs/` – Extra plugin configuration (`tags`, `markdown-highlighter`).
- `build/` – Last generated output (mirrors the `master` branch).
- `mysite.lektorproject` – Project metadata, deploy target and plugin list.
- `temp/` – Ignored scratch directory Lektor can use while building.

## Handy references
- Blog posts live under `content/articles/` and `content/blog/`.
- Drafts and notes live under `content/unpublished/`.
- Static verification files (CNAME, sitemap, yandex verification, etc.) stay inside `content/` so they survive new builds.

## Tips
- If automatic plugin downloads slow down your workflow, set `LEKTOR_DISABLE_PACKAGE_CACHE_UPDATES=1` temporarily, but remember to re-enable and update occasionally so you stay in sync with plugins.
- Keep the `build/` directory clean before deploying: `rm -rf build/*` and rerun `lektor build -O build` to ensure the published site only contains files produced by Lektor (the multiplication game is preserved because the source lives in `content/carpim.html`).
