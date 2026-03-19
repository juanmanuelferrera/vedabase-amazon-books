#!/usr/bin/env python3
"""
Create Kindle eBook cover (front only)
KDP requirements: 1600 x 2560 px (1:1.6 ratio), JPEG, RGB
"""

import os
import yaml
from PIL import Image, ImageDraw, ImageFont

# eBook cover dimensions (KDP recommended)
EBOOK_WIDTH = 1600
EBOOK_HEIGHT = 2560

# Colors
COLORS = {
    'burgundy': {
        'bg': (74, 28, 35),
        'text': (255, 250, 240),
        'accent': (180, 140, 100),
    },
    'blue': {
        'bg': (18, 40, 70),
        'text': (255, 250, 240),
        'accent': (140, 160, 180),
    },
    'forest': {
        'bg': (25, 50, 35),
        'text': (255, 250, 240),
        'accent': (140, 180, 140),
    },
    'orange': {
        'bg': (120, 60, 20),
        'text': (255, 250, 240),
        'accent': (200, 160, 100),
    }
}

DEFAULT_COLOR = 'burgundy'


def load_font(name, size):
    """Load a font, with fallbacks"""
    font_paths = [
        f"/System/Library/Fonts/{name}.ttc",
        f"/System/Library/Fonts/{name}.ttf",
        f"/Library/Fonts/{name}.ttf",
        f"/Library/Fonts/{name}.ttc",
        f"fonts/{name}.ttf",
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue

    # Fallbacks
    fallbacks = [
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/System/Library/Fonts/Times.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]

    for path in fallbacks:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue

    return ImageFont.load_default()


def create_ebook_cover(title, subtitle=None, series_number=None, color_scheme='burgundy', output_path=None):
    """Create Kindle eBook cover image"""

    colors = COLORS.get(color_scheme, COLORS[DEFAULT_COLOR])

    # Create image
    img = Image.new('RGB', (EBOOK_WIDTH, EBOOK_HEIGHT), colors['bg'])
    draw = ImageDraw.Draw(img)

    # Draw decorative border
    border_margin = 60
    border_width = 3
    draw.rectangle(
        [border_margin, border_margin, EBOOK_WIDTH - border_margin, EBOOK_HEIGHT - border_margin],
        outline=colors['accent'],
        width=border_width
    )

    # Inner border
    inner_margin = 80
    draw.rectangle(
        [inner_margin, inner_margin, EBOOK_WIDTH - inner_margin, EBOOK_HEIGHT - inner_margin],
        outline=colors['accent'],
        width=1
    )

    # Title
    title_font = load_font("Georgia", 120)

    # Word wrap title
    max_width = EBOOK_WIDTH - 200
    words = title.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    # Calculate title position
    line_height = 140
    total_title_height = len(lines) * line_height
    title_y = 600

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (EBOOK_WIDTH - text_width) // 2
        y = title_y + i * line_height
        draw.text((x, y), line, font=title_font, fill=colors['text'])

    # Subtitle
    if subtitle:
        subtitle_font = load_font("Georgia", 60)
        subtitle_y = title_y + total_title_height + 60
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (EBOOK_WIDTH - text_width) // 2
        draw.text((x, subtitle_y), subtitle, font=subtitle_font, fill=colors['accent'])

    # Decorative line
    line_y = 1400
    line_width = 400
    line_x = (EBOOK_WIDTH - line_width) // 2
    draw.line([(line_x, line_y), (line_x + line_width, line_y)], fill=colors['accent'], width=2)

    # Author
    author_prefix_font = load_font("Georgia", 36)
    author_font = load_font("Georgia", 48)
    author_title_font = load_font("Georgia", 56)

    prefix = "His Divine Grace"
    author = "A.C. Bhaktivedanta Swami"
    author_title = "Prabhupada"

    # Author prefix
    bbox = draw.textbbox((0, 0), prefix, font=author_prefix_font)
    x = (EBOOK_WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, 1500), prefix, font=author_prefix_font, fill=colors['text'])

    # Author name
    bbox = draw.textbbox((0, 0), author, font=author_font)
    x = (EBOOK_WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, 1560), author, font=author_font, fill=colors['text'])

    # Prabhupada
    bbox = draw.textbbox((0, 0), author_title, font=author_title_font)
    x = (EBOOK_WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, 1630), author_title, font=author_title_font, fill=colors['text'])

    # Series branding at bottom
    series_font = load_font("Georgia", 32)
    series_text = "VEDABASE ORIGINAL EDITION"
    bbox = draw.textbbox((0, 0), series_text, font=series_font)
    x = (EBOOK_WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, EBOOK_HEIGHT - 180), series_text, font=series_font, fill=colors['accent'])

    # Series number if provided
    if series_number:
        num_font = load_font("Georgia", 28)
        bbox = draw.textbbox((0, 0), series_number, font=num_font)
        x = (EBOOK_WIDTH - (bbox[2] - bbox[0])) // 2
        draw.text((x, EBOOK_HEIGHT - 130), series_number, font=num_font, fill=colors['accent'])

    # Save
    if output_path:
        img.save(output_path, 'JPEG', quality=95)
        print(f"eBook cover saved: {output_path}")

    return img


def load_book_metadata(book_id):
    """Load book metadata from YAML file"""
    books_dir = 'books'
    for category in os.listdir(books_dir):
        cat_path = os.path.join(books_dir, category)
        if os.path.isdir(cat_path):
            for book_dir in os.listdir(cat_path):
                if book_id.lower() in book_dir.lower():
                    meta_path = os.path.join(cat_path, book_dir, 'metadata.yaml')
                    if os.path.exists(meta_path):
                        with open(meta_path, 'r') as f:
                            return yaml.safe_load(f)
    return None


if __name__ == '__main__':
    import sys

    output_dir = 'output/ebook_covers'
    os.makedirs(output_dir, exist_ok=True)

    if len(sys.argv) > 1:
        book_id = sys.argv[1]
        meta = load_book_metadata(book_id)

        if meta:
            output_path = os.path.join(output_dir, f"{book_id}_ebook_cover.jpg")
            create_ebook_cover(
                title=meta.get('title', 'Untitled'),
                subtitle=meta.get('subtitle'),
                series_number=meta.get('series_id', book_id),
                output_path=output_path
            )
        else:
            print(f"Book not found: {book_id}")
    else:
        # Default: Raja-vidya
        output_path = os.path.join(output_dir, "I-01_ebook_cover.jpg")
        create_ebook_cover(
            title="Raja-vidya",
            subtitle="The King of Knowledge",
            series_number="I-01",
            output_path=output_path
        )
