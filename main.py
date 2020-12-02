#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

from pathlib import Path


def display_error_and_exit(error_message):
    print(error_message)
    sys.exit()


def create_project_directory():
    # There should be 3 arguments (this file name will count as one)
    if len(sys.argv) != 3:
        display_error_and_exit("Must pass in project parent directory and project name parameters.")

    project_parent_directory = Path(sys.argv[1])

    if not project_parent_directory.exists():
        display_error_and_exit("Project parent directory does not exist.")

    project_directory_name = sys.argv[2]

    illegal_characters = [".", "/", "\\", "|", "<", ">", "\'", "\"", "{", "}", "[", "]"]

    for illegal_character in illegal_characters:
        if illegal_character in project_directory_name:
            display_error_and_exit("Project name has illegal characters.")

    project_directory_absolute_path = project_parent_directory / project_directory_name

    # If os.mkdir ends up not blocking execution until the directory is made, then use:
    # subprocess.call(["mkdir", project_final_path])
    # We will know if there is ever a situation where future operations fail because this directory
    # hasn't been made yet.
    if project_directory_absolute_path.exists():
        display_error_and_exit("Project already exists")

    os.mkdir(project_directory_absolute_path)

    return project_directory_absolute_path


def add_source_folder(project_directory_absolute_path):
    source_directory_absolute_path = project_directory_absolute_path / "source"
    os.mkdir(source_directory_absolute_path)


def add_template_files(project_directory_absolute_path):
    template_files_directory = Path("./template_files")

    if not template_files_directory.exists():
        raise Exception("Template directory is not valid.")

    template_text_extension = ".template"

    for root, _, template_files in os.walk(template_files_directory):
        for template_file in template_files:
            if template_text_extension in template_file:
                template_file_absolute_path = Path(root, template_file)

                project_file_name = str(template_file).replace(template_text_extension, "")
                project_file_absolute_path = project_directory_absolute_path / project_file_name

                shutil.copy2(template_file_absolute_path, project_file_absolute_path)


def initialize_git_repository(project_directory_absolute_path, should_create_initial_commit=False):
    subprocess.call(["git", "-C", project_directory_absolute_path, "init"])

    if should_create_initial_commit:
        subprocess.call(["git", "-C", project_directory_absolute_path, "add", project_directory_absolute_path])
        subprocess.call(["git", "-C", project_directory_absolute_path, "commit", "-m", "Initial commit"])


def main():
    project_directory_absolute_path = create_project_directory()

    add_template_files(project_directory_absolute_path)
    add_source_folder(project_directory_absolute_path)
    initialize_git_repository(project_directory_absolute_path)


if __name__ == "__main__":
    main()


# Should this whole project be generalized to allow for the creation of any type of project, and not just Python ones?
