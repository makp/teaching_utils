#! /usr/bin/env python3

import argparse

import pymupdf


def extract_pdftext_with_pymupdf(pdf_path):
    with pymupdf.open(pdf_path) as pdf:
        text = "\n".join([page.get_text() for page in pdf])  # type: ignore
    return text.strip()


def extract_pdftext_with_tesseract(pdf_path):
    with pymupdf.open(pdf_path) as doc:
        text = "\n".join(
            [
                page.get_textpage_ocr(  # type: ignore
                    language="eng", tessdata="/usr/share/tessdata/"
                ).extractText()
                for page in doc
            ]
        )
    return text.strip()


def extract_pdftext(pdf_path, use_tesseract=False):
    if use_tesseract:
        out = extract_pdftext_with_tesseract(pdf_path)
    else:
        out = extract_pdftext_with_pymupdf(pdf_path)
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from PDF.")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument(
        "-t", "--tesseract", help="Use Tesseract to extract text", default=False
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file to write text to",
        default=None,
    )

    args = parser.parse_args()

    content = extract_pdftext(args.pdf_path, use_tesseract=args.tesseract)

    if args.output:
        with open(args.output, "w") as f:
            f.write(content)
    else:
        print(content)
