import os
from pathlib import Path
from typing import List

def read_file_as_text(path)-> str:

    contents = None

    with open(path, "r", encoding="UTF-8") as f:
        contents = str(f.readlines())

    return contents

def read_file_as_lines(path)-> List[str]:

    contents = None

    with open(path, "r", encoding="UTF-8") as f:
        contents = f.readlines()

    return contents

def read_file_as_binary(path):

    contents = None

    with open(path, "rb") as f:
        contents = f.readlines()

    return contents


def get_current_dir(source):
    return os.path.dirname(os.path.realpath(source))

def get_parent_dir(source):
    return Path(os.path.dirname(os.path.realpath(source))).parent

def write_file(file, contents) -> None:
    with open(file, 'w') as f:
        f.write(contents)