# Handoff: Spudooli Feed Reader — Design Refresh

## Overview

This is a visual design refresh of an existing Python Flask RSS feed reader application. There is **no new functionality** — the task is purely a template and CSS update. The existing app structure, routes, and Python logic remain completely unchanged. Only the HTML templates and stylesheet need to be updated to match this design.

## About the Design File

`Feed Reader Refresh v2.html` is a **high-fidelity design reference** built in plain HTML/CSS. It is not production code to copy directly — it is a mockup showing the exact intended look and behaviour of the refreshed UI. Your task is to recreate this design within the existing Flask/Jinja2 template structure, replacing the current CSS and template markup while preserving all existing template variables, loops, and logic.

## Fidelity

**High-fidelity.** This is a pixel-accurate mockup with final colours, typography, spacing, and interactions. Implement it as close to pixel-perfect as possible using the values documented below.

---

## External Dependencies to Add

These replace or supplement whatever is currently loaded. Add to your base template `<head>`:

```html
<!-- Google Fonts: DM Sans + DM Mono -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300;1,9..40,400&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">

<!-- Bootstrap 5.3.3 (keep if already present, just confirm version) -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Ionicons 7.4.0 (for star icon on feed items) -->
<script type="module" src="https://unpkg.com/ionicons@7.4.0/dist/ionicons/ionicons.esm.js"></script>
<script nomodule src="https://unpkg.com/ionicons@7.4.0/dist/ionicons/ionicons.js"></script>
```

---

## Design Tokens

Put these CSS custom properties in your main stylesheet, on `:root`:

```css
:root {
  --bg:         #ffffff;
  --sidebar-bg: #f7f8fa;
  --text:       #18181b;
  --muted:      #71717a;
  --faint:      #a1a1aa;
  --border:     #e4e4e7;
  --link:       #1d4ed8;
  --accent:     #1d4ed8;
  --mono:       'DM Mono', monospace;
  --sans:       'DM Sans', sans-serif;
  --body-size:  15px;
  --body-lh:    1.7;
}
```

---

## Global Base Styles

```css
*, *::before, *::after { box-sizing: border-box; }

html, body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  font-size: var(--body-size);
  line-height: var(--body-lh);
  -webkit-font-smoothing: antialiased;
}

a { color: var(--link); }
a:hover { color: var(--link); }
```

---

## Layout

The page uses a full-width sticky header, then a centred container with a flex row of sidebar + content river.

### Container

```css
.site-container {
  max-width: 1320px;   /* Bootstrap container-xxl */
  margin: 0 auto;
}
```

### Layout row (sidebar + content)

```css
.layout-row {
  display: flex;
  min-height: calc(100vh - 56px);
}
```

**Jinja template structure:**

```html
<header class="site-header">
  <div class="site-container">
    <!-- brand + nav -->
  </div>
</header>

<div class="site-container">
  <div class="layout-row">
    <aside class="sidebar"><!-- sidebar content --></aside>
    <main class="content-river"><!-- feed items --></main>
  </div>
</div>
```

---

## Site Header

The header is sticky, full viewport width border-bottom, content centred at 1320px.

```css
.site-header {
  border-bottom: 1px solid var(--border);
  min-height: 56px;
  background: var(--bg);
  position: sticky;
  top: 0;
  z-index: 100;
}

.site-header .site-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 72px;
  padding: 0 2rem;
  flex-wrap: wrap;
  gap: 8px;
}

.site-header .brand {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 40px;
  letter-spacing: -0.03em;
  color: var(--text);
  text-decoration: none;
  white-space: nowrap;
  line-height: 1;
}

.site-header nav a {
  font-family: var(--sans);
  font-size: 15px;
  color: var(--link);
  text-decoration: none;
  margin-left: 28px;
}

.site-header nav a.active {
  color: var(--text);
  font-weight: 500;
}

.site-header nav a:hover {
  text-decoration: underline;
}
```

**Template markup:**

```html
<header class="site-header">
  <div class="site-container">
    <a href="{{ url_for('index') }}" class="brand">Spudooli Feed Reader</a>
    <nav>
      <a href="{{ url_for('index') }}" class="{% if active_page == 'read' %}active{% endif %}">Read</a>
      <a href="{{ url_for('about') }}" class="{% if active_page == 'about' %}active{% endif %}">About</a>
      <a href="{{ url_for('reading_list') }}" class="{% if active_page == 'reading_list' %}active{% endif %}">Reading List</a>
    </nav>
  </div>
</header>
```

---

## Sidebar (col-sm-3 / 25%)

```css
.sidebar {
  width: 25%;
  flex-shrink: 0;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  padding: 40px 32px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.sidebar-count {
  font-family: var(--sans);
  font-size: 40px;
  font-weight: 300;
  letter-spacing: -0.04em;
  color: var(--text);
  line-height: 1;
  margin-bottom: 2px;
}

.sidebar-label {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 28px;
}

.feed-list {
  list-style: none;
  padding: 0;
  margin: 0 0 32px 0;
}

.feed-list li {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 7px 0;
  border-bottom: 1px solid var(--border);
}

.feed-list li:first-child {
  border-top: 1px solid var(--border);
}

.feed-name {
  font-family: var(--sans);
  font-size: 13.5px;
  color: var(--text);
}

.feed-count {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--faint);
  font-weight: 400;
  min-width: 18px;
  text-align: right;
}

.feed-count.has-items {
  color: var(--accent);
  font-weight: 500;
}

.sidebar-links {
  border-top: 1px solid var(--border);
  padding-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: auto;
}

.sidebar-links a {
  font-family: var(--sans);
  font-size: 13.5px;
  color: var(--link);
  text-decoration: none;
}

.sidebar-links a:hover { text-decoration: underline; }

.sidebar-footer {
  margin-top: 40px;
  font-family: var(--sans);
  font-size: 11.5px;
  color: var(--faint);
  line-height: 1.8;
}

.sidebar-footer a {
  color: var(--link);
  text-decoration: none;
}
```

**Template markup** (adapt variable names to match your existing Flask context):

```html
<aside class="sidebar">
  <div class="sidebar-count">{{ feeds | length }}</div>
  <div class="sidebar-label">Feeds</div>

  <ul class="feed-list">
    {% for feed in feeds %}
    <li>
      <span class="feed-name">{{ feed.name }}</span>
      <span class="feed-count {% if feed.unread_count > 0 %}has-items{% endif %}">
        {{ feed.unread_count }}
      </span>
    </li>
    {% endfor %}
  </ul>

  <div class="sidebar-links">
    <a href="{{ url_for('stars') }}">Stars</a>
    <a href="{{ url_for('feeds_admin') }}">Feeds Admin</a>
  </div>

  <div class="sidebar-footer">
    <div>© Copyright {{ now.year }}</div>
    <a href="#">Spudooli Investments Ltd</a>
  </div>
</aside>
```

---

## Content River (col-sm-9 / 75%)

```css
.content-river {
  flex: 1;
  padding: 0 48px 80px 48px;
}
```

---

## Feed Item

Each post in the river is an `<article class="feed-item">`. The item chrome (source label, date, star button, title) is designed. The post body is rendered as raw feed HTML — do not restructure it, just wrap it in `.item-body`.

```css
.feed-item {
  padding: 28px 0;
  border-bottom: 1px solid var(--border);
}

/* ── Meta row: source label left, date + star right ── */
.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  gap: 12px;
  flex-wrap: nowrap;
}

.item-source {
  display: flex;
  align-items: center;
  gap: 7px;
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--muted);
  flex-shrink: 0;
  white-space: nowrap;
}

.item-source img.favicon {
  width: 14px;
  height: 14px;
  border-radius: 2px;
  object-fit: contain;
}

.item-source .favicon-placeholder {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--border);
  flex-shrink: 0;
}

.item-right {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.item-date {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--faint);
  letter-spacing: 0.01em;
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Star button ── */
.star-btn {
  background: none;
  border: 1px solid var(--border);
  border-radius: 4px;
  cursor: pointer;
  padding: 3px 6px;
  color: var(--faint);
  font-size: 16px;
  line-height: 1;
  transition: color 0.15s, border-color 0.15s;
  display: flex;
  align-items: center;
}

.star-btn:hover {
  color: var(--accent);
  border-color: var(--accent);
}

.star-btn.starred {
  color: var(--accent);
  border-color: var(--accent);
}

.star-btn ion-icon {
  display: block;
  font-size: 15px;
}

/* ── Post title (linked) ── */
.item-title {
  font-family: var(--sans);
  font-weight: 500;
  font-size: 17px;
  line-height: 1.3;
  letter-spacing: -0.01em;
  margin-bottom: 10px;
}

.item-title a {
  color: var(--link);
  text-decoration: none;
}

.item-title a:hover {
  text-decoration: underline;
}

/* ── Post body: raw feed HTML, minimal overrides only ── */
.item-body {
  font-family: var(--sans);
  font-size: var(--body-size);
  line-height: var(--body-lh);
  color: var(--text);
}

.item-body p               { margin-bottom: 0.75em; }
.item-body p:last-child    { margin-bottom: 0; }
.item-body a               { color: var(--link); }
.item-body blockquote {
  margin: 1em 0;
  padding-left: 1.1em;
  border-left: 3px solid var(--border);
  color: var(--muted);
  font-style: italic;
}
.item-body blockquote p    { margin-bottom: 0.5em; }
.item-body ul, .item-body ol { padding-left: 1.4em; margin-bottom: 0.75em; }
.item-body img             { max-width: 100%; height: auto; border-radius: 4px; margin: 0.5em 0; }
.item-body audio           { width: 100%; margin: 0.5em 0; }
.item-body strong          { font-weight: 600; }
.item-body code {
  font-family: var(--mono);
  font-size: 0.88em;
  background: var(--sidebar-bg);
  padding: 0.1em 0.35em;
  border-radius: 3px;
}
.item-body pre {
  background: var(--sidebar-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1em;
  overflow-x: auto;
  font-family: var(--mono);
  font-size: 0.88em;
  margin-bottom: 0.75em;
}
```

**Template markup** for a single feed item (adapt variable names to your existing context):

```html
<article class="feed-item">
  <div class="item-meta">
    <span class="item-source">
      {% if item.feed.favicon_url %}
        <img class="favicon" src="{{ item.feed.favicon_url }}" alt="">
      {% else %}
        <span class="favicon-placeholder"></span>
      {% endif %}
      {{ item.feed.name }}
    </span>
    <div class="item-right">
      <span class="item-date">{{ item.published | format_datetime }}</span>
      <button
        class="star-btn {% if item.starred %}starred{% endif %}"
        onclick="this.classList.toggle('starred'); this.querySelector('ion-icon').name = this.classList.contains('starred') ? 'star' : 'star-outline'; /* call your existing star toggle endpoint here */"
        title="Star this item"
      >
        <ion-icon name="{% if item.starred %}star{% else %}star-outline{% endif %}"></ion-icon>
      </button>
    </div>
  </div>

  {% if item.title %}
  <h2 class="item-title">
    <a href="{{ item.url }}" target="_blank" rel="noopener">{{ item.title }}</a>
  </h2>
  {% endif %}

  <!-- Feed body: render raw HTML exactly as delivered by the feed -->
  <div class="item-body">
    {{ item.content | safe }}
  </div>
</article>
```

---

## Star Button — Wiring to Existing Endpoint

The mockup shows a client-side class toggle for demo purposes. In your Flask app, wire it to your existing star/unstar endpoint (whatever it currently is). A minimal approach that keeps the visual toggle snappy:

```javascript
function toggleStar(btn, itemId) {
  btn.classList.toggle('starred');
  const icon = btn.querySelector('ion-icon');
  icon.name = btn.classList.contains('starred') ? 'star' : 'star-outline';

  // Call your existing endpoint — adapt URL/method to match your current implementation
  fetch(`/items/${itemId}/star`, { method: 'POST' });
}
```

Then update the button's `onclick`:

```html
<button class="star-btn {% if item.starred %}starred{% endif %}"
  onclick="toggleStar(this, {{ item.id }})"
  title="Star this item">
  <ion-icon name="{% if item.starred %}star{% else %}star-outline{% endif %}"></ion-icon>
</button>
```

---

## Assets / Icons

- **Star icon**: Ionicons `star` (filled) and `star-outline` (empty). Loaded via CDN — no local asset needed.
- **Favicons**: Loaded from each feed's existing favicon URL. No change to how these are fetched.
- No other image assets are part of this design.

---

## What Does NOT Change

- All Flask routes and view functions
- All Python business logic
- Database models and queries  
- Feed fetching / parsing logic
- The star/unstar endpoint behaviour
- The Reading List, About, Stars, and Feeds Admin page logic
- Any existing Jinja2 template variables — just the markup wrapping them

---

## Files in This Package

| File | Purpose |
|---|---|
| `README.md` | This document |
| `Feed Reader Refresh v2.html` | Full high-fidelity design reference — open in a browser to see the intended result |
