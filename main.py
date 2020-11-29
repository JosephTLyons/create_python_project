#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
from pathlib import Path


def display_error_and_exit(error_message):
    print(error_message)
    sys.exit()


# Fix up print messages
# Test sys.exit() and see how it works
def create_project_directory():
    # There should be 3 arguments (this file name will count as one)
    if len(sys.argv) != 3:
        display_error_and_exit("Must pass in project directory and project name parameters.")

    project_parent_directory = Path(sys.argv[1])

    if not project_parent_directory.exists():
        display_error_and_exit("Path must exist.")

    project_directory_relative = sys.argv[2]

    if not project_directory_relative.isalnum():
        display_error_and_exit("Project name has illegal characters.")

    project_directory_absolute_path = project_parent_directory.joinpath() / project_directory_relative

    # If os.mkdir ends up not blocking execution until the directory is made, then use:
    # subprocess.call(["mkdir", project_final_path])
    # We will know if there is ever a situation where future operations fail because this directory
    # hasn't been made yet.
    if not project_directory_absolute_path.exists():
        os.mkdir(project_directory_absolute_path)

    return project_directory_absolute_path


def add_source_folder(project_directory_absolute_path):
    source_directory_absolute_path = project_directory_absolute_path / "source"

    if not source_directory_absolute_path.exists():
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

                shutil.copy(template_file_absolute_path, project_file_absolute_path)


def initialize_git_repository(project_directory_absolute_path, should_create_initial_commit=False):
    subprocess.call([f"git init {project_directory_absolute_path}"])

    if should_create_initial_commit:
        # Will need to figure out how to provide the absolute path to the git repo of the new project here
        subprocess.call(["git add ."])
        subprocess.call(["git commit -m \"Initial commit\""])


# Make sure to use blocking subprocess calls
# Can either create files and load in the contents or have files in this repo that get copied over

# Take in parameters from the command line so that paths can be autocompleted
# Validate that we are getting a path that is a path and a string for a project and that that
# Project name doesn't already exist in that directory
# Check that path is valid too
def main():
    project_directory_absolute_path = create_project_directory()

    add_template_files(project_directory_absolute_path)
    add_source_folder(project_directory_absolute_path)
    initialize_git_repository(project_directory_absolute_path)


if __name__ == "__main__":
    main()
