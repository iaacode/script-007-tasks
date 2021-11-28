import os
import os.path
import re
import shutil
import logging
from datetime import datetime


def _name_is_invalid(path: str):
    return bool(re.search(r'(^|[\\/])\.\.($|[\\/])', path))


def _get_absolute_path(filename: str):
    return os.path.abspath(filename)


def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """

    if _name_is_invalid(path):
        raise ValueError(f'Path {path} is invalid')

    if not os.path.exists(path):
        if autocreate:
            os.makedirs(path)
        else:
            raise RuntimeError(f'The directory {path} does not exist')

    os.chdir(path)


def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    os.getcwd()
    files = os.listdir(path='.')
    list = []
    for file in files:
        list.append([file, datetime.fromtimestamp(os.path.getctime(file)),
                     datetime.fromtimestamp(os.path.getmtime(file)), os.path.getsize(file)])

    return list


def get_file_data(filename: str) -> dict:
    """Get full info about file.

    Args:
        filename (str): Filename.

    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    filepath = os.path.join(os.getcwd(), filename)

    if _name_is_invalid(filename):
        raise ValueError(f'Filename {filename} is invalid')

    if not os.path.exists(filepath):
        raise RuntimeError(f'Path {filepath} does not exist')

    with open(filepath, 'rb') as file_content:
        return {
            'name': filename,
            'create_date': datetime.fromtimestamp(os.path.getctime(filepath)),
            'edit_date': datetime.fromtimestamp(os.path.getmtime(filepath)),
            'size': os.path.getsize(filepath),
            'content': file_content.read()
        }


def create_file(filename: str, content: str = None) -> dict:
    """Create a new file.

    Args:
        filename (str): Filename.
        content (str): String with file content.

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
    """

    filepath = os.path.join(os.getcwd(), filename)

    if _name_is_invalid(filename):
        raise ValueError(f'Filename {filename} is invalid')

    if os.path.isdir(filepath):
        os.makedirs(filepath)
    else:
        with open(filepath, "w") as file:
            if content:
                file.write(content)
    return {
        'name': filename,
        'content': content,
        'create_date': datetime.fromtimestamp(os.path.getctime(filepath)),
        'size': os.path.getsize(filepath)
    }


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    filepath = _get_absolute_path(filename)

    if not os.path.exists(filepath):
        raise RuntimeError(f'Path {filepath} does not exist')

    if _name_is_invalid(filename):
        raise ValueError(f'Filename {filename} is invalid')

    if os.path.isfile(filepath):
        os.remove(filepath)
    else:
        shutil.rmtree(filepath)

