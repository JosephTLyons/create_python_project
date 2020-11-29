#!/usr/bin/env python3

import sys

from pathlib import Path


def display_error_and_exit(error_message):
    print(error_message)
    sys.exit()


# Fix up print messages
# Test sys.exit() and see how it works
def create_project_directory():
    # There should be 3 argumnets (this file name will count as one)
    if len(sys.argv) != 3:
        display_error_and_exit("Must pass in project directory and project name parameters.")

    try:
        project_destination = Path(sys.argv[1])
    except:
        display_error_and_exit("First parameter must a path.")

    if not project_destination.exists():
        display_error_and_exit("Path must exist.")

    project_name = sys.argv[2]

    if not project_name.isalnum():
        display_error_and_exit("Project name has illegal characters.")

    project_final_path = project_destination.joinpath() / project_name

    print(project_final_path)


def add_main_py():
    pass


def add_gitignore():
    pass


def initialize_git_repository():
    pass


# Make sure to use blocking subprocess calls
# Can eiher create files and load in the contents or have files in this repo that get copied over

# Take in parameters from the command line so that paths can be autocompleted
# Validate that we are getting a path that is a path and a string for a project and that that
# Project name doesn't already exist in that directory
# Check that path is valid too
def main():
    create_project_directory()


if __name__ == "__main__":
    main()
