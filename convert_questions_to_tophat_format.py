#! /usr/bin/env python3

"""Convert JSON-formatted questions to a text file in TopHat format."""

import argparse
import json


def get_option_letters(n):
    """Return a list of letters to use as multiple choice options."""
    return [chr(i) for i in range(ord("a"), ord("a") + n)]


def mark_correct_answer(answers, idx):
    """Mark the correct answer with an asterisk."""
    if idx is not None:
        answers[idx] = f"*{answers[idx]}"
    return answers


def get_correct_answer_index(options, correct_answer):
    """Return the index of the correct answer."""
    # if pd.isna(correct_answer):
    #     return None
    if correct_answer in [True, False]:  # if I forgot to add quotes
        correct_answer = str(correct_answer)
    return options.index(correct_answer) if correct_answer else None


def format_question(q, index):
    """Format a question in TopHat format."""
    options = q["mc_options"]
    if q["question_type"] == "TF":
        options = ["True", "False"]

    idx = get_correct_answer_index(options, q["correct_answer"])
    answers = mark_correct_answer(
        [
            f"{char}. {option}\n"
            for char, option in zip(get_option_letters(len(options)), options)
        ],
        idx,
    )
    return f"{index}. {q['question']}\n{''.join(answers)}"


def write_formatted_questions_from_json(json_path, filename="output.txt"):
    """Write formatted questions to a text file."""
    with open(json_path, "r") as f:
        questions = json.load(f)

    formatted_questions = [
        format_question(q, idx + 1) for idx, q in enumerate(questions)
    ]

    with open(filename, "w") as file:
        for item in formatted_questions:
            file.write(f"{item}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert JSON-formatted questions to TopHat format."
    )

    parser.add_argument("json_path", help="Path to JSON file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output file to write questions to",
        default="/tmp/questions_in_tophat_format.txt",
    )

    args = parser.parse_args()

    write_formatted_questions_from_json(json_path=args.json_path, filename=args.output)
