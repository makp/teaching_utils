#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import os
import subprocess
from teaching_data.syllabi_data import syllabi_data, CURRENT_SEMESTER


# Set up Jinja2 env
sections_path = os.path.abspath('./teaching_data')
env = Environment(loader=FileSystemLoader(sections_path))
template = env.get_template('door_schedule.j2')


def create_door_schedule(semester):
    folder_path = "./teaching_data/door_schedule"
    file_name = f"door-schedule_{semester}.tex"
    full_path = os.path.join(folder_path, file_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    data = syllabi_data[semester]
    output = template.render(data=data)

    with open(full_path, 'w') as f:
        f.write(output)

    return full_path


def run_pdflatex(full_path):
    try:
        folder = os.path.dirname(full_path)
        subprocess.run(['pdflatex', os.path.basename(full_path)],
                       check=True, cwd=folder)
    except subprocess.CalledProcessError as e:
        print("Error running pdflatex:", e)

    for ext in ['aux', 'log', 'out']:
        try:
            root, _ = os.path.splitext(full_path)
            os.remove(f"{root}.{ext}")
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    full_path = create_door_schedule(CURRENT_SEMESTER)
    run_pdflatex(full_path)
