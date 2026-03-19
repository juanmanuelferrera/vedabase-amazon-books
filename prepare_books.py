#!/usr/bin/env python3
"""
Prepare books from downloaded vedabase content
Creates proper directory structure with metadata and content files
"""

import os
import yaml
import re
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, 'downloads')
BOOKS_DIR = os.path.join(BASE_DIR, 'books')

# Book definitions with metadata
BOOKS = {
    'path-of-perfection': {
        'id': 'I-02',
        'title': 'The Path of Perfection',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1979',
        'price_tier': 'M',  # 120-200 pages
    },
    'perfect-questions-perfect-answers': {
        'id': 'I-03',
        'title': 'Perfect Questions, Perfect Answers',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1977',
        'price_tier': 'S',
    },
    'perfection-of-yoga': {
        'id': 'I-04',
        'title': 'The Perfection of Yoga',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1972',
        'price_tier': 'XS',
    },
    'beyond-birth-and-death': {
        'id': 'I-05',
        'title': 'Beyond Birth and Death',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1972',
        'price_tier': 'XS',
    },
    'easy-journey-to-other-planets': {
        'id': 'I-06',
        'title': 'Easy Journey to Other Planets',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1970',
        'price_tier': 'S',
    },
    'elevation-to-krsna-consciousness': {
        'id': 'I-07',
        'title': 'Elevation to Krsna Consciousness',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1973',
        'price_tier': 'S',
    },
    'life-comes-from-life': {
        'id': 'I-08',
        'title': 'Life Comes from Life',
        'subtitle': 'Morning Walks with His Divine Grace A.C. Bhaktivedanta Swami Prabhupada',
        'category': 'introductory',
        'first_edition_year': '1979',
        'price_tier': 'M',
    },
    'light-of-the-bhagavata': {
        'id': 'I-09',
        'title': 'Light of the Bhagavata',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1984',
        'price_tier': 'S',
    },
    'on-the-way-to-krsna': {
        'id': 'I-10',
        'title': 'On the Way to Krsna',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1973',
        'price_tier': 'XS',
    },
    'reservoir-of-pleasure': {
        'id': 'I-11',
        'title': 'The Reservoir of Pleasure',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1972',
        'price_tier': 'XS',
    },
    'topmost-yoga-system': {
        'id': 'I-12',
        'title': 'The Topmost Yoga System',
        'subtitle': None,
        'category': 'introductory',
        'first_edition_year': '1972',
        'price_tier': 'XS',
    },
    'second-chance': {
        'id': 'I-13',
        'title': 'Second Chance',
        'subtitle': 'The Story of a Near-Death Experience',
        'category': 'introductory',
        'first_edition_year': '1991',
        'price_tier': 'M',
    },
}


def prepare_book(slug, info):
    """Prepare a single book directory"""

    # Check if source files exist
    md_file = os.path.join(DOWNLOADS_DIR, f"{slug}.md")
    if not os.path.exists(md_file):
        print(f"  SKIP: {slug} - no source file")
        return False

    # Create book directory
    book_dir = os.path.join(BOOKS_DIR, info['category'], f"{info['id']}_{slug.replace('-', '_')}")
    os.makedirs(book_dir, exist_ok=True)

    # Copy content file
    content_dest = os.path.join(book_dir, 'content.md')
    shutil.copy(md_file, content_dest)

    # Create metadata
    metadata = {
        'title': info['title'],
        'subtitle': info.get('subtitle'),
        'series_id': info['id'],
        'category': info['category'],
        'first_edition_year': info['first_edition_year'],
        'price_tier': info['price_tier'],
        'glossary': []
    }

    meta_path = os.path.join(book_dir, 'metadata.yaml')
    with open(meta_path, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True)

    print(f"  OK: {info['id']} - {info['title']}")
    return True


def main():
    print("Preparing books from downloads...\n")

    success = 0
    for slug, info in BOOKS.items():
        if prepare_book(slug, info):
            success += 1

    print(f"\nPrepared {success}/{len(BOOKS)} books")
    print("\nTo generate PDFs, run:")
    print("  python generate_interior.py <BOOK_ID>")


if __name__ == '__main__':
    main()
