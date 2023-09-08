from bs4 import BeautifulSoup
import os


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()


def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


def embed_css_in_html(html_content, htlm_dir):
    soup = BeautifulSoup(html_content, 'html.parser')

    for link_tag in soup.find_all('link', {'rel': 'stylesheet'}):
        relative_css_path = link_tag['href']
        absolute_css_path = os.path.join(htlm_dir, relative_css_path)
        css_content = read_file(absolute_css_path)

        style_tag = soup.new_tag('style', type='text/css')
        style_tag.string = css_content
        link_tag.replace_with(style_tag)

    return str(soup)


def generate_embedded_html_file(html_path):
    html_dir = os.path.dirname(html_path)
    html_content = read_file(html_path)
    new_html_content = embed_css_in_html(html_content, html_dir)
    new_html_file = f"embedded_{os.path.basename(html_path)}"
    write_file(new_html_file, new_html_content)
    print(f"CSS has been embedded into the new HTML file: {new_html_file}")
