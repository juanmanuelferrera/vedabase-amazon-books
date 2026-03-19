# Interior PDF Generation Guide

Reference for generating KDP-ready interior PDFs with WeasyPrint.

## Critical Architecture Decisions

### CSS @page Rules Location

**IMPORTANT**: All `@page` rules MUST be in the HTML template inline, NOT in external CSS.

**Why**: WeasyPrint's external CSS passed via `stylesheets=[css]` completely overrides inline @page rules. This causes running headers and page configurations to fail silently.

**Solution**: Inject CSS into HTML string instead of passing as external stylesheet:

```python
# In generate_interior.py
css_path = os.path.join(TEMPLATES_DIR, 'interior.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Inject CSS into HTML before </head>
html_with_css = html_content.replace('</head>', f'<style>{css_content}</style></head>')

html = HTML(string=html_with_css, base_url=TEMPLATES_DIR)
html.write_pdf(output_path)
```

### File Responsibilities

| File | Contains | Does NOT Contain |
|------|----------|------------------|
| `book_template.html` | All @page rules (inline `<style>`) | Typography styles |
| `interior.css` | Typography, page assignments, layout | @page rules |

---

## Running Headers Implementation

### How They Work

1. **Define running elements in body**:
```html
<p class="header-left">{{ book_title }}</p>
<p class="header-right">{{ book_title }}</p>
```

2. **Position them as running elements**:
```css
.header-left {
  position: running(headerLeft);
}
.header-right {
  position: running(headerRight);
}
```

3. **Place them in page margins**:
```css
@page :left {
  @top-left {
    content: element(headerLeft);
  }
}
@page :right {
  @top-right {
    content: element(headerRight);
  }
}
```

### Professional Header Positioning

Headers go on the **EXTERIOR** of pages (industry standard):

| Page Type | Header Position | Content |
|-----------|-----------------|---------|
| Left (verso) | Top-left (exterior) | Book title |
| Right (recto) | Top-right (exterior) | Chapter title |

### Updating Chapter Headers

Each chapter updates the right header:
```html
{% for chapter in content %}
<section class="chapter">
  <p class="header-right">{{ chapter.title }}</p>
  <!-- chapter content -->
</section>
{% endfor %}
```

---

## Named Pages

### Page Types

| Named Page | Used For | Headers | Page Numbers |
|------------|----------|---------|--------------|
| `frontmatter` | Half-title, title, copyright, TOC | None | None |
| `chapter-start` | First page of each chapter | None | Yes |
| `backmatter` | Glossary, about author | None | Yes |
| `:blank` | Auto-inserted blank pages | None | None |
| `:first` | Very first page of document | None | None |

### CSS Assignments

In `interior.css`:
```css
.half-title, .series-page, .title-page, .copyright-page, .toc, .publishers-note {
  page: frontmatter;
}

.chapter {
  page-break-before: right;
}

.chapter-header {
  page: chapter-start;
  page-break-after: avoid;
}

.glossary, .about-author, .series-info {
  page: backmatter;
}
```

### @page Definitions

In `book_template.html` inline styles:
```css
@page frontmatter {
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-center { content: none; }
}

@page chapter-start {
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-center {
    content: counter(page);
    font-size: 10pt;
  }
}

@page backmatter {
  @top-left { content: none; }
  @top-right { content: none; }
}

@page :blank {
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-center { content: none; }
}
```

---

## KDP Requirements

### Minimum Pages
- **Minimum**: 24 pages
- **Maximum**: 828 pages

### Margins for 6x9 Format

```css
@page :left {
  margin-left: 0.5in;    /* Inside (gutter) */
  margin-right: 0.75in;  /* Outside */
  margin-top: 0.75in;
  margin-bottom: 0.75in;
}

@page :right {
  margin-left: 0.75in;   /* Inside (gutter) */
  margin-right: 0.5in;   /* Outside */
  margin-top: 0.75in;
  margin-bottom: 0.75in;
}
```

**Note**: Inside margins (gutter) are SMALLER because the spine binding takes space.

### Page Size

```css
@page {
  size: 6in 9in;
}
```

---

## Troubleshooting

### Headers Not Appearing

1. Check that @page rules are in HTML inline, not external CSS
2. Verify running elements exist in body before content
3. Confirm `position: running()` is applied to header elements
4. Check browser console for CSS errors

### Headers on Wrong Pages

1. Verify named page assignments in CSS
2. Check that `page:` property is set on correct elements
3. Ensure `@page pagename` has `content: none` for headers

### Margins Look Wrong

1. Remember: inside margin = gutter side (near spine)
2. Left pages: margin-left is inside
3. Right pages: margin-left is inside
4. Inside margins should be smaller than outside

---

## Generation Command

```bash
source venv/bin/activate && python generate_interior.py BOOK_ID
```

Example:
```bash
python generate_interior.py I-01  # Raja-vidya
```

Output:
- HTML: `output/interiors/BOOK_ID_interior.html`
- PDF: `output/interiors/BOOK_ID_interior.pdf`
