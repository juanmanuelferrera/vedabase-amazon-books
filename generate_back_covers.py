#!/usr/bin/env python3
"""
Vedabase Original Edition - Back Cover Generator
Generates consistent back covers with variable book descriptions
For Amazon KDP 6x9 format
"""

from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# KDP 6x9 cover dimensions (with bleed)
COVER_WIDTH = 1838  # 6.125 * 300
COVER_HEIGHT = 2775  # 9.25 * 300
DPI = 300

# Safe area
BLEED = 38
SAFE_LEFT = BLEED + 60
SAFE_TOP = BLEED + 60
SAFE_RIGHT = COVER_WIDTH - BLEED - 60
SAFE_BOTTOM = COVER_HEIGHT - BLEED - 60

# Colors
COLORS = {
    'major_works': '#1a365d',
    'essential': '#722f37',
    'teachings': '#2d5016',
    'introductory': '#c65d07',
    'lectures': '#4a1a6b',
}

CREAM = '#f5f5dc'
GOLD = '#d4af37'
DARK_TEXT = '#1a1a1a'

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_font(name, size):
    font_paths = [
        f"/System/Library/Fonts/Supplemental/{name}.ttf",
        f"/System/Library/Fonts/{name}.ttc",
        f"/Library/Fonts/{name}.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    fallbacks = [
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/NewYork.ttf",
    ]
    for path in fallbacks:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

def wrap_text_to_lines(text, font, max_width, draw):
    """Wrap text and return lines"""
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

def generate_back_cover(
    book_description,
    category,
    series_number,
    output_path,
    tagline="The words he chose. Unchanged. Unedited."
):
    """Generate a back cover with consistent layout"""

    bg_color = hex_to_rgb(COLORS.get(category, COLORS['introductory']))
    text_color = hex_to_rgb(CREAM)
    accent_color = hex_to_rgb(GOLD)

    # Create image
    img = Image.new('RGB', (COVER_WIDTH, COVER_HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    quote_font = get_font("Georgia Italic", 48)
    desc_font = get_font("Georgia", 42)
    tagline_font = get_font("Georgia Bold", 36)
    small_font = get_font("Georgia", 32)
    series_font = get_font("Georgia", 38)

    # Content area
    content_left = SAFE_LEFT + 80
    content_right = SAFE_RIGHT - 80
    content_width = content_right - content_left
    center_x = COVER_WIDTH // 2

    # Top decorative border
    border_y = SAFE_TOP + 40
    draw.line([(content_left, border_y), (content_right, border_y)], fill=accent_color, width=3)

    # Main description area
    desc_y = SAFE_TOP + 150

    # Book description (main text)
    desc_lines = wrap_text_to_lines(book_description, desc_font, content_width, draw)

    line_height = 60
    for i, line in enumerate(desc_lines):
        draw.text((content_left, desc_y + i * line_height), line, font=desc_font, fill=text_color)

    # About This Edition section
    about_y = desc_y + len(desc_lines) * line_height + 100

    # Section divider
    draw.line([(center_x - 150, about_y), (center_x + 150, about_y)], fill=accent_color, width=2)

    about_y += 50
    about_title = "ABOUT THIS EDITION"
    bbox = draw.textbbox((0, 0), about_title, font=tagline_font)
    x = center_x - (bbox[2] - bbox[0]) // 2
    draw.text((x, about_y), about_title, font=tagline_font, fill=accent_color)

    about_y += 70
    about_text = (
        "This text has been meticulously transcribed from high-resolution scans "
        "of the original first edition, published during the author's lifetime. "
        "No posthumous editorial changes have been made."
    )

    about_lines = wrap_text_to_lines(about_text, small_font, content_width, draw)
    for i, line in enumerate(about_lines):
        draw.text((content_left, about_y + i * 50), line, font=small_font, fill=text_color)

    # Bottom section
    bottom_y = SAFE_BOTTOM - 350

    # Tagline
    draw.line([(content_left, bottom_y), (content_right, bottom_y)], fill=accent_color, width=2)

    bottom_y += 50
    bbox = draw.textbbox((0, 0), tagline, font=quote_font)
    x = center_x - (bbox[2] - bbox[0]) // 2
    draw.text((x, bottom_y), tagline, font=quote_font, fill=text_color)

    # Website
    bottom_y += 100
    website = "vedabase.bhaktiyoga.es"
    bbox = draw.textbbox((0, 0), website, font=series_font)
    x = center_x - (bbox[2] - bbox[0]) // 2
    draw.text((x, bottom_y), website, font=series_font, fill=accent_color)

    # Series info
    bottom_y += 80
    series_text = f"VEDABASE ORIGINAL EDITION  •  {series_number}"
    bbox = draw.textbbox((0, 0), series_text, font=small_font)
    x = center_x - (bbox[2] - bbox[0]) // 2
    draw.text((x, bottom_y), series_text, font=small_font, fill=text_color)

    # Bottom decorative border
    draw.line([(content_left, SAFE_BOTTOM - 40), (content_right, SAFE_BOTTOM - 40)], fill=accent_color, width=3)

    # Save
    img.save(output_path, 'PDF', resolution=DPI)
    print(f"Generated: {output_path}")

    jpg_path = output_path.replace('.pdf', '.jpg')
    img.save(jpg_path, 'JPEG', quality=95)

    return img

# Book descriptions for back covers
BOOK_DESCRIPTIONS = {
    'I-01': """In this small but powerful book, Srila Prabhupada explains the essence of Bhagavad-gita's ninth chapter—the most confidential knowledge. What is the king of all knowledge? Why is devotion to Krishna the supreme secret? Here, these profound truths become accessible to everyone, regardless of background or prior study.""",

    'I-02': """The path to perfection is not abstract theory—it is a practical science of self-realization. Through the teachings of dhyana-yoga from Bhagavad-gita's sixth chapter, Srila Prabhupada guides us step by step toward the ultimate goal of human life: direct connection with the Supreme.""",

    'I-03': """In 1972, a young American named Bob Cohen traveled to India seeking answers. He found Srila Prabhupada in a small village and asked the questions that burn in every sincere heart: Who am I? Why do I suffer? What happens after death? These intimate conversations reveal wisdom that transforms lives.""",

    'I-04': """Yoga has become synonymous with physical postures and breathing exercises. But what is the actual goal of yoga? In this compact volume, Srila Prabhupada cuts through modern misconceptions to reveal the original purpose of yoga as taught by Krishna himself.""",

    'I-05': """Death is the one appointment no one can avoid. Yet most people live in denial, unprepared for this inevitable transition. Srila Prabhupada illuminates what the Vedas reveal about the soul's journey beyond the body—knowledge that liberates us from the fear of death.""",

    'I-06': """Long before modern science speculated about extraterrestrial life and interplanetary travel, the Vedic literature described in detail the inhabitants and conditions of other planets. This book presents the science of traveling beyond this world—not by mechanical means, but by consciousness.""",

    'I-07': """How does one begin the spiritual journey? What are the first steps toward elevation of consciousness? Srila Prabhupada provides a clear, practical guide for anyone seeking to rise above the mundane platform and taste the happiness of spiritual awareness.""",

    'I-08': """Modern science claims that life arises from matter. But is this really true? In these thought-provoking conversations with his disciples, Srila Prabhupada challenges the assumptions of materialistic science and presents the Vedic understanding: life comes from life.""",

    'I-09': """Inspired by the autumn season's beauty, this unique work combines Srila Prabhupada's poetic insights with stunning paintings depicting scenes from Krishna's pastimes. Each verse illuminates the spiritual significance hidden within the natural world.""",

    'I-10': """For those just beginning to explore spiritual life, this book offers a warm and encouraging introduction. Srila Prabhupada explains the basic principles of Krishna consciousness in a way that is both profound and accessible to newcomers.""",

    'I-11': """Where can we find real pleasure—pleasure that doesn't fade or disappoint? Srila Prabhupada reveals that Krishna is the reservoir of all pleasure, and that connecting with Him is the key to experiencing lasting satisfaction.""",

    'I-12': """Among all yoga systems, which is the highest? In this concise guide, Srila Prabhupada explains why bhakti-yoga—the yoga of devotion—is declared by Krishna to be the topmost spiritual process, accessible to everyone in this age.""",
}

def generate_all_back_covers(output_dir):
    """Generate back covers for all books"""
    os.makedirs(output_dir, exist_ok=True)

    for book_id, description in BOOK_DESCRIPTIONS.items():
        # Determine category from ID
        if book_id.startswith('I-'):
            category = 'introductory'
        elif book_id.startswith('ET-'):
            category = 'essential'
        elif book_id.startswith('T-'):
            category = 'teachings'
        elif book_id.startswith('MW-'):
            category = 'major_works'
        elif book_id.startswith('LC-'):
            category = 'lectures'
        else:
            category = 'introductory'

        filename = f"back_{book_id.lower().replace('-', '_')}.pdf"
        output_path = os.path.join(output_dir, filename)

        generate_back_cover(
            book_description=description,
            category=category,
            series_number=book_id,
            output_path=output_path
        )

if __name__ == '__main__':
    import sys

    output_dir = os.path.join(os.path.dirname(__file__), 'covers', 'back')
    os.makedirs(output_dir, exist_ok=True)

    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        generate_all_back_covers(output_dir)
    else:
        # Test with Raja-vidya
        generate_back_cover(
            book_description=BOOK_DESCRIPTIONS['I-01'],
            category='introductory',
            series_number='I-01',
            output_path=os.path.join(output_dir, 'back_i_01.pdf')
        )
        print("\nTest back cover generated!")
