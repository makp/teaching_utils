"""Use GPT model to convert questions to JSON format."""

import os

from openai import OpenAI

client = OpenAI()

INSTRUCTION_MAIN = """
Please convert the provided questions into the JSON format as outlined
below:

[
    {
        "question_type": "",
        "question": "",
        "mc_options": [],
        "correct_answer": "",
        "subject": [],
        "notes": ""
    }
]

- "question_type": This key accepts one of two values: "TF" for
  true/false questions or "MC" for multiple choice questions.
- "question": Insert the text of the question here as a string.
- "mc_options": If the question is of type "TF", this key should
  contain an empty list `[]`. For multiple choice questions, populate
  this list with the answer options, each formatted as a string.
- "correct_answer": This key holds the correct answer to the
  question. For multiple choice questions, the value should match one
  of the strings listed in "mc_options".
- "subject": Populate this key with a list of strings that represent
  the topics or subjects relevant to the question.
- "notes": Use this key to add any supplementary notes or comments,
  formatted as a string.
"""

INSTRUCTION_NORMATIVE_ETHICS = """
For the "subject" key, use concise descriptors, ideally one or two
words, to describe the topic of the question. Examples of such topics
are: 'consequentialism', 'utilitarianism', 'deontology', 'social
contract', and 'hedonism'.
"""

INSTRUCTION_GENERIC = """
For the "subject" key, use concise descriptors, ideally one or two
words, to describe the topic of the question.
"""

MODEL_ASSISTANT = os.environ.get("OPENAI_ADVANCED")

if not MODEL_ASSISTANT:
    raise ValueError("Please set the environment variable with GPT model.")


def convert_questions_to_json_via_gpt(
    questions,
    output_file=None,
    special_instruction="INSTRUCTION_GENERIC",
    model=MODEL_ASSISTANT,
    temperature=0.5,
):
    """
    Use GPT model to convert questions to JSON format.

    This function takes either a string containing questions or a file
    path to a text file containing questions. It uses the specified
    GPT model to generate JSON-formatted content from those questions
    and prints the content.
    """
    if os.path.isfile(questions):
        with open(questions, "r") as f:
            content = f.read()
    else:
        content = questions

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        # response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "\n".join([INSTRUCTION_MAIN, special_instruction]),
            },
            {"role": "user", "content": content},
        ],
    )

    out = response.choices[0].message.content

    if output_file:
        with open(output_file, "w") as f:
            f.write(str(out))
        return print(f"File saved to {output_file}")
    else:
        return print(out)


if __name__ == "__main__":
    base_name = "XXX"  # Insert the base name of the file
    raw_questions = f"/tmp/{base_name}.org"
    tophat_questions = f"/tmp/{base_name}.org"
    convert_questions_to_json_via_gpt(
        questions=raw_questions,
        output_file=tophat_questions,
    )
