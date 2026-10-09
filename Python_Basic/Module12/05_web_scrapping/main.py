# TODO здесь писать код
import re
import urllib.request


def get_h3_regex(file_path: str = None, url: str = None) -> list[str]:
    """
    Извлекает H3 с помощью регулярных выражений.
    """
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    elif url:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8')
    else:
        raise ValueError("Укажите file_path или url")

    pattern = r'<h3[^>]*>(.*?)</h3>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)

    return [match.strip() for match in matches]


print(get_h3_regex('examples.html'))

# В данном случае запрос request.get заменен на загрзку сайта из файла html
with open('examples.html', 'r') as f:
    text = f.read()
# По итогу вы так же получаете код сайта в виде одной строки
