# HabiVox website

Static site: `index.html`, `privacy.html`, `terms.html`, `delete-account.html`.
No framework, no JavaScript apart from closing the mobile menu.

## Editing

Edit the files in `src/`, then run:

```
python build.py
```

The build adds the shared header, footer, `<head>` and Lucide icons, and stops
if it finds an em dash, an en dash or an unfilled placeholder.

Design rules used:
- Font: Inter (matches the app's system font), from Google Fonts
- Colors from the app: orange `#F97316` and gray-900 `#111827`, with white and `#F9FAFB` surfaces
- One button style (`.btn`), one icon set (Lucide), 12-column grid, 8px spacing scale

## Preview locally

```
python -m http.server 4321 --directory habivox-site
```

## Launch checklist

- [ ] Buy the domain and connect it in Vercel (project root: `habivox-site`)
- [ ] Set `SITE_URL` in `build.py` to the domain, then `python build.py`
      (adds canonical URLs, the social preview image, `sitemap.xml`, `robots.txt`)
- [ ] Testimonials: add only real ones, with a link to the source
- [ ] Play Console: set Privacy Policy to `https://<domain>/privacy` and the
      account deletion URL to `https://<domain>/delete-account`
- [ ] Play Console: update the Data safety form for AI features and usage analytics

Favicon, app icons and the social image are already in `assets/`.
There is no "Made with" badge anywhere.
