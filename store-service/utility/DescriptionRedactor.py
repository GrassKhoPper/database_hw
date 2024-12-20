"""
HTML Sanitization module.

This module provides functionality for sanitizing HTML content by removing potentially 
dangerous tags and attributes while preserving safe formatting elements.
"""      

import bleach

ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'strike', 'h1', 
								'h2', 'h3', 'ul', 'ol', 'li', 'blockquote'] # 'a'
ALLOWED_ATTRIBUTES = {'a': ['href', 'title'], 'img': ['src', 'alt']}

def sanitize_html(html):
	"""
    Sanitizes HTML content by removing unsafe tags and attributes.

    Args:
        html (str): Raw HTML content to be sanitized

    Returns:
        str: Sanitized HTML with only allowed tags and attributes
	"""
	cleaned_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
	return cleaned_html
