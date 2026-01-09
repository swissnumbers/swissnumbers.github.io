# Copilot Instructions for Minima Theme

## Project Overview

**Minima** is Jekyll's default theme (v3.0.0-dev) - a minimal, elegant blogging theme distributed as a Ruby gem. This is the core theme package that users install via Gemfile or `jekyll-remote-theme` plugin, not a user site.

### Key Architecture

The theme follows a component-based Jekyll layout system with pluggable color skins:

```
base.html (root layout)
  ├─ head.html (includes: custom-head, google-analytics)
  ├─ header.html (navigation)
  ├─ footer.html (social links via include)
  └─ sub-footer.html

home.html, post.html, page.html (extend base)
```

## Critical Workflows

### Development & Testing

- **Local preview**: `script/server` → runs `bundle exec jekyll serve --config _config_theme-dev.yml`
- **Build example site**: `script/build` → compiles to `_site/` using dev config
- **Config**: `_config_theme-dev.yml` enables testing theme against example posts/pages

### Theme Packaging

- **Gemspec** (`minima.gemspec`): Defines gem metadata, runtime deps (jekyll ≥3.5 <5.0, jekyll-feed, jekyll-seo-tag)
- **Gem distribution**: Uses `git ls-files` to package only `assets/`, `_includes/`, `_layouts/`, `_sass/`, and license/readme
- **Version**: Currently `3.0.0.dev` - breaking changes from v2.x (see `base.html` vs old `default.html`)

## Project Conventions & Patterns

### Layout Hierarchy (Liquid)

1. **base.html**: Universal structure (doctype, head, body, wrapper). All layouts inherit via `layout: base`
2. **Specific layouts** extend with content-specific markup:
   - `post.html`: Article semantics (h-entry, schema.org), publish/update dates, author support
   - `home.html`: Posts list + paginator support, optional title/excerpt
   - `page.html`: Simple content wrapper for non-blog pages

### Styling Architecture (SCSS)

- **initialize.scss**: Defines spacing unit ($30px), typography defaults, media queries
- **_base.scss**: Resets, global typography, flexbox body (min-height: 100vh, flex-column)
- **_layout.scss**: Component styles (.wrapper, .site-header, .site-nav, .post-list, etc.)
- **custom-variables.scss & custom-styles.scss**: User overrides (color, fonts)
- **Skins**: 6 selectable color schemes (auto, classic, dark, solarized variants) in `_sass/minima/skins/`
- **Skin selection**: Via `minima.skin` config key (default: auto)

### Frontend Features

- **Responsive nav**: Checkbox-toggle pattern (no JS) in `header.html` with label targeting #nav-trigger
- **Font Awesome CDN**: Loaded via footer link for social icons (v7.0.0)
- **h-cards & schema.org**: Post/author microdata for SEO and feed aggregation
- **Jekyll SEO Tag & Feed**: Auto-included via plugins for meta tags & Atom feed

### Content Configuration (Front Matter)

**Posts** (`_posts/YYYY-MM-DD-title.md`):
- `layout: post` (auto-detected by Jekyll)
- `title`, `author` (string or array), `date`, `modified_date` (optional)
- `date_format` override via front matter or site config

**Pages**:
- `layout: page` or custom
- Optional `title` for explicit heading

**Home page** (`index.md`):
- `layout: home`
- Optional `title` for explicit main heading
- `list_title` to customize "Posts" section heading
- Content before post list supported (since v2.2)

## Key Files & Examples

| File | Purpose |
|------|---------|
| [_includes/header.html](_includes/header.html) | Nav with responsive checkbox pattern |
| [_layouts/post.html](_layouts/post.html) | Post semantics, date/author display |
| [_sass/minima/initialize.scss](_sass/minima/initialize.scss) | Spacing, typography, viewport breakpoints |
| [_sass/minima/skins/dark.scss](_sass/minima/skins/dark.scss) | Color scheme overrides |
| [assets/css/style.scss](assets/css/style.scss) | Main SCSS import chain |
| [_config.yml](_config.yml) | All config options documented with examples |

## Development Notes

- **Breaking change in v3**: Renamed `default.html` → `base.html` (backward compat: create `default.html` wrapping `base.html`)
- **Environment-specific**: Production GA only (`jekyll.environment == 'production'`)
- **Mobile-first media queries**: Use `max-width` (desktop-first legacy approach in some mixins)
- **Defaults**: Most SCSS vars use `!default` for user overrides
- **Liquid filters**: Post date format customizable via site/page front matter
- **Remote theme support**: Can be used via `jekyll-remote-theme` plugin by pointing to specific git ref (encouraged over master HEAD)

## Testing & Validation

When modifying layouts/styles:
1. Build example site: `script/build`
2. Check `_site/` output for markup structure
3. Test responsive nav on mobile breakpoint ($on-palm: 600px)
4. Verify skin switching works (check `_sass/minima/skins/` imports)
5. Ensure all includes still render (`custom-head.html`, `social.html`, etc.)
