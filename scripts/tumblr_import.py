#!/usr/bin/env python3
"""
Tumblr Post Importer for Lektor

Usage:
    python3 scripts/tumblr_import.py <tumblr_url> [url2] ...

Example:
    python3 scripts/tumblr_import.py https://miratcan.tumblr.com/day/2013/10/30
    python3 scripts/tumblr_import.py https://miratcan.tumblr.com/post/65521920605

Supported post types: text, quote, photo, video, link
(audio is not supported)
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

CONTENT_DIR = Path(__file__).parent.parent / "content" / "articles"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

POST_TYPES = {
    'text-post': 'text',
    'quote-post': 'quote',
    'photo-post': 'photo',
    'video-post': 'video',
    'link-post': 'link',
}


def slugify(text):
    text = text.lower().strip()
    for old, new in [('ğ','g'),('ü','u'),('ş','s'),('ı','i'),('ö','o'),('ç','c')]:
        text = text.replace(old, new)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:60]


def fetch(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def caption_to_markdown(el):
    """Convert Tumblr caption/body HTML to markdown."""
    if not el:
        return ''

    parts = []
    for child in el.children:
        if not hasattr(child, 'name') or not child.name:
            text = str(child).strip()
            if text:
                parts.append(text)
            continue

        if child.name == 'blockquote':
            bq_text = child.get_text(strip=True)
            parts.append('> ' + bq_text)
        elif child.name == 'p':
            text = ''
            for c in child.children:
                if hasattr(c, 'name') and c.name == 'a':
                    href = c.get('href', '')
                    link_text = c.get_text()
                    text += f'[{link_text}]({href})'
                else:
                    text += str(c)
            parts.append(text.strip())
        elif child.name in ('h1', 'h2', 'h3'):
            level = int(child.name[1])
            parts.append('#' * level + ' ' + child.get_text(strip=True))
        elif child.name == 'ul':
            for li in child.find_all('li'):
                parts.append('- ' + li.get_text(strip=True))
        elif child.name == 'ol':
            for i, li in enumerate(child.find_all('li'), 1):
                parts.append(f'{i}. ' + li.get_text(strip=True))

    return '\n\n'.join(parts)


def parse_date(info_div):
    """Extract date from info div."""
    if not info_div:
        return ''
    date_link = info_div.find('a')
    if not date_link:
        return ''
    date_text = date_link.get_text(strip=True)
    match = re.search(r'(\w+ \d+,?\s*\d{4})', date_text)
    if not match:
        return ''
    for fmt in ('%b %d, %Y', '%b %d %Y'):
        try:
            return datetime.strptime(match.group(1), fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return ''


def parse_tags(article):
    """Extract tags from article."""
    tags_div = article.find('div', class_='tags')
    if not tags_div:
        return []
    return [a.get_text(strip=True).lstrip('#') for a in tags_div.find_all('a') if a.get_text(strip=True)]


def get_photoset_images(iframe_src, base_url):
    """Fetch images from a photoset iframe."""
    if iframe_src.startswith('/'):
        parsed = urlparse(base_url)
        iframe_url = f"{parsed.scheme}://{parsed.netloc}{iframe_src}"
    else:
        iframe_url = iframe_src

    soup = BeautifulSoup(fetch(iframe_url), 'html.parser')
    images = []
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src and 'media.tumblr.com' in src:
            src = re.sub(r'_\d+\.', '_1280.', src)
            images.append(src)
    return images


def detect_post_type(article):
    """Detect Tumblr post type from article classes."""
    classes = article.get('class') or []
    for cls, ptype in POST_TYPES.items():
        if cls in classes:
            return ptype
    return None


def extract_text_post(article):
    """Extract a text post."""
    post = {'type': 'text', 'body': '', 'title': ''}

    # Text posts may have a title
    title_div = article.find('div', class_='title')
    if title_div:
        post['title'] = title_div.get_text(strip=True)

    body_div = article.find('div', class_='body')
    if body_div:
        post['body'] = caption_to_markdown(body_div)
    else:
        caption = article.find('div', class_='caption')
        if caption:
            post['body'] = caption_to_markdown(caption)

    return post


def extract_quote_post(article):
    """Extract a quote post."""
    post = {'type': 'quote', 'body': ''}

    quote_div = article.find('div', class_='quote')
    source_div = article.find('div', class_='source')

    quote_text = quote_div.get_text(strip=True) if quote_div else ''
    source_text = source_div.get_text(strip=True) if source_div else ''

    body = quote_text
    if source_text:
        body += f'\n\n— {source_text}'
    post['body'] = body

    return post


def extract_photo_post(article, page_url):
    """Extract a photo post."""
    post = {'type': 'photo', 'body': '', 'images': []}

    # Single photo
    legacy_photo = article.find('div', class_='legacy-photo')
    if legacy_photo:
        img = legacy_photo.find('img')
        if img and img.get('src'):
            src = re.sub(r'_\d+\.', '_1280.', img['src'])
            post['images'].append(src)

    # Photoset
    legacy_photoset = article.find('div', class_='legacy-photoset')
    if legacy_photoset:
        iframe = legacy_photoset.find('iframe')
        if iframe and iframe.get('src'):
            post['images'] = get_photoset_images(iframe['src'], page_url)

    # Caption
    caption = article.find('div', class_='caption')
    post['body'] = caption_to_markdown(caption)

    return post


def extract_video_post(article):
    """Extract a video post."""
    post = {'type': 'video', 'body': '', 'video_url': ''}

    # Find YouTube iframe
    for iframe in article.find_all('iframe'):
        src = iframe.get('src', '')
        if 'youtube.com/embed' in src:
            post['video_url'] = src.split('?')[0]  # clean URL
            break
        if 'player.vimeo.com' in src:
            post['video_url'] = src.split('?')[0]
            break

    # Caption
    caption = article.find('div', class_='caption')
    caption_md = caption_to_markdown(caption)

    # Build body with video embed + caption
    parts = []
    if post['video_url']:
        parts.append(f'<iframe class="youtube-video" src="{post["video_url"]}" frameborder="0" allowfullscreen></iframe>')
    if caption_md:
        parts.append(caption_md)

    post['body'] = '\n\n'.join(parts)
    return post


def extract_link_post(article):
    """Extract a link post."""
    post = {'type': 'text', 'body': ''}  # links become text posts

    link_div = article.find('div', class_='link')
    caption = article.find('div', class_='caption')

    parts = []
    if link_div:
        a = link_div.find('a')
        if a:
            href = a.get('href', '')
            text = a.get_text(strip=True)
            parts.append(f'[{text}]({href})')

    if caption:
        parts.append(caption_to_markdown(caption))

    post['body'] = '\n\n'.join(parts)
    return post


def extract_posts(html, page_url):
    """Extract all posts from a Tumblr page."""
    soup = BeautifulSoup(html, 'html.parser')
    posts = []

    for article in soup.find_all('article'):
        ptype = detect_post_type(article)
        if not ptype:
            continue

        if ptype == 'text':
            post = extract_text_post(article)
        elif ptype == 'quote':
            post = extract_quote_post(article)
        elif ptype == 'photo':
            post = extract_photo_post(article, page_url)
        elif ptype == 'video':
            post = extract_video_post(article)
        elif ptype == 'link':
            post = extract_link_post(article)
        else:
            continue

        # Common fields
        info_div = article.find('div', class_='info')
        post['date'] = parse_date(info_div)
        post['tumblr_tags'] = parse_tags(article)

        posts.append(post)

    return posts


def download_image(url, dest_path):
    """Download an image."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(resp.content)
        print(f"    {dest_path.name} ({len(resp.content) // 1024}KB)")
        return True
    except Exception as e:
        print(f"    FAILED {url}: {e}")
        return False


def create_post(post, slug):
    """Create Lektor article from extracted post data."""
    post_dir = CONTENT_DIR / slug
    if post_dir.exists():
        resp = input(f"  '{slug}' already exists. Overwrite? [y/N] ").strip().lower()
        if resp != 'y':
            return False

    post_dir.mkdir(parents=True, exist_ok=True)

    ptype = post['type']

    # Download images for photo posts
    if ptype == 'photo':
        print("  Downloading images:")
        downloaded = []
        for i, img_url in enumerate(post.get('images', []), 1):
            ext = '.jpg'
            if '.png' in img_url:
                ext = '.png'
            elif '.gif' in img_url:
                ext = '.gif'
            filename = f"photo-{i}{ext}"
            if download_image(img_url, post_dir / filename):
                downloaded.append(filename)
        if not downloaded:
            print("  No images downloaded, skipping.")
            return False

    # Title
    title = post.get('title', '')
    if not title:
        body_preview = post['body'][:80].replace('\n', ' ') if post['body'] else '(no text)'
        print(f"  Preview: {body_preview}")
        title = input("  Title: ").strip()
    if not title:
        title = slug.replace('-', ' ').title()

    pub_date = post.get('date', '')
    if not pub_date:
        pub_date = input("  Date (YYYY-MM-DD): ").strip()

    # Tags: post type tag + personal
    lektor_tags = ['personal']
    if ptype in ('photo', 'quote', 'video'):
        lektor_tags.append(ptype)

    meta_desc = post['body'][:150].replace('\n', ' ').strip() if post['body'] else title

    # Build contents.lr
    contents = f"title: {title}\n"
    contents += "---\n"
    contents += "body:\n\n"
    contents += post['body'] + "\n"
    contents += "---\n"
    contents += f"pub_date: {pub_date}\n"
    contents += "---\n"
    contents += "tags:\n\n"
    contents += '\n'.join(lektor_tags) + '\n'
    contents += "---\n"
    contents += f"meta_desc: {meta_desc}\n"
    contents += "---\n"
    contents += "language: tr\n"

    (post_dir / 'contents.lr').write_text(contents, encoding='utf-8')

    img_count = len(post.get('images', []))
    extra = f", {img_count} images" if img_count else ""
    print(f"  Created: {slug}/ (type={ptype}{extra})")
    return True


def main():
    if len(sys.argv) < 2:
        print("Tumblr Importer for Lektor")
        print()
        print("Usage: python3 scripts/tumblr_import.py <url1> [url2] ...")
        print()
        print("Supported: text, quote, photo, video, link posts")
        print("Not supported: audio posts")
        print()
        print("Examples:")
        print("  python3 scripts/tumblr_import.py https://miratcan.tumblr.com/day/2013/10/30")
        print("  python3 scripts/tumblr_import.py https://miratcan.tumblr.com/post/65521920605")
        sys.exit(1)

    for url in sys.argv[1:]:
        print(f"\n{'='*60}")
        print(f"Fetching: {url}")
        html = fetch(url)
        posts = extract_posts(html, url)

        if not posts:
            print("  No supported posts found on this page.")
            continue

        type_summary = ', '.join(f"{p['type']}" for p in posts)
        print(f"  Found {len(posts)} post(s): [{type_summary}]\n")

        for i, post in enumerate(posts):
            ptype = post['type']
            print(f"--- Post {i+1}/{len(posts)} [{ptype}] ---")
            print(f"  Date: {post.get('date', 'unknown')}")
            if post.get('tumblr_tags'):
                print(f"  Tumblr tags: {', '.join(post['tumblr_tags'][:5])}")
            if ptype == 'photo':
                print(f"  Images: {len(post.get('images', []))}")
            if post.get('body'):
                print(f"  Body: {post['body'][:100].replace(chr(10), ' ')}...")

            action = input("  Slug (or 'skip'): ").strip()
            if action == 'skip':
                print("  Skipped.\n")
                continue

            slug = action if action else slugify(
                post.get('title') or post['body'][:40] or f"post-{i+1}"
            )
            create_post(post, slug)
            print()

    print("\nDone! Run 'lektor build' to rebuild.")


if __name__ == '__main__':
    main()
