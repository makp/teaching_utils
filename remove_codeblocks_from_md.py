#! /usr/bin/env python3

import os
import re
import sys


def clean_markdown(file_path):
    with open(file_path, "r") as file:
        md_content = file.read()

    pattern = re.compile(r"```comment([\s\S]*?)```", re.MULTILINE)
    md_cleaned = re.sub(pattern, "", md_content)

    file_out = f"{os.path.splitext(file_path)[0]}_out{os.path.splitext(file_path)[1]}"
    with open(file_out, "w") as file:
        file.write(md_cleaned)

    print(f"Cleaned file saved as: {file_out}")

    return file_out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_markdown.py <path_to_markdown_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    clean_markdown(file_path)
