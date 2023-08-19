from jinja2 import Environment, FileSystemLoader
import os
import subprocess
from teaching_data.syllabi_data import syllabi_data


# Set up Jinja2 env
sections_path = os.path.abspath('./teaching_data/syllabus_sections')
env = Environment(loader=FileSystemLoader(sections_path))
template = env.get_template('syllabus.j2')


def create_syllabi(semester):
    lst_tex_files = []
    for idx, syllabus_vars in enumerate(syllabi_data[semester]):
        base = f"syllabus_{semester}_{syllabus_vars['course_code'].lower()}-{idx + 1}"
        folder_name = "./teaching_data/" + base

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        output = template.render(syllabus_vars)
        full_path = f"{folder_name}/{base}.tex"
        with open(full_path, 'w') as file:
            file.write(output)
        lst_tex_files.append(full_path)
    return lst_tex_files


def run_pdflatex(tex_files):
    for tex in tex_files:
        try:
            folder = os.path.dirname(tex)
            subprocess.run(['pdflatex', os.path.basename(tex)],
                           check=True, cwd=folder)
        except subprocess.CalledProcessError as e:
            print("Error running pdflatex:", e)

        for ext in ['aux', 'log', 'out']:
            try:
                root, _ = os.path.splitext(tex)
                os.remove(f"{root}.{ext}")
            except FileNotFoundError:
                pass
