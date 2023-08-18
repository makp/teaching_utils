from jinja2 import Environment, FileSystemLoader
import os
import subprocess
from syllabi_data import syllabi_data


# Set up Jinja2 env
env = Environment(loader=FileSystemLoader('sections'))
template = env.get_template('syllabus.j2')


def create_syllabi(semester):
    lst_folders = []
    for idx, syllabus_vars in enumerate(syllabi_data[semester]):
        folder_name = f"syllabus_{semester}_{syllabus_vars['course_code'].lower()}-{idx + 1}"

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        output = template.render(syllabus_vars)
        with open(f"{folder_name}/{folder_name}.tex", 'w') as file:
            file.write(output)
        lst_folders.append(folder_name)
    return lst_folders


def run_pdflatex(folders):
    for folder in folders:
        try:
            subprocess.run(['pdflatex', folder], check=True, cwd=folder)
        except subprocess.CalledProcessError as e:
            print("Error running pdflatex:", e)

        for ext in ['aux', 'log', 'out']:
            try:
                os.remove(f"{folder}/{folder}.{ext}")
            except FileNotFoundError:
                pass
