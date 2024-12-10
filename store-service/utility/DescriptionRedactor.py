      
import bleach

ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'strike', 'a', 'img', 'h1', 
								'h2', 'h3', 'ul', 'ol', 'li', 'blockquote']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title'], 'img': ['src', 'alt']}

def sanitize_html(html):
	cleaned_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
	return cleaned_html
