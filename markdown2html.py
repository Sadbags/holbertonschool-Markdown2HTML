#!/usr/bin/python3
"""
Converts Markdown to HTML.
"""

import sys
import os
import re
import hashlib


def main():
    """
    Converts a markdown file to HTML.
    """
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} README.md README.html", file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    output_filename = sys.argv[2]

    if not os.path.exists(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    with open(md_file, 'r') as f:
        lines = f.read().splitlines()

    html_lines = []
    in_ul = False
    in_ol = False
    in_p = False
    p_buf = []

    def process_inline(text):
        """Apply inline markdown formatting to text."""
        def md5_replace(m):
            inner = m.group(1).encode('utf-8')
            return hashlib.md5(inner).hexdigest()

        text = re.sub(r'\[\[(.+?)\]\]', md5_replace, text)

        def remove_c(m):
            return re.sub(r'(?i)c', '', m.group(1))

        text = re.sub(r'\(\((.+?)\)\)', remove_c, text)
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)

        return text

    def flush_paragraph():
        """Flush buffered paragraph lines to HTML."""
        nonlocal in_p, p_buf
        if not p_buf:
            return
        html_lines.append('<p>')
        for idx, pline in enumerate(p_buf):
            if idx > 0:
                html_lines.append('<br/>')
            html_lines.append(process_inline(pline))
        html_lines.append('</p>')
        p_buf = []
        in_p = False

    def close_lists():
        """Close open unordered or ordered lists."""
        nonlocal in_ul, in_ol
        if in_ul:
            html_lines.append('</ul>')
            in_ul = False
        if in_ol:
            html_lines.append('</ol>')
            in_ol = False

    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            flush_paragraph()
            close_lists()
            level = len(m.group(1))
            content = process_inline(m.group(2))
            html_lines.append(f'<h{level}>{content}</h{level}>')
            continue

        m = re.match(r'^-\s+(.*)', line)
        if m:
            flush_paragraph()
            if in_ol:
                html_lines.append('</ol>')
                in_ol = False
            if not in_ul:
                html_lines.append('<ul>')
                in_ul = True
            item = process_inline(m.group(1))
            html_lines.append(f'<li>{item}</li>')
            continue

        m = re.match(r'^\*\s+(.*)', line)
        if m:
            flush_paragraph()
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            if not in_ol:
                html_lines.append('<ol>')
                in_ol = True
            item = process_inline(m.group(1))
            html_lines.append(f'<li>{item}</li>')
            continue

        if line.strip() == '':
            flush_paragraph()
            close_lists()
            continue

        if not in_p:
            in_p = True
            p_buf = []
        p_buf.append(line)

    flush_paragraph()
    close_lists()

    with open(output_filename, 'w') as f:
        f.write('\n'.join(html_lines))

    sys.exit(0)


if __name__ == "__main__":
    main()
