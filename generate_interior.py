#!/usr/bin/env python3
"""
Vedabase Original Edition - Interior PDF Generator
Converts book content to KDP-ready PDF interiors
"""

import os
import re
import yaml
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
BOOKS_DIR = os.path.join(BASE_DIR, 'books')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'interiors')

# Series books list for series page
SERIES_BOOKS = [
    "Bhagavad-gita As It Is",
    "Srimad-Bhagavatam",
    "Sri Caitanya-caritamrta",
    "Krsna, the Supreme Personality of Godhead",
    "The Nectar of Devotion",
    "The Nectar of Instruction",
    "Sri Isopanisad",
    "Teachings of Lord Caitanya",
    "Teachings of Lord Kapila",
    "Teachings of Queen Kunti",
    "Raja-vidya: The King of Knowledge",
    "The Path of Perfection",
    "Perfect Questions, Perfect Answers",
    "The Perfection of Yoga",
    "Beyond Birth and Death",
    "Easy Journey to Other Planets",
    "Life Comes from Life",
    "The Science of Self-Realization",
]


def parse_verse_block(content):
    """Parse Sanskrit verse blocks into structured HTML"""
    # Pattern for verse numbers like "TEXT 1" or "VERSE 1"
    verse_pattern = r'(?:TEXT|VERSE)\s+(\d+)'

    # Split content by verse markers
    parts = re.split(verse_pattern, content)

    if len(parts) <= 1:
        return content

    html_parts = []
    i = 0
    while i < len(parts):
        if i == 0 and parts[i].strip():
            html_parts.append(parts[i])
            i += 1
        elif i + 1 < len(parts):
            verse_num = parts[i]
            verse_content = parts[i + 1] if i + 1 < len(parts) else ""

            # Try to identify parts of the verse
            html = format_verse(verse_num, verse_content)
            html_parts.append(html)
            i += 2
        else:
            i += 1

    return '\n'.join(html_parts)


def format_verse(verse_num, content):
    """Format a single verse with its components"""
    html = f'<div class="verse-block">\n'
    html += f'  <p class="verse-number">TEXT {verse_num}</p>\n'

    # Try to identify Sanskrit, synonyms, translation, purport
    lines = content.strip().split('\n')

    sanskrit_lines = []
    synonyms_lines = []
    translation_lines = []
    purport_lines = []

    current_section = 'sanskrit'

    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # Remove markdown bold markers
        line_clean = line_stripped.replace('**', '').replace('__', '')
        line_lower_clean = line_clean.lower()

        if line_lower_clean.startswith('synonyms') or line_lower_clean.startswith('word for word'):
            current_section = 'synonyms'
            continue
        elif line_lower_clean.startswith('translation'):
            current_section = 'translation'
            continue
        elif line_lower_clean.startswith('purport'):
            current_section = 'purport'
            continue

        # Clean the line of markdown artifacts
        line_output = line_stripped.replace('**', '').replace('__', '')

        if current_section == 'sanskrit':
            sanskrit_lines.append(line_output)
        elif current_section == 'synonyms':
            synonyms_lines.append(line_output)
        elif current_section == 'translation':
            translation_lines.append(line_output)
        elif current_section == 'purport':
            purport_lines.append(line_output)

    if sanskrit_lines:
        sanskrit_text = " ".join([l for l in sanskrit_lines if l])
        if sanskrit_text.strip():
            html += f'  <div class="sanskrit">{sanskrit_text}</div>\n'

    if synonyms_lines:
        synonyms_text = " ".join([l for l in synonyms_lines if l])
        if synonyms_text.strip():
            html += f'  <div class="synonyms">{synonyms_text}</div>\n'

    if translation_lines:
        translation_text = " ".join([l for l in translation_lines if l])
        if translation_text.strip():
            html += f'  <div class="translation">{translation_text}</div>\n'

    if purport_lines:
        html += f'  <p class="purport-header">PURPORT</p>\n'
        html += f'  <div class="purport">\n'
        for para in purport_lines:
            if para.strip():
                html += f'    <p>{para}</p>\n'
        html += f'  </div>\n'

    html += '</div>\n'
    return html


def detect_sanskrit_verses(html):
    """Detect and wrap Sanskrit verse blocks for tighter line spacing"""
    # Pattern to match diacritics in Sanskrit transliteration
    diacritic_pattern = r'[āīūṛṝḷḹēōṃḥṅñṭḍṇśṣĀĪŪṚṜḶḸĒŌṂḤṄÑṬḌṆŚṢ]'

    lines = html.split('\n')
    result = []
    verse_buffer = []
    in_verse = False

    for line in lines:
        # Check if this is a short paragraph
        if line.startswith('<p>') and line.endswith('</p>'):
            content = line[3:-4].strip()
            has_diacritics = bool(re.search(diacritic_pattern, content))
            is_short = len(content) < 60
            no_period = not content.endswith('.')
            # Check if looks like verse (short, no period, no quotes at start)
            looks_like_verse = is_short and no_period and not content.startswith('"')

            # Start verse if has diacritics
            if has_diacritics and looks_like_verse:
                if not in_verse:
                    in_verse = True
                    verse_buffer = []
                verse_buffer.append(content)
                continue
            # Continue verse if already in one and line looks like verse
            elif in_verse and looks_like_verse and len(content) > 10:
                verse_buffer.append(content)
                continue

        # If we were in a verse and now we're not, flush the buffer
        if in_verse:
            if len(verse_buffer) >= 2:
                result.append(format_verse_block(verse_buffer))
            else:
                for v in verse_buffer:
                    result.append(f'<p>{v}</p>')
            verse_buffer = []
            in_verse = False

        result.append(line)

    # Flush any remaining verse buffer
    if in_verse and verse_buffer:
        if len(verse_buffer) >= 2:
            result.append(format_verse_block(verse_buffer))
        else:
            for v in verse_buffer:
                result.append(f'<p>{v}</p>')

    return '\n'.join(result)


def format_verse_block(verses):
    """Format verse block, splitting into stanzas of 4 lines if needed"""
    if len(verses) <= 4:
        html = '<div class="sanskrit-verse">\n'
        for v in verses:
            html += f'  <p>{v}</p>\n'
        html += '</div>'
        return html
    else:
        # Split into stanzas of 4 lines
        html = '<div class="sanskrit-verse">\n'
        for i, v in enumerate(verses):
            html += f'  <p>{v}</p>\n'
            # Add stanza break after every 4 lines (except at the end)
            if (i + 1) % 4 == 0 and i + 1 < len(verses):
                html += '  <p class="stanza-break"></p>\n'
        html += '</div>'
        return html


def markdown_to_html(md_content):
    """Convert markdown content to HTML"""
    import markdown

    # Convert markdown to HTML
    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # Process verse blocks if present
    html = parse_verse_block(html)

    # Detect and wrap Sanskrit verses
    html = detect_sanskrit_verses(html)

    return html


def load_book_content(book_path):
    """Load book content from markdown or HTML files"""
    chapters = []

    # Check for content.md or individual chapter files
    content_file = os.path.join(book_path, 'content.md')

    if os.path.exists(content_file):
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by H1 headers (# Chapter...)
        # Pattern: lines starting with single # followed by space
        lines = content.split('\n')
        current_chapter = None
        current_body = []

        for line in lines:
            # Check if this is a chapter header (# Chapter X: Title)
            if line.startswith('# ') and not line.startswith('## '):
                # Save previous chapter if exists
                if current_chapter is not None:
                    current_chapter['body'] = markdown_to_html('\n'.join(current_body))
                    chapters.append(current_chapter)

                # Parse the header
                header = line[2:].strip()  # Remove "# "

                # Try to extract chapter number and title
                # Pattern: "Chapter 1: Title" or "Chapter 1 Title" or just "Title"
                match = re.match(r'Chapter\s+(\d+)[:\s]*(.+)', header, re.IGNORECASE)
                if match:
                    chapter_num = int(match.group(1))
                    title = match.group(2).strip()
                else:
                    chapter_num = len(chapters) + 1
                    title = header

                current_chapter = {
                    'number': chapter_num,
                    'title': title,
                    'subtitle': None,
                    'body': ''
                }
                current_body = []
            elif current_chapter is not None:
                current_body.append(line)

        # Don't forget the last chapter
        if current_chapter is not None:
            current_chapter['body'] = markdown_to_html('\n'.join(current_body))
            chapters.append(current_chapter)

    else:
        # Look for individual chapter files
        chapter_files = sorted([f for f in os.listdir(book_path)
                               if f.startswith('chapter') and f.endswith('.md')])

        for i, cf in enumerate(chapter_files, 1):
            with open(os.path.join(book_path, cf), 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract title from first line
            lines = content.split('\n')
            title = lines[0].lstrip('#').strip() if lines else f"Chapter {i}"
            body = '\n'.join(lines[1:]) if len(lines) > 1 else ""

            chapters.append({
                'number': i,
                'title': title,
                'subtitle': None,
                'body': markdown_to_html(body)
            })

    return chapters


def load_book_metadata(book_path):
    """Load book metadata from YAML file"""
    meta_file = os.path.join(book_path, 'metadata.yaml')

    if os.path.exists(meta_file):
        with open(meta_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    # Default metadata
    return {
        'title': os.path.basename(book_path).replace('_', ' ').title(),
        'subtitle': None,
        'first_edition_year': '1972',
        'glossary': []
    }


def generate_interior_pdf(book_id, book_path, output_path):
    """Generate KDP-ready interior PDF for a book"""

    # Load metadata and content
    metadata = load_book_metadata(book_path)
    chapters = load_book_content(book_path)

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template('book_template.html')

    # Build TOC
    toc = []
    for i, ch in enumerate(chapters, 1):
        toc.append({
            'number': ch.get('number', i),
            'title': ch['title'],
            'page': ''  # Page numbers added by PDF renderer
        })

    # Render HTML
    html_content = template.render(
        book_title=metadata.get('title', 'Untitled'),
        subtitle=metadata.get('subtitle'),
        first_edition_year=metadata.get('first_edition_year', '1972'),
        current_year=datetime.now().year,
        series_books=SERIES_BOOKS,
        chapters=toc,
        content=chapters,
        glossary=metadata.get('glossary', [])
    )

    # Save HTML for debugging
    html_path = output_path.replace('.pdf', '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML saved: {html_path}")

    # Generate PDF with WeasyPrint
    css_path = os.path.join(TEMPLATES_DIR, 'interior.css')

    html = HTML(string=html_content, base_url=TEMPLATES_DIR)
    css = CSS(filename=css_path)

    html.write_pdf(output_path, stylesheets=[css])
    print(f"PDF generated: {output_path}")

    return output_path


def create_sample_book():
    """Create a sample book structure for testing"""
    sample_dir = os.path.join(BOOKS_DIR, 'introductory', 'I-01_raja_vidya')
    os.makedirs(sample_dir, exist_ok=True)

    # Create metadata
    metadata = {
        'title': 'Raja-vidya',
        'subtitle': 'The King of Knowledge',
        'first_edition_year': '1973',
        'series_id': 'I-01',
        'category': 'introductory',
        'glossary': [
            {'term': 'Bhagavad-gita', 'definition': 'The Song of God, spoken by Lord Krishna'},
            {'term': 'Krishna', 'definition': 'The Supreme Personality of Godhead'},
            {'term': 'Raja-vidya', 'definition': 'The king of knowledge'},
        ]
    }

    meta_path = os.path.join(sample_dir, 'metadata.yaml')
    with open(meta_path, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True)

    # Create sample content
    content = """# Chapter 1: Knowledge Beyond Samsara

This is sample content for Raja-vidya Chapter 1.

The Bhagavad-gita teaches us about the eternal soul and its relationship with the Supreme.

## TEXT 1

raja-vidya raja-guhyam
pavitram idam uttamam
pratyakshavagamam dharmyam
su-sukham kartum avyayam

**SYNONYMS**

raja-vidya—the king of education; raja-guhyam—the king of confidential knowledge; pavitram—the purest; idam—this; uttamam—transcendental.

**TRANSLATION**

This knowledge is the king of education, the most secret of all secrets. It is the purest knowledge, and because it gives direct perception of the self by realization, it is the perfection of religion.

**PURPORT**

This chapter of Bhagavad-gita is called the king of education because it is the essence of all doctrines and philosophies explained before.

In India there are many systems of philosophy, and whenever there is a philosophical presentation, it is called a darsana. The Bhagavad-gita is called the culmination of all darsanas.

# Chapter 2: The Eternal Soul

This chapter discusses the nature of the eternal soul.

The soul is never born, and it never dies. It is eternal, ever-existing, and primeval.
"""

    content_path = os.path.join(sample_dir, 'content.md')
    with open(content_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Sample book created at: {sample_dir}")
    return sample_dir


if __name__ == '__main__':
    import sys

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if len(sys.argv) > 1:
        book_id = sys.argv[1]
        # Find book path
        for category in ['introductory', 'essential', 'teachings', 'major_works', 'lectures']:
            cat_dir = os.path.join(BOOKS_DIR, category)
            if os.path.exists(cat_dir):
                for book_dir in os.listdir(cat_dir):
                    if book_id.lower() in book_dir.lower():
                        book_path = os.path.join(cat_dir, book_dir)
                        output_path = os.path.join(OUTPUT_DIR, f"{book_id}_interior.pdf")
                        generate_interior_pdf(book_id, book_path, output_path)
                        sys.exit(0)

        print(f"Book not found: {book_id}")
    else:
        # Use existing Raja-vidya if it exists
        sample_path = os.path.join(BOOKS_DIR, 'introductory', 'I-01_raja_vidya')
        content_file = os.path.join(sample_path, 'content.md')

        if not os.path.exists(content_file):
            print("Creating sample book...")
            sample_path = create_sample_book()
        else:
            print("Using existing Raja-vidya content...")

        output_path = os.path.join(OUTPUT_DIR, "I-01_raja_vidya_interior.pdf")
        generate_interior_pdf("I-01", sample_path, output_path)

        print("\nDone! Run with book ID to generate specific book:")
        print("  python generate_interior.py I-01")
