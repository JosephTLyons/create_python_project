#!/usr/bin/env python3

import os
import sys
import subprocess

from pathlib import Path
from shutil import copy


def display_error_and_exit(error_message):
    print(error_message)
    sys.exit()


# Fix up print messages
# Test sys.exit() and see how it works
def create_project_directory():
    # There should be 3 argumnets (this file name will count as one)
    if len(sys.argv) != 3:
        display_error_and_exit("Must pass in project directory and project name parameters.")

    project_parent_directory = Path(sys.argv[1])

    if not project_parent_directory.exists():
        display_error_and_exit("Path must exist.")

    project_directory_relative = sys.argv[2]

    if not project_directory_relative.isalnum():
        display_error_and_exit("Project name has illegal characters.")

    project_directory_absolute = project_parent_directory.joinpath() / project_directory_relative

    # If os.mkdir ends up not blocking execution until the directory is made, then use:
    # subprocess.call(["mkdir", project_final_path])
    # We will know if there is ever a situation where future operations fail because this directory
    # hasn't been made yet.
    if not project_directory_absolute.exists():
        os.mkdir(project_directory_absolute)

    return project_directory_absolute


def add_source_folder(project_directory_absolute):
    source_directory_absolute = project_directory_absolute / "source"

    if not source_directory_absolute.exists():
        os.mkdir(source_directory_absolute)


def add_template_files(project_directory_absolute):
    template_files_directory = Path("./template_files")

    if not template_files_directory.exists():
        raise Exception("Template directory is not valid.")

    items_to_ignore = [".DS_STORE"]
    template_text_to_replace = ".template"

    for root, _, files in os.walk(template_files_directory):
        for file in files:
            if file not in items_to_ignore:
                file_path_in_template_files_directory = Path(root, file)

                copy(file_path_in_template_files_directory, project_directory_absolute)

                if template_text_to_replace in file:
                    file_path_string_template_stripped = file.replace(template_text_to_replace, "")
                    file_path_in_project = project_directory_absolute / file
                    file_path_in_project.rename(file_path_string_template_stripped)


def initialize_git_repository(project_directory_absolute):
    pass


# Make sure to use blocking subprocess calls
# Can eiher create files and load in the contents or have files in this repo that get copied over

# Take in parameters from the command line so that paths can be autocompleted
# Validate that we are getting a path that is a path and a string for a project and that that
# Project name doesn't already exist in that directory
# Check that path is valid too
def main():
    project_directory_absolute = create_project_directory()

    add_source_folder(project_directory_absolute)
    add_template_files(project_directory_absolute)


if __name__ == "__main__":
    main()
