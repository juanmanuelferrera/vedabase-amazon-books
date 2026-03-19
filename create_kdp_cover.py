#!/usr/bin/env python3
"""
Create KDP-ready full cover (front + spine + back)
Automatically calculates spine width based on page count
"""

import argparse
import os
import subprocess
import yaml
from PIL import Image, ImageDraw, ImageFont

# KDP specs for 6x9 cream paper
DPI = 300
FRONT_WIDTH = 6.125  # 6" + 0.125" bleed
FRONT_HEIGHT = 9.25  # 9" + 0.25" bleed
BACK_WIDTH = 6.125
PAGE_THICKNESS = 0.0025  # inches per page (cream paper)

# Series color - Vedabase Original Edition
COLORS = {
    'burgundy': {
        'bg': (74, 28, 35),       # Darker burgundy
        'spine': (54, 18, 25),
        'text': (255, 250, 240),
    },
    'blue': {
        'bg': (18, 40, 70),       # Darker blue
        'spine': (12, 30, 55),
        'text': (255, 250, 240),
    }
}

DEFAULT_COLOR = 'burgundy'


def get_pdf_page_count(pdf_path):
    """Get page count from PDF using pdfinfo or similar"""
    try:
        result = subprocess.run(
            ['pdfinfo', pdf_path],
            capture_output=True, text=True
        )
        for line in result.stdout.split('\n'):
            if line.startswith('Pages:'):
                return int(line.split(':')[1].strip())
    except:
        pass

    # Fallback: try with mdls (macOS)
    try:
        result = subprocess.run(
            ['mdls', '-name', 'kMDItemNumberOfPages', pdf_path],
            capture_output=True, text=True
        )
        if 'kMDItemNumberOfPages' in result.stdout:
            pages = result.stdout.split('=')[1].strip()
            if pages != '(null)':
                return int(pages)
    except:
        pass

    return None


def load_book_metadata(book_id):
    """Load book metadata from YAML file"""
    # Search in books directory
    books_dir = 'books'
    for category in os.listdir(books_dir):
        cat_path = os.path.join(books_dir, category)
        if os.path.isdir(cat_path):
            for book_dir in os.listdir(cat_path):
                if book_dir.lower().startswith(book_id.lower()):
                    meta_path = os.path.join(cat_path, book_dir, 'metadata.yaml')
                    if os.path.exists(meta_path):
                        with open(meta_path, 'r') as f:
                            meta = yaml.safe_load(f)
                        meta['path'] = os.path.join(cat_path, book_dir)
                        return meta
    return None


def find_cover_image(book_id, meta=None):
    """Find original cover image for a book"""
    covers_dir = 'covers/originals'
    book_id_lower = book_id.lower().replace('-', '_')

    # Build search patterns
    patterns = [
        f"{book_id_lower}_cover",
        book_id_lower,
    ]

    # Add patterns from metadata title if available
    if meta and 'title' in meta:
        title_slug = meta['title'].lower().replace(' ', '_').replace('-', '_').replace(':', '')
        # Extract key words from title
        for word in title_slug.split('_'):
            if len(word) > 3:  # Skip short words
                patterns.append(word)
        patterns.append(title_slug)

    for f in os.listdir(covers_dir):
        f_lower = f.lower()
        for pattern in patterns:
            if pattern in f_lower and f_lower.endswith(('.jpg', '.jpeg', '.png')):
                return os.path.join(covers_dir, f)

    return None


def find_interior_pdf(book_id):
    """Find interior PDF for page count - prefer the largest file"""
    output_dir = 'output/interiors'
    matches = []
    for f in os.listdir(output_dir):
        if book_id in f and f.endswith('.pdf'):
            path = os.path.join(output_dir, f)
            size = os.path.getsize(path)
            matches.append((path, size))

    if matches:
        # Return the largest PDF (most likely the complete one)
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[0][0]
    return None


def create_cover(book_id, pages=None, color=DEFAULT_COLOR, title=None, subtitle=None):
    """Create KDP cover for a book"""

    # Load metadata
    meta = load_book_metadata(book_id)
    if not meta and not title:
        print(f"Error: No metadata found for {book_id}")
        return None

    book_title = title or meta.get('title', book_id)
    book_subtitle = subtitle or meta.get('subtitle', '')

    # Get page count
    if pages is None:
        pdf_path = find_interior_pdf(book_id)
        if pdf_path:
            pages = get_pdf_page_count(pdf_path)
            print(f"Auto-detected pages: {pages}")

        if pages is None:
            print("Error: Could not determine page count. Use --pages")
            return None

    # Calculate dimensions
    spine_width = pages * PAGE_THICKNESS
    total_width = BACK_WIDTH + spine_width + FRONT_WIDTH

    print(f"Book: {book_title}")
    print(f"Pages: {pages}")
    print(f"Spine: {spine_width:.3f} in")
    print(f"Total cover: {total_width:.3f} x {FRONT_HEIGHT:.3f} in")

    # Pixel dimensions
    width_px = int(total_width * DPI)
    height_px = int(FRONT_HEIGHT * DPI)
    front_px = int(FRONT_WIDTH * DPI)
    spine_px = int(spine_width * DPI)
    back_px = int(BACK_WIDTH * DPI)

    # Colors
    palette = COLORS.get(color, COLORS[DEFAULT_COLOR])
    bg_color = palette['bg']
    spine_color = palette['spine']
    text_color = palette['text']

    # Create base image
    cover = Image.new('RGB', (width_px, height_px), bg_color)
    draw = ImageDraw.Draw(cover)

    # Draw spine area
    spine_x = back_px
    draw.rectangle([spine_x, 0, spine_x + spine_px, height_px], fill=spine_color)

    # Load original cover image if available
    cover_img_path = find_cover_image(book_id, meta)
    if cover_img_path:
        original = Image.open(cover_img_path)

        # Scale to fit (85% of front width)
        scale_width = int(front_px * 0.85)
        scale_height = int(original.height * (scale_width / original.width))
        original_resized = original.resize((scale_width, scale_height), Image.LANCZOS)

        # Position on front cover (centered horizontally and vertically)
        front_start = back_px + spine_px
        img_x = front_start + (front_px - scale_width) // 2
        img_y = (height_px - scale_height) // 2

        # White border
        border = 10
        draw.rectangle([img_x - border, img_y - border,
                        img_x + scale_width + border, img_y + scale_height + border],
                       fill=(255, 255, 255))
        cover.paste(original_resized, (img_x, img_y))

    # Load fonts
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 36)
        author_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 30)
        spine_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", max(18, spine_px // 4))
        series_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 24)
        back_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = title_font
        author_font = title_font
        spine_font = title_font
        series_font = title_font
        back_font = title_font

    # Front cover - Series name at bottom
    front_start = back_px + spine_px
    series_text = "VEDABASE ORIGINAL EDITION"
    bbox = draw.textbbox((0, 0), series_text, font=series_font)
    series_width = bbox[2] - bbox[0]
    draw.text((front_start + (front_px - series_width) // 2, height_px - int(0.08 * height_px)),
              series_text, fill=text_color, font=series_font)

    # Spine text (only if spine is wide enough for KDP - minimum ~67 pages)
    # Professional convention: title at top, author in center, number at bottom (horizontal)
    # Font sizes scale with spine width but have min/max limits for series consistency
    if spine_px > 50:

        # Calculate font sizes: % of spine with min/max limits for series consistency
        def calc_font_size(spine_width, percent, min_px, max_px):
            size = int(spine_width * percent)
            return max(min_px, min(size, max_px))

        # Font sizes that scale but maintain consistency across the series
        # Larger spine = larger fonts (with min/max limits for consistency)
        title_font_size = calc_font_size(spine_px, 0.50, 24, 80)
        author_font_size = calc_font_size(spine_px, 0.40, 18, 65)
        number_font_size = calc_font_size(spine_px, 0.60, 40, 130)

        spine_font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", title_font_size)
        spine_font_author = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", author_font_size)

        # Create spine image (width=height_px because it will be rotated)
        spine_img = Image.new('RGBA', (height_px, spine_px), (0, 0, 0, 0))
        spine_draw = ImageDraw.Draw(spine_img)

        # Extract series number from book_id (e.g., "I-01" → "01")
        series_number = book_id.split('-')[-1] if '-' in book_id else "01"

        # Title
        title_text = book_title.upper()
        bbox_title = spine_draw.textbbox((0, 0), title_text, font=spine_font_title)
        title_width = bbox_title[2] - bbox_title[0]
        title_height = bbox_title[3] - bbox_title[1]
        title_offset_y = bbox_title[1]  # Offset from baseline

        # Author
        author_text = "A.C. Bhaktivedanta Swami Prabhupāda"
        bbox_author = spine_draw.textbbox((0, 0), author_text, font=spine_font_author)
        author_width = bbox_author[2] - bbox_author[0]
        author_height = bbox_author[3] - bbox_author[1]
        author_offset_y = bbox_author[1]  # Offset from baseline

        # THREE INDEPENDENT ZONES on spine (after 90° rotation: right=top, left=bottom)
        # Zone 1: TITLE at top
        # Zone 2: AUTHOR in center-upper
        # Zone 3: NUMBER at bottom (horizontal, not rotated)

        # ZONE 1 - TITLE: at TOP (82% from bottom = 18% from top)
        title_zone = int(height_px * 0.82)
        title_x = title_zone - (title_width // 2)
        title_y = (spine_px - title_height) // 2 - title_offset_y

        # ZONE 2 - AUTHOR: centered between middle and bottom (25% from bottom)
        author_zone = int(height_px * 0.25)
        author_x = author_zone - (author_width // 2)
        author_y = (spine_px - author_height) // 2 - author_offset_y

        spine_draw.text((title_x, title_y), title_text, fill=text_color, font=spine_font_title)
        spine_draw.text((author_x, author_y), author_text, fill=text_color, font=spine_font_author)

        # Rotate 90° clockwise so text reads top-to-bottom
        spine_rotated = spine_img.rotate(90, expand=True)
        cover.paste(spine_rotated, (spine_x, 0), spine_rotated)

        # ZONE 3 - NUMBER: HORIZONTAL at bottom (independent calculation)
        # Scale with spine but respect min/max for series consistency
        spine_number_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", number_font_size)

        bbox_num = draw.textbbox((0, 0), series_number, font=spine_number_font)
        num_width = bbox_num[2] - bbox_num[0]
        num_height = bbox_num[3] - bbox_num[1]

        # NUMBER position: centered on spine, 6% from bottom edge
        num_zone_y = height_px - int(0.06 * height_px)
        num_x = spine_x + (spine_px - num_width) // 2
        num_y = num_zone_y - (num_height // 2)

        draw.text((num_x, num_y), series_number, fill=text_color, font=spine_number_font)

    # Back cover - Professional layout, JUSTIFIED text
    back_center = back_px // 2
    back_margin_left = int(0.65 * DPI)   # 0.65" left margin
    back_margin_right = int(0.65 * DPI)  # 0.65" right margin
    text_width = back_px - back_margin_left - back_margin_right

    # Professional fonts - LARGE sizes
    back_title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 110)
    back_subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 64)
    blurb_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 60)
    back_author_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 44)
    series_back_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 34)

    # Title - prominent at top, centered
    bbox = draw.textbbox((0, 0), book_title.upper(), font=back_title_font)
    draw.text((back_center - (bbox[2] - bbox[0]) // 2, int(0.07 * height_px)),
              book_title.upper(), fill=text_color, font=back_title_font)

    # Subtitle - centered
    if book_subtitle:
        bbox = draw.textbbox((0, 0), book_subtitle, font=back_subtitle_font)
        draw.text((back_center - (bbox[2] - bbox[0]) // 2, int(0.15 * height_px)),
                  book_subtitle, fill=text_color, font=back_subtitle_font)

    # Blurb/Description from metadata
    book_description = meta.get('description', '') if meta else ''
    if not book_description:
        book_description = "This is the original edition, unchanged and unedited."

    def draw_justified_text(text, font, left_x, right_x, start_y, line_height):
        """Draw text with FULL justification - both edges perfectly aligned"""
        width = right_x - left_x

        # Normalize text: join lines within paragraphs, keep blank lines as separators
        raw_lines = text.strip().split('\n')
        paragraphs = []
        current_para = []

        for line in raw_lines:
            if line.strip():
                current_para.append(line.strip())
            else:
                if current_para:
                    paragraphs.append(' '.join(current_para))
                    current_para = []
        if current_para:
            paragraphs.append(' '.join(current_para))

        y = start_y

        for paragraph in paragraphs:
            words = paragraph.split()
            lines = []
            current = []

            # Word wrap
            for word in words:
                test = ' '.join(current + [word])
                bb = draw.textbbox((0, 0), test, font=font)
                if bb[2] - bb[0] <= width:
                    current.append(word)
                else:
                    if current:
                        lines.append(current)
                    current = [word]
            if current:
                lines.append(current)

            for i, words_in_line in enumerate(lines):
                is_last = (i == len(lines) - 1)
                n = len(words_in_line)

                if n == 1 or is_last:
                    # Last line or single word: left-align
                    draw.text((left_x, y), ' '.join(words_in_line), fill=text_color, font=font)
                else:
                    # Full justify: calculate exact positions
                    # Get width of each word
                    word_widths = []
                    for w in words_in_line:
                        bb = draw.textbbox((0, 0), w, font=font)
                        word_widths.append(bb[2] - bb[0])

                    total_words_width = sum(word_widths)
                    total_space = width - total_words_width
                    space_between = total_space / (n - 1)

                    # Calculate absolute positions to avoid rounding errors
                    positions = []
                    for j in range(n):
                        if j == 0:
                            pos = left_x
                        elif j == n - 1:
                            # Last word: explicitly place at right edge
                            pos = right_x - word_widths[j]
                        else:
                            # Middle words: proportional spacing
                            pos = left_x + sum(word_widths[:j]) + (j * space_between)
                        positions.append(round(pos))

                    # Draw each word at its calculated position
                    for j, word in enumerate(words_in_line):
                        draw.text((positions[j], y), word, fill=text_color, font=font)

                y += line_height

            y += int(line_height * 0.5)

        return y

    # Draw justified blurb
    y_pos = int(0.25 * height_px)
    line_height = 72
    right_edge = back_px - back_margin_right
    y_pos = draw_justified_text(book_description, blurb_font, back_margin_left, right_edge, y_pos, line_height)

    # BARCODE AREA - Amazon places 2" x 1.2" barcode in bottom right, 0.25" from edges
    # Keep text on LEFT side at bottom to avoid barcode area
    # Barcode zone: from (back_px - 2.25" * DPI) to (back_px - 0.25" * DPI) horizontally
    #               from (height_px - 1.45" * DPI) to (height_px - 0.25" * DPI) vertically

    # Author section - LEFT aligned
    author_y = height_px - int(0.22 * height_px)

    # Line 1: "His Divine Grace" (regular, larger)
    author_title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 46)
    draw.text((back_margin_left, author_y), "His Divine Grace", fill=text_color, font=author_title_font)

    # Lines 2-3: Name in bold, UPPERCASE
    author_name_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 52)
    draw.text((back_margin_left, author_y + 60), "A.C. BHAKTIVEDANTA", fill=text_color, font=author_name_font)
    draw.text((back_margin_left, author_y + 120), "SWAMI PRABHUPĀDA", fill=text_color, font=author_name_font)

    # Series name - LEFT side, above barcode zone
    series_y = height_px - int(0.06 * height_px)
    series_back = "VEDABASE ORIGINAL EDITION"
    draw.text((back_margin_left, series_y), series_back, fill=text_color, font=series_back_font)
    # Space reserved: 2" x 1.2" in bottom right corner for Amazon barcode

    # Save
    os.makedirs('output/covers', exist_ok=True)

    # Clean filename
    clean_title = book_title.lower().replace(' ', '_').replace('-', '_')
    clean_title = ''.join(c for c in clean_title if c.isalnum() or c == '_')

    pdf_path = f'output/covers/{book_id}_{clean_title}_kdp_cover.pdf'
    jpg_path = f'output/covers/{book_id}_{clean_title}_kdp_cover.jpg'

    cover_rgb = cover.convert('RGB')
    cover_rgb.save(pdf_path, 'PDF', resolution=300)
    cover_rgb.save(jpg_path, 'JPEG', quality=95)

    print(f"\nCover created:")
    print(f"  PDF: {pdf_path}")
    print(f"  JPG: {jpg_path}")
    print(f"  Dimensions: {width_px} x {height_px} px")

    return pdf_path


def main():
    parser = argparse.ArgumentParser(description='Create KDP-ready book cover')
    parser.add_argument('book_id', help='Book ID (e.g., I-01)')
    parser.add_argument('--pages', type=int, help='Number of pages (auto-detected if not provided)')
    parser.add_argument('--color', choices=['burgundy', 'blue'], default=DEFAULT_COLOR,
                        help='Cover color scheme')
    parser.add_argument('--title', help='Override book title')
    parser.add_argument('--subtitle', help='Override book subtitle')

    args = parser.parse_args()

    create_cover(
        args.book_id,
        pages=args.pages,
        color=args.color,
        title=args.title,
        subtitle=args.subtitle
    )


if __name__ == '__main__':
    main()
