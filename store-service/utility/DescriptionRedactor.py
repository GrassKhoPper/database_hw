"""
This module provides functional for cleaning HTML content. It uses the bleach library to strip unauthorized HTML tags and attributes.

"""      

import bleach

ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'strike', 'a', 'img', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'blockquote']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title'], 'img': ['src', 'alt']}

def sanitize_html(html):
	"""
    Sanitize HTML content by removing unauthorized tags and attributes (not explicitly allowed in ALLOWED_TAGS and ALLOWED_ATTRIBUTES)

    Args:
        html (str): The input HTML to be sanitized

    Returns:
        str: Cleaned HTML containing only allowed tags and attributes
    """
	cleaned_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
	return cleaned_html
