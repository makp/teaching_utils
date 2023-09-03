import json
import ast


def get_option_letters(n):
    return [chr(i) for i in range(ord('a'), ord('a') + n)]


def mark_correct_answer(answers, idx):
    if idx is not None:
        answers[idx] = f"*{answers[idx]}"
    return answers


def get_correct_answer_index(options, correct_answer):
    # if pd.isna(correct_answer):
    #     return None
    if correct_answer in [True, False]:  # if I forgot to add quotes
        correct_answer = str(correct_answer)
    return options.index(correct_answer) if correct_answer else None


def format_question(q, index):
    options = q['mc_options']
    if q['question_type'] == 'TF':
        options = ['True', 'False']

    idx = get_correct_answer_index(options, q['correct_answer'])
    answers = mark_correct_answer(
        [f"{char}. {option}\n" for char, option in zip(get_option_letters(len(options)), options)], idx)
    return f"{index}. {q['question']}\n{''.join(answers)}"


def write_formatted_questions_from_json(json_path, filename="output.txt"):
    with open(json_path, 'r') as f:
        questions = json.load(f)

    formatted_questions = [format_question(q, idx+1) for idx, q in enumerate(questions)]

    with open(filename, "w") as file:
        for item in formatted_questions:
            file.write(f"{item}\n")

# def write_formatted_questions_from_df(df, filename="output.txt"):
#     mask = df['mc_options'].apply(lambda x: isinstance(x, str))
#     if mask.any():
#         df.loc[mask, 'mc_options'] = df.loc[mask, 'mc_options'].apply(ast.literal_eval)
#     formatted_questions = [format_question(row, idx+1)
#                            for idx, (_, row) in enumerate(df.iterrows())]
#     with open(filename, "w") as file:
#         for item in formatted_questions:
#             file.write(f"{item}\n")
