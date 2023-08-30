import pandas as pd
import ast


def get_option_letters(n):
    return [chr(i) for i in range(ord('a'), ord('a') + n)]


def mark_correct_answer(answers, idx):
    if idx is not None:
        answers[idx] = f"*{answers[idx]}"
    return answers


def get_correct_answer_index(options, correct_answer):
    if pd.isna(correct_answer):
        return None
    return options.index(correct_answer) if correct_answer else None


def format_question(row, index):
    options = row['mc_options']
    if row['question_type'] == 'TF':
        options = ['True', 'False']

    idx = get_correct_answer_index(options, row['correct_answer'])
    answers = mark_correct_answer(
        [f"{char}. {option}\n" for char, option in zip(get_option_letters(len(options)), options)], idx)
    return f"{index}. {row['question']}\n{''.join(answers)}"


def write_formatted_questions(df, filename="output.txt"):
    has_string = df['mc_options'].apply(lambda x: isinstance(x, str)).any()
    if has_string:
        df['mc_options'] = df['mc_options'].apply(ast.literal_eval)
    formatted_questions = [format_question(row, idx+1)
                           for idx, (_, row) in enumerate(df.iterrows())]
    with open(filename, "w") as file:
        for item in formatted_questions:
            file.write(f"{item}\n")
