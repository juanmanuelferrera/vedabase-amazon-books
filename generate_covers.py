#!/usr/bin/env python3
"""
Vedabase Original Edition - Cover Generator
Generates minimalist book covers in the style of Penguin Classics
For Amazon KDP 6x9 format
"""

from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# KDP 6x9 cover dimensions (with bleed)
# Cover: 6.125" x 9.25" at 300 DPI
COVER_WIDTH = 1838  # 6.125 * 300
COVER_HEIGHT = 2775  # 9.25 * 300
DPI = 300

# Safe area (0.125" bleed on each side)
BLEED = 38  # 0.125 * 300
SAFE_LEFT = BLEED
SAFE_TOP = BLEED
SAFE_RIGHT = COVER_WIDTH - BLEED
SAFE_BOTTOM = COVER_HEIGHT - BLEED

# Colors by category
COLORS = {
    'major_works': {'bg': '#1a365d', 'name': 'Deep Blue'},
    'essential': {'bg': '#722f37', 'name': 'Burgundy'},
    'teachings': {'bg': '#2d5016', 'name': 'Forest Green'},
    'introductory': {'bg': '#c65d07', 'name': 'Golden Orange'},
    'lectures': {'bg': '#4a1a6b', 'name': 'Purple'},
}

# Accent colors
CREAM = '#f5f5dc'
GOLD = '#d4af37'
LIGHT_GOLD = '#c9a227'

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_font(name, size):
    """Get font, falling back to default if not found"""
    font_paths = [
        f"/System/Library/Fonts/{name}.ttc",
        f"/System/Library/Fonts/Supplemental/{name}.ttf",
        f"/Library/Fonts/{name}.ttf",
        f"/Library/Fonts/{name}.otf",
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass

    # Fallback fonts
    fallbacks = [
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/System/Library/Fonts/NewYork.ttf",
    ]

    for path in fallbacks:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass

    return ImageFont.load_default()

def draw_decorative_border(draw, x1, y1, x2, y2, color, width=3):
    """Draw a decorative double-line border"""
    # Outer border
    draw.rectangle([x1, y1, x2, y2], outline=color, width=width)
    # Inner border
    offset = 15
    draw.rectangle([x1 + offset, y1 + offset, x2 - offset, y2 - offset], outline=color, width=2)

def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width"""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def generate_cover(title, subtitle, category, series_number, output_path):
    """Generate a minimalist book cover"""

    # Get category color
    cat_colors = COLORS.get(category, COLORS['introductory'])
    bg_color = hex_to_rgb(cat_colors['bg'])
    text_color = hex_to_rgb(CREAM)
    accent_color = hex_to_rgb(GOLD)

    # Create image
    img = Image.new('RGB', (COVER_WIDTH, COVER_HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = get_font("Georgia Bold", 120)
    subtitle_font = get_font("Georgia Italic", 60)
    author_font = get_font("Georgia", 54)
    series_font = get_font("Georgia", 42)
    number_font = get_font("Georgia Bold", 36)

    # Calculate positions
    content_left = SAFE_LEFT + 100
    content_right = SAFE_RIGHT - 100
    content_width = content_right - content_left
    center_x = COVER_WIDTH // 2

    # Draw decorative border
    border_margin = 80
    draw_decorative_border(
        draw,
        SAFE_LEFT + border_margin,
        SAFE_TOP + border_margin,
        SAFE_RIGHT - border_margin,
        SAFE_BOTTOM - border_margin,
        accent_color,
        width=4
    )

    # Title area (upper third)
    title_y = 400

    # Wrap and draw title
    title_lines = wrap_text(title.upper(), title_font, content_width, draw)

    for i, line in enumerate(title_lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        line_width = bbox[2] - bbox[0]
        x = center_x - line_width // 2
        draw.text((x, title_y + i * 140), line, font=title_font, fill=text_color)

    # Subtitle (if exists)
    if subtitle:
        subtitle_y = title_y + len(title_lines) * 140 + 60
        subtitle_lines = wrap_text(subtitle, subtitle_font, content_width, draw)
        for i, line in enumerate(subtitle_lines):
            bbox = draw.textbbox((0, 0), line, font=subtitle_font)
            line_width = bbox[2] - bbox[0]
            x = center_x - line_width // 2
            draw.text((x, subtitle_y + i * 80), line, font=subtitle_font, fill=text_color)

    # Decorative line
    line_y = COVER_HEIGHT // 2 + 100
    line_margin = 300
    draw.line(
        [(center_x - 200, line_y), (center_x + 200, line_y)],
        fill=accent_color,
        width=3
    )

    # Small decorative element
    draw.ellipse(
        [(center_x - 8, line_y - 8), (center_x + 8, line_y + 8)],
        fill=accent_color
    )

    # Author
    author_text = "His Divine Grace"
    author_y = line_y + 80
    bbox = draw.textbbox((0, 0), author_text, font=series_font)
    x = center_x - (bbox[2] - bbox[0]) // 2
    draw.text((x, author_y), author_text, font=series_font, fill=text_color)

    author_name = "A.C. Bhaktivedanta Swami"
    author_y += 70
    bbox = draw.textbbox((0, 0), author_name, font=author_font)
    x = center_x - (bbox[2] - bbox[0]) // 2
    draw.text((x, author_y), author_name, font=author_font, fill=text_color)

    author_title = "PRABHUPADA"
    author_y += 80
    prabhupada_font = get_font("Georgia Bold", 72)
    bbox = draw.textbbox((0, 0), author_title, font=prabhupada_font)
    x = center_x - (bbox[2] - bbox[0]) // 2
    draw.text((x, author_y), author_title, font=prabhupada_font, fill=accent_color)

    # Series branding at bottom
    series_y = SAFE_BOTTOM - 250

    # Horizontal line
    draw.line(
        [(content_left + 100, series_y), (content_right - 100, series_y)],
        fill=accent_color,
        width=2
    )

    # Series name
    series_text = "VEDABASE ORIGINAL EDITION"
    series_y += 40
    bbox = draw.textbbox((0, 0), series_text, font=series_font)
    x = center_x - (bbox[2] - bbox[0]) // 2
    draw.text((x, series_y), series_text, font=series_font, fill=text_color)

    # Series number
    if series_number:
        number_text = f"[ {series_number} ]"
        series_y += 60
        bbox = draw.textbbox((0, 0), number_text, font=number_font)
        x = center_x - (bbox[2] - bbox[0]) // 2
        draw.text((x, series_y), number_text, font=number_font, fill=accent_color)

    # Save
    img.save(output_path, 'PDF', resolution=DPI)
    print(f"Generated: {output_path}")

    # Also save as JPG for preview
    jpg_path = output_path.replace('.pdf', '.jpg')
    img.save(jpg_path, 'JPEG', quality=95)
    print(f"Preview: {jpg_path}")

    return img

# Book catalog
BOOKS = {
    'introductory': [
        {'id': 'I-01', 'title': 'Raja-vidya', 'subtitle': 'The King of Knowledge'},
        {'id': 'I-02', 'title': 'The Path of Perfection', 'subtitle': None},
        {'id': 'I-03', 'title': 'Perfect Questions, Perfect Answers', 'subtitle': None},
        {'id': 'I-04', 'title': 'The Perfection of Yoga', 'subtitle': None},
        {'id': 'I-05', 'title': 'Beyond Birth and Death', 'subtitle': None},
        {'id': 'I-06', 'title': 'Easy Journey to Other Planets', 'subtitle': None},
        {'id': 'I-07', 'title': 'Elevation to Krsna Consciousness', 'subtitle': None},
        {'id': 'I-08', 'title': 'Life Comes from Life', 'subtitle': None},
        {'id': 'I-09', 'title': 'Light of the Bhagavata', 'subtitle': None},
        {'id': 'I-10', 'title': 'On the Way to Krsna', 'subtitle': None},
        {'id': 'I-11', 'title': 'The Reservoir of Pleasure', 'subtitle': None},
        {'id': 'I-12', 'title': 'Topmost Yoga System', 'subtitle': None},
    ],
    'essential': [
        {'id': 'ET-01', 'title': 'The Nectar of Devotion', 'subtitle': 'The Complete Science of Bhakti-yoga'},
        {'id': 'ET-02', 'title': 'The Nectar of Instruction', 'subtitle': 'Sri Upadesamrta'},
        {'id': 'ET-03', 'title': 'Sri Isopanisad', 'subtitle': None},
        {'id': 'ET-04', 'title': 'Teachings of Lord Caitanya', 'subtitle': None},
    ],
    'teachings': [
        {'id': 'T-01', 'title': 'Teachings of Lord Kapila', 'subtitle': 'The Son of Devahuti'},
        {'id': 'T-02', 'title': 'Teachings of Queen Kunti', 'subtitle': None},
        {'id': 'T-03', 'title': 'Teachings of Prahlada Maharaja', 'subtitle': None},
        {'id': 'T-04', 'title': 'The Science of Self-Realization', 'subtitle': None},
    ],
    'major_works': [
        {'id': 'MW-01', 'title': 'Bhagavad-gita As It Is', 'subtitle': None},
        {'id': 'MW-02', 'title': 'Srimad-Bhagavatam', 'subtitle': 'Bhagavata Purana'},
        {'id': 'MW-03', 'title': 'Sri Caitanya-caritamrta', 'subtitle': None},
        {'id': 'MW-04', 'title': 'Krsna', 'subtitle': 'The Supreme Personality of Godhead'},
    ],
    'lectures': [
        {'id': 'LC-01', 'title': 'Lectures', 'subtitle': 'Part One'},
        {'id': 'LC-02', 'title': 'Lectures', 'subtitle': 'Part Two'},
        {'id': 'LC-03', 'title': 'Conversations', 'subtitle': None},
        {'id': 'LC-04', 'title': 'Letters', 'subtitle': None},
    ],
}

def generate_all_covers(output_dir):
    """Generate covers for all books"""
    os.makedirs(output_dir, exist_ok=True)

    for category, books in BOOKS.items():
        cat_dir = os.path.join(output_dir, category)
        os.makedirs(cat_dir, exist_ok=True)

        for book in books:
            filename = f"cover_{book['id'].lower().replace('-', '_')}.pdf"
            output_path = os.path.join(cat_dir, filename)

            generate_cover(
                title=book['title'],
                subtitle=book.get('subtitle'),
                category=category,
                series_number=book['id'],
                output_path=output_path
            )

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        # Generate all covers
        output_dir = os.path.join(os.path.dirname(__file__), 'covers')
        generate_all_covers(output_dir)
    else:
        # Generate single test cover
        output_dir = os.path.join(os.path.dirname(__file__), 'covers', 'test')
        os.makedirs(output_dir, exist_ok=True)

        generate_cover(
            title="Raja-vidya",
            subtitle="The King of Knowledge",
            category="introductory",
            series_number="I-01",
            output_path=os.path.join(output_dir, "cover_raja_vidya.pdf")
        )

        print("\nTest cover generated! Run with --all to generate all covers.")
