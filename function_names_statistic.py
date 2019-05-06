import ast
import os
import logging

from nltk import pos_tag
from re import search
from collections import Counter
from itertools import chain
from typing import List, Tuple

PY_FILES_LIMIT = 100
TOP_VERBS_LIMIT = 10
TOP_NAMES_LIMIT = 10
TOP_VERBS_MP_LIMIT = 200


def get_python_files_in_project(project_path: str, limit: int = PY_FILES_LIMIT) -> List[str]:
    """
    Get paths to python files in project directory.
    :param project_path: Path to directory.
    :param limit: Maximum size of the resulting list.
    :return: List with python files paths.
    """
    file_paths = []
    if not os.path.exists(project_path):
        logging.info(f'{project_path} not found.')
    for dir_name, _, file_names in os.walk(project_path, topdown=True):
        python_files = [file for file in file_names if file.endswith('.py')]
        for file in python_files[:limit]:
            file_paths.append(os.path.join(dir_name, file))
    return file_paths


def get_syntax_tree(file_path: str) -> ast.Module:
    """
    Get abstract syntax tree from python file.
    :param file_path: Path to file.
    :return: Abstract syntax tree.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        try:
            syntax_tree = ast.parse(file_content)
        except SyntaxError as e:
            logging.warning(f'{e} {file_path}')
            syntax_tree = ast.Module()
    return syntax_tree


def get_syntax_trees_in_project(project_path: str) -> List[ast.Module]:
    """
    Get abstract syntax trees of python files in project directory.
    :param project_path: Path to directory.
    :return: List with abstract trees.
    """
    python_files = get_python_files_in_project(project_path)
    syntax_trees = [get_syntax_tree(file_path) for file_path in python_files]
    return syntax_trees


def get_var_names_in_tree(syntax_tree: ast.Module) -> List[str]:
    """
    Get variable names in syntax tree.
    :param syntax_tree: Abstract syntax tree object.
    :return: List with variable names.
    """
    var_names = [node.id for node in ast.walk(syntax_tree) if isinstance(node, ast.Name)]
    return var_names


def get_verbs(words: List[str]) -> List[str]:
    """
    Get verbs from words list.
    :param words: List with words.
    :return: List with verbs.
    """
    tagged_words = pos_tag(words)
    verbs = [word for word, tag in tagged_words if tag.startswith('VB')]
    return verbs


def get_function_names_in_tree(syntax_tree: ast.Module) -> List[str]:
    """
    Get function names in syntax tree.
    :param syntax_tree: Abstract syntax tree object.
    :return: List with function names.
    """
    function_names = []
    for node in ast.walk(syntax_tree):
        if isinstance(node, ast.FunctionDef) and not search(r'^__.*__$', node.name):
            function_names.append(node.name.lower())
    return function_names


def get_function_names_in_project(project_path: str) -> List[str]:
    """
    Get function names contained in python files in the directory.
    :param project_path: Path to directory.
    :return: List with function names.
    """
    syntax_trees = get_syntax_trees_in_project(project_path)
    function_names = chain.from_iterable(get_function_names_in_tree(tree) for tree in syntax_trees)
    return list(function_names)


def get_all_words_in_project(project_path: str) -> List[str]:
    """
    Get words contained in function names in project.
    :param project_path: Path to directory.
    :return: List with words.
    """
    function_names = get_function_names_in_project(project_path)
    splitted_names = chain.from_iterable(name.split('_') for name in function_names)
    words = filter(None, splitted_names)
    return list(words)


def get_verbs_in_project(project_path: str) -> List[str]:
    """
    Get verbs contained in the function names in the project.
    :param project_path: Path to directory.
    :return: List with verbs.
    """
    words = get_all_words_in_project(project_path)
    verbs = get_verbs(words)
    return verbs


def get_top_verbs_in_project(project_path: str, limit: int = TOP_VERBS_LIMIT) -> List[Tuple[str, int]]:
    """
    Get most common verbs contained in the function names in the project.
    :param project_path: Path to directory.
    :param limit: Maximum size of the resulting list.
    :return: List with counted verbs.
    """
    verbs = get_verbs_in_project(project_path)
    counted_verbs = Counter(verbs).most_common(limit)
    return counted_verbs


def get_top_function_names_in_project(project_path: str, limit: int = TOP_NAMES_LIMIT) -> List[Tuple[str, int]]:
    """
    Get most common function names in the project.
    :param project_path: Path to directory.
    :param limit: Maximum size of the resulting list.
    :return: List with counted function names.
    """
    function_names = get_function_names_in_project(project_path)
    counted_names = Counter(function_names).most_common(limit)
    return counted_names


def get_top_verbs_in_multiple_projects(root_path: str,
                                       projects: List[str],
                                       limit: int = TOP_VERBS_MP_LIMIT) -> List[Tuple[str, int]]:
    """
    Get most common verbs contained in the function names in multiple projects.
    :param root_path: Path to root directory.
    :param projects: List of project names.
    :param limit: Maximum size of the resulting list.
    :return: List with counted verbs.
    """
    verbs = []
    for project_name in projects:
        project_path = os.path.join(root_path, project_name)
        verbs.extend(get_verbs_in_project(project_path))
    counted_verbs = Counter(verbs).most_common(limit)
    return counted_verbs
