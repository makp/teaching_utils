"""Convert questions to JSON format using the GPT model."""

import openai
import os

openai.api_key = os.getenv("OPENAI_KEY")

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


def convert_questions_to_json_via_gpt(questions,
                                      output_file=None,
                                      special_instruction="INSTRUCTION_GENERIC",  # noqa
                                      model='gpt-4-1106-preview',
                                      temperature=0.5):
    """
    Convert questions to JSON format using the GPT model.

    This function takes either a string containing questions or a file
    path to a text file containing questions. It uses the specified
    GPT model to generate JSON-formatted content from those questions
    and prints the content.
    """
    if os.path.isfile(questions):
        with open(questions, 'r') as f:
            content = f.read()
    else:
        content = questions

    response = openai.ChatCompletion.create(
        model=model,
        temperature=temperature,
        messages=[{"role": "system", "content":
                   "\n".join([INSTRUCTION_MAIN, special_instruction])},
                  {"role": "user", "content": content}]
    )

    out = response['choices'][0]['message']['content']

    if output_file:
        with open(output_file, 'w') as f:
            f.write(out)
        return print(f"File saved to {output_file}")
    else:
        return print(response['choices'][0]['message']['content'])
