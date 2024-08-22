#! /usr/bin/env python3

import argparse
import subprocess

from remove_codeblocks_from_md import clean_markdown


def main():
    parser = argparse.ArgumentParser(description="Convert markdown to HTML.")
    parser.add_argument("file_path", help="Path to markdown file")
    parser.add_argument("-c", "--clean", help="Clean the markdown file", default=True)

    args = parser.parse_args()

    # Clean markdown file?
    if args.clean:
        print("Cleaning markdown file...")
        md_path = clean_markdown(args.file_path)
    else:
        md_path = args.file_path

    # Convert markdown file to HTML
    html_path = f"{md_path}.html"
    subprocess.run(
        ["pandoc", "-s", "-f", "markdown", "-t", "html", md_path, "-o", html_path]
    )
    print(f"HTML file saved as: {html_path}")


if __name__ == "__main__":
    main()
