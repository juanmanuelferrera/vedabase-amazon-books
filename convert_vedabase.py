#!/usr/bin/env python3
"""
Convert Vedabase markdown format to interior generator format
"""

import re
import os

# Chapter titles from TOC
RAJA_VIDYA_CHAPTERS = {
    1: "Raja-Vidya: The King of Knowledge",
    2: "Knowledge Beyond Samsara",
    3: "Knowledge of Krsna's Energies",
    4: "Knowledge by Way of the Mahatmas, Great Souls",
    5: "Parampara: Knowledge Through Disciplic Succession",
    6: "Knowledge of Krsna's Appearances and Activities",
    7: "Knowledge as Faith in Guru and Surrender to Krsna",
    8: "Action in Knowledge of Krsna",
}

def convert_raja_vidya(input_path, output_path):
    """Convert Raja-vidya markdown to generator format"""

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # Find chapter boundaries
    chapter_starts = []
    for i, line in enumerate(lines):
        if line.startswith('Chapter ') and line.split()[1].lower() in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']:
            chapter_starts.append(i)

    chapter_starts.append(len(lines))  # End marker

    # Word to number mapping
    word_to_num = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8
    }

    output_lines = []

    for idx in range(len(chapter_starts) - 1):
        start = chapter_starts[idx]
        end = chapter_starts[idx + 1]

        # Get chapter number from line
        chapter_line = lines[start]
        chapter_word = chapter_line.split()[1].lower()
        chapter_num = word_to_num.get(chapter_word, idx + 1)

        # Get chapter title
        chapter_title = RAJA_VIDYA_CHAPTERS.get(chapter_num, f"Chapter {chapter_num}")

        # Add chapter header in new format
        output_lines.append(f"# Chapter {chapter_num}: {chapter_title}")
        output_lines.append("")

        # Skip the original chapter line and any title lines that follow
        body_start = start + 1

        # Skip empty lines and the repeated title
        while body_start < end and (not lines[body_start].strip() or
               lines[body_start].strip() in RAJA_VIDYA_CHAPTERS.values() or
               lines[body_start].strip().startswith('Rāja-Vidyā') or
               lines[body_start].strip().startswith('Raja-Vidya')):
            body_start += 1

        # Add the chapter body
        for i in range(body_start, end):
            output_lines.append(lines[i])

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"Converted: {output_path}")
    print(f"Chapters: {len(chapter_starts) - 1}")


if __name__ == '__main__':
    input_file = 'raja-vidya-temp/raja-vidya.md'
    output_file = 'books/introductory/I-01_raja_vidya/content.md'

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    convert_raja_vidya(input_file, output_file)
