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
- **Secondary pages** (about, readinglist, feed-admin, login, errors) use `.content-page` wrapper

**All static assets must be served locally — no external CDN for fonts, JS, or CSS.**

## Frontend interactivity (`reader/static/main.js`)

- `getfocus(itemid, feedid)` — marks item read, hides it, updates sidebar counts, enables undo
- `undoRead()` — reverses the last read action
- `setstar(itemid)` — stars an item (one-way; changes ion-icon name attribute to `star`)
- Ionicons (self-hosted via cdnjs) used for star, undo icons — do not replace with other icon libraries

## Notes

- Dates are stored in NZ timezone (`Pacific/Auckland`)
- Bluesky (`bsky.app`) feed items get oEmbed HTML fetched from `embed.bsky.app`
- CSRF protection is enabled via Flask-WTF on all POST routes
- The `/readinglist` and `/about` routes are public (no login required)
- Feed post HTML content must be rendered as-is — never modify markup inside `.item-body`
