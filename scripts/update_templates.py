from pathlib import Path

base = Path(__file__).resolve().parent.parent / 'templates'
for html in sorted(base.glob('*.html')):
    text = html.read_text(encoding='utf-8')
    if '{% load static %}' not in text:
        text = text.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n{% load static %}', 1)
    text = text.replace('href="style.css"', 'href="{% static \'style.css\' %}"')
    text = text.replace('src="auth.js"', 'src="{% static \'auth.js\' %}"')
    html.write_text(text, encoding='utf-8')
    print(f'Updated {html.name}')
