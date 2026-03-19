# Vedabase Original Edition - Amazon Book Collection

Professional book publishing system for creating KDP-ready interiors from [vedabase.bhaktiyoga.es](https://vedabase.bhaktiyoga.es) content.

## Features

- **6x9 interior PDFs** - KDP-ready format with professional typography
- **Sanskrit verse detection** - Automatic formatting with proper line spacing
- **Penguin Classics style** - EB Garamond, proper margins, professional layout
- **Multi-book support** - Process entire catalog systematically

## Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install weasyprint jinja2 markdown pyyaml

# Generate interior PDF
python generate_interior.py I-01
```

## Project Structure

```
amazon_books/
├── templates/
│   ├── interior.css          # Interior styling (6x9)
│   ├── book_template.html    # Jinja2 template
│   └── publishers_note*.md   # Publisher's note EN/ES
├── books/
│   └── [category]/[book_id]/
│       ├── content.md        # Book content
│       └── metadata.yaml     # Book metadata
├── generate_interior.py      # Interior PDF generator
├── generate_covers.py        # Cover generator
├── convert_vedabase.py       # Vedabase format converter
├── inventory.yaml            # Book catalog
└── pricing_guide.md          # KDP pricing reference
```

## Workflow

1. **Download** content from vedabase.bhaktiyoga.es
2. **Convert** using `convert_vedabase.py`
3. **Generate** interior with `generate_interior.py`
4. **Upload** to Amazon KDP

## Typography

- **Body**: EB Garamond 11pt
- **Format**: 6x9 inches
- **Margins**: Inside 0.75", Outside 0.5", Top/Bottom 0.75"

## Series

| Category | Code | Example |
|----------|------|---------|
| Introductory | I-XX | I-01 Raja-vidya |
| Essential | ET-XX | ET-01 Nectar of Devotion |
| Teachings | T-XX | T-01 Teachings of Lord Kapila |
| Major Works | MW-XX | MW-01 Bhagavad-gita |

## License

Content published under license from Krishna Books Inc.
Original unrevised editions.

---

*"The words he chose. Unchanged. Unedited."*
