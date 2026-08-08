# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-user RSS feed reader built with Flask and MySQL. The app fetches and displays RSS feed items, supports starring items for later, and has a basic feed admin interface.

## Running the app

```bash
flask --app reader --debug run --port 5002
```

## Deploying

```bash
sudo ./deploy.sh
```

This copies files to `/var/www/reader/` and restarts the `reader.spudooli.com` systemd/gunicorn service.

## Feed update script

Run manually or via cron:

```bash
python3 bin/update-feeds.py
```

Logs to `/tmp/update-feeds.log`.

## Architecture

The app is a Flask package in `reader/`:

- `reader/__init__.py` — App factory: creates Flask app, registers auth blueprint, sets up CSRF protection, loads config
- `reader/main.py` — All main routes (index, stars, read, star, feed-admin, deletefeed, readinglist, about)
- `reader/auth.py` — Auth blueprint (`/auth/login`, `/auth/logout`), `login_required` decorator, session-based auth
- `reader/db.py` — MySQL connection via `flask_mysqldb`, exports `mysql` instance used directly in routes
- `reader/config.py` — Secret key and session cookie config (loaded by `__init__.py` via `app.config.from_pyfile`)
- `config.py` (root) — Development secret key override

Database queries use raw MySQL cursors (no ORM). The `urlhash` MD5 column on `feed_items` prevents duplicate entries.

**Key tables:** `feeds` (feed list), `feed_items` (articles), `users` (single user with hashed password)

## Config

- `reader/config.py` — loaded at runtime, contains `SECRET_KEY` and session cookie settings
- `reader/db.py` — hardcodes MySQL credentials (`root`/`bobthefish`, db `reader`)
- Passwords are hashed with `werkzeug.security.generate_password_hash` and stored in the `users` table

## Frontend design

The UI uses a custom CSS design system in `reader/static/style.css` — no utility framework for layout. Key structure:

- **Layout:** sticky `.site-header` + `.layout-row` (`.sidebar` 25% + `.content-river` flex:1)
- **Fonts:** DM Sans (UI) and DM Mono (dates, counts) — WOFF2 files are self-hosted in `reader/static/dm-*.woff2` with `@font-face` declarations at the top of `style.css`
- **CSS variables:** defined in `:root` — `--bg`, `--sidebar-bg`, `--text`, `--muted`, `--faint`, `--border`, `--link`, `--accent`, `--sans`, `--mono`
- **Secondary pages** (about, readinglist, feed-admin, errors) use `.content-page` wrapper

**Login page** uses the shared Spudooli split-screen design language (same markup/classes as the `negative` and `sitestats` projects: `.loginL` / `.loginR` / `.wm` / `.big` / `.meta` / `.ufield` / `.err`). Light mode only — the other two projects are dark, this one deliberately is not. It suppresses the site header via `{% block chrome %}{% endblock %}` and sets `{% block body_class %}login{% endblock %}`.

**All static assets must be served locally — no external CDN for fonts, JS, or CSS.**

## Frontend interactivity (`reader/static/main.js`)

Reading is driven by a **cursor** over the `.feed-item` articles (`items` / `state` / `readHistory` / `cursor` in `main.js`). Each item is `unread`, `read` (marked read on the server and hidden), or `revealed` (read, but pulled back into view). Articles carry `data-item` and `data-feed` for this.

- `j` — marks the item at the cursor read, hides it, scrolls the next one under the sticky header
- `k` — un-hides the most recently hidden item and puts the cursor back on it. Google Reader style: repeated presses walk further back. The item **stays read on the server** and the sidebar counts do not go back up — revealed items exist only until the next page load, and are never re-fetched from the database
- `getfocus(itemid, feedid)` — click handler on the item body and date; marks read, hides, updates sidebar counts. Clicking below the cursor leaves the cursor alone so `j` still resumes from the top of the river
- `undoRead()` — the undo arrow, now just `k` with a mouse
- `setstar(itemid)` — stars an item (one-way; changes ion-icon name attribute to `star`)

Counts are only decremented when an item moves out of `unread`, so re-reading a revealed item never double-counts. `/stars` renders the same template without a sidebar, so all count updates are null-guarded.
- Ionicons (self-hosted via cdnjs) used for star, undo icons — do not replace with other icon libraries

## Notes

- Dates are stored in NZ timezone (`Pacific/Auckland`)
- Bluesky (`bsky.app`) feed items get oEmbed HTML fetched from `embed.bsky.app`
- CSRF protection is enabled via Flask-WTF on all POST routes
- The `/readinglist` and `/about` routes are public (no login required)
- Feed post HTML content must be rendered as-is — never modify markup inside `.item-body`
