#!/usr/bin/env python3
"""
Vedabase Original Edition - EPUB Generator
Converts book content to EPUB format for eReaders and Archive.org
"""

import os
import yaml
from ebooklib import epub
from datetime import datetime

# Reuse functions from interior generator
from generate_interior import (
    load_book_metadata,
    load_book_content,
    BOOKS_DIR,
    SERIES_BOOKS
)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'epub')


def create_epub_css():
    """Create CSS for EPUB styling"""
    return '''
body {
    font-family: Georgia, serif;
    font-size: 1em;
    line-height: 1.6;
    margin: 1em;
}

h1 {
    font-size: 1.8em;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1em;
}

h2 {
    font-size: 1.4em;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 0.75em;
}

.chapter-number {
    text-align: center;
    font-size: 0.9em;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 0.5em;
}

.chapter-title {
    text-align: center;
    font-size: 1.6em;
    margin-bottom: 1.5em;
}

.verse-block {
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.verse-number {
    font-weight: bold;
    text-align: center;
    margin-bottom: 0.5em;
}

.sanskrit {
    font-style: italic;
    text-align: center;
    margin-bottom: 0.75em;
}

.synonyms {
    font-size: 0.95em;
    margin-bottom: 0.75em;
}

.translation {
    font-style: italic;
    margin-bottom: 0.75em;
}

.purport-header {
    font-weight: bold;
    font-size: 0.9em;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 1em;
    margin-bottom: 0.5em;
}

.purport p {
    text-indent: 1.5em;
    margin-bottom: 0.5em;
}

.purport p:first-child {
    text-indent: 0;
}

.title-page {
    text-align: center;
    margin-top: 30%;
}

.title-page h1 {
    font-size: 2em;
    margin-bottom: 0.5em;
}

.title-page .subtitle {
    font-style: italic;
    font-size: 1.2em;
    margin-bottom: 2em;
}

.title-page .author {
    font-size: 1.1em;
    margin-top: 2em;
}

.copyright-page {
    font-size: 0.85em;
    margin-top: 50%;
}

.copyright-page p {
    margin: 0.3em 0;
}

.toc-title {
    text-align: center;
    font-size: 1.4em;
    margin-bottom: 1.5em;
}

.toc-list {
    list-style: none;
    padding: 0;
}

.toc-list li {
    margin: 0.5em 0;
}

.toc-list a {
    text-decoration: none;
    color: #333;
}
'''


def generate_epub(book_id, book_path, output_path):
    """Generate EPUB for a book"""

    # Load metadata and content
    metadata = load_book_metadata(book_path)
    chapters = load_book_content(book_path)

    book_title = metadata.get('title', 'Untitled')
    subtitle = metadata.get('subtitle', '')

    # Create EPUB book
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier(f'vedabase-{book_id}')
    book.set_title(book_title)
    book.set_language('en')
    book.add_author('A.C. Bhaktivedanta Swami Prabhupada')

    # Add metadata
    book.add_metadata('DC', 'publisher', 'Vedabase Original Edition')
    book.add_metadata('DC', 'date', metadata.get('first_edition_year', '1972'))
    book.add_metadata('DC', 'description',
        f'Original unedited edition of {book_title}, as published during the author\'s lifetime.')
    book.add_metadata('DC', 'subject', 'Hinduism')
    book.add_metadata('DC', 'subject', 'Vedic Philosophy')
    book.add_metadata('DC', 'subject', 'Krishna Consciousness')

    # Add CSS
    css = epub.EpubItem(
        uid='style',
        file_name='style/main.css',
        media_type='text/css',
        content=create_epub_css()
    )
    book.add_item(css)

    # Create title page
    title_content = f'''
    <html>
    <head><link rel="stylesheet" href="style/main.css" type="text/css"/></head>
    <body>
    <div class="title-page">
        <h1>{book_title}</h1>
        {f'<p class="subtitle">{subtitle}</p>' if subtitle else ''}
        <p class="author">His Divine Grace</p>
        <p class="author"><strong>A.C. Bhaktivedanta Swami Prabhupada</strong></p>
        <p style="margin-top: 3em; font-size: 0.9em;">Vedabase Original Edition</p>
    </div>
    </body>
    </html>
    '''

    title_page = epub.EpubHtml(title='Title Page', file_name='title.xhtml')
    title_page.content = title_content
    title_page.add_item(css)
    book.add_item(title_page)

    # Create copyright page
    copyright_content = f'''
    <html>
    <head><link rel="stylesheet" href="style/main.css" type="text/css"/></head>
    <body>
    <div class="copyright-page">
        <p><em>{book_title}</em></p>
        {f'<p><em>{subtitle}</em></p>' if subtitle else ''}
        <p>&nbsp;</p>
        <p>By His Divine Grace A.C. Bhaktivedanta Swami Prabhupada</p>
        <p>Founder-Acarya of the International Society for Krishna Consciousness</p>
        <p>&nbsp;</p>
        <p>First Edition: {metadata.get('first_edition_year', '1972')}</p>
        <p>This Edition: {datetime.now().year}</p>
        <p>&nbsp;</p>
        <p>Original unrevised edition</p>
        <p>Published under license from Krishna Books Inc.</p>
        <p>&nbsp;</p>
        <p><strong>Vedabase Original Edition</strong></p>
        <p>vedabase.bhaktiyoga.es</p>
    </div>
    </body>
    </html>
    '''

    copyright_page = epub.EpubHtml(title='Copyright', file_name='copyright.xhtml')
    copyright_page.content = copyright_content
    copyright_page.add_item(css)
    book.add_item(copyright_page)

    # Create chapters
    epub_chapters = []

    for chapter in chapters:
        chapter_num = chapter.get('number', '')
        chapter_title = chapter.get('title', 'Untitled')
        chapter_body = chapter.get('body', '')

        # Create chapter HTML
        chapter_content = f'''
        <html>
        <head><link rel="stylesheet" href="style/main.css" type="text/css"/></head>
        <body>
        <div class="chapter">
            {f'<p class="chapter-number">Chapter {chapter_num}</p>' if chapter_num else ''}
            <h1 class="chapter-title">{chapter_title}</h1>
            {chapter_body}
        </div>
        </body>
        </html>
        '''

        # Create EPUB chapter
        epub_chapter = epub.EpubHtml(
            title=f'Chapter {chapter_num}: {chapter_title}' if chapter_num else chapter_title,
            file_name=f'chapter_{chapter_num or len(epub_chapters)+1}.xhtml'
        )
        epub_chapter.content = chapter_content
        epub_chapter.add_item(css)
        book.add_item(epub_chapter)
        epub_chapters.append(epub_chapter)

    # Create about the author page
    about_content = '''
    <html>
    <head><link rel="stylesheet" href="style/main.css" type="text/css"/></head>
    <body>
    <h2>About the Author</h2>
    <p>His Divine Grace A.C. Bhaktivedanta Swami Prabhupada appeared in this world in 1896 in Calcutta, India. He first met his spiritual master, Srila Bhaktisiddhanta Sarasvati Gosvami, in Calcutta in 1922.</p>
    <p>At their first meeting, Srila Bhaktisiddhanta Sarasvati requested Srila Prabhupada to broadcast Vedic knowledge in English. In the years that followed, Srila Prabhupada wrote a commentary on the Bhagavad-gita, assisted the Gaudiya Matha in its work, and in 1944 started Back to Godhead, an English fortnightly magazine.</p>
    <p>In 1965, at the age of sixty-nine, Srila Prabhupada traveled to New York City aboard a cargo ship. After almost a year of great difficulty, he established the International Society for Krishna Consciousness in July 1966.</p>
    <p>Before passing away on November 14, 1977, he had guided ISKCON and seen it grow to a worldwide confederation of more than one hundred asramas, schools, temples, institutes, and farm communities.</p>
    </body>
    </html>
    '''

    about_page = epub.EpubHtml(title='About the Author', file_name='about.xhtml')
    about_page.content = about_content
    about_page.add_item(css)
    book.add_item(about_page)

    # Define table of contents
    book.toc = [
        epub.Link('title.xhtml', 'Title Page', 'title'),
        epub.Link('copyright.xhtml', 'Copyright', 'copyright'),
    ] + [
        epub.Link(ch.file_name, ch.title, f'ch{i}')
        for i, ch in enumerate(epub_chapters)
    ] + [
        epub.Link('about.xhtml', 'About the Author', 'about'),
    ]

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define spine
    book.spine = ['nav', title_page, copyright_page] + epub_chapters + [about_page]

    # Write EPUB file
    epub.write_epub(output_path, book)
    print(f"EPUB generated: {output_path}")

    return output_path


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
                        output_path = os.path.join(OUTPUT_DIR, f"{book_id}_vedabase.epub")
                        generate_epub(book_id, book_path, output_path)
                        sys.exit(0)

        print(f"Book not found: {book_id}")
    else:
        # Default to Raja-vidya
        book_path = os.path.join(BOOKS_DIR, 'introductory', 'I-01_raja_vidya')
        if os.path.exists(book_path):
            output_path = os.path.join(OUTPUT_DIR, "I-01_raja_vidya_vedabase.epub")
            generate_epub("I-01", book_path, output_path)
        else:
            print("Raja-vidya not found. Run with book ID:")
            print("  python generate_epub.py I-01")
