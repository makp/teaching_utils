#! /usr/bin/env python3

import argparse
import base64
import os

from bs4 import BeautifulSoup


def read_file(filename, mode="r"):
    with open(filename, mode) as file:
        return file.read()


def write_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def embed_assets_in_html(html_content, htlm_dir):
    soup = BeautifulSoup(html_content, "html.parser")

    # Embed CSS
    for link_tag in soup.find_all("link", {"rel": "stylesheet"}):
        relative_css_path = link_tag["href"]
        absolute_css_path = os.path.join(htlm_dir, relative_css_path)
        css_content = read_file(absolute_css_path)

        style_tag = soup.new_tag("style", type="text/css")
        style_tag.string = css_content
        link_tag.replace_with(style_tag)

    # Embed images
    for img_tag in soup.find_all("img"):
        relative_img_path = img_tag["src"]
        absolute_img_path = os.path.join(htlm_dir, relative_img_path)
        img_extension = os.path.splitext(absolute_img_path)[1][1:]
        img_base64 = encode_image_to_base64(absolute_img_path)
        img_tag["src"] = f"data:image/{img_extension};base64,{img_base64}"

    return str(soup)


def generate_embedded_html_file(html_path):
    html_dir = os.path.dirname(html_path)
    html_content = read_file(html_path)
    new_html_content = embed_assets_in_html(html_content, html_dir)
    new_html_file = f"embedded_{os.path.basename(html_path)}"
    write_file(new_html_file, new_html_content)
    print(f"Assets have been embedded into the new HTML file: {new_html_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed CSS and images into HTML file")
    parser.add_argument("html_path", help="Path to HTML file to embed assets into")
    args = parser.parse_args()

    generate_embedded_html_file(args.html_path)
