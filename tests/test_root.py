# -*- coding: utf-8 -*-
# Copyright 2026 Matthew Fitzpatrick.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
r"""Contains tests for the root of the package :mod:`pylibtemplate`.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For getting the default values of function parameters.
import inspect

# For operations related to unit tests.
import pytest

# For removing directories.
import shutil

# For setting file permissions and executing Python scripts.
import os

# For making directories.
import pathlib

# For creating JSON files.
import json



# For generating local ``git`` repository templates.
import pylibtemplate



##################################
## Define classes and functions ##
##################################

def get_default_repo_name():
    param_name = "repo_name"
    func_alias = pylibtemplate.generate_local_git_repo_template
    func_signature = inspect.signature(func_alias)
    default_repo_name = func_signature.parameters[param_name].default

    return default_repo_name



def generate_repo_template_config_params_1():
    author_to_email_map = {"Randy Lahey": "randy.lahey@bobandy.com",
                           "Corey Trevor": "corey.trevor@twosmokes.com"}
    maintainer_to_email_map = {"Steve French": "steve.french@goodkitty.com",
                               "J-Roc": "j.roc@lazysusan.com",
                               "Smokey": "smokey@cheeze.com"}

    line_exceeding_80_chars = ("# This is a line that exceeds 80 characters "
                               "that belongs to the new file header. This line "
                               "is deliberately longer than 80 characters to "
                               "test the text wrapping feature of "
                               "``pylibtemplate``.")

    file_header = ("# This is a custom file header."
                   "#",
                   line_exceeding_80_chars)

    repo_template_config_params_1 = \
        {"repo_name": "my-py-lib",
         "lib_name_for_imports": "mypylib",
         "abbreviated_lib_name_for_docs": "MyPyLib",
         "non_abbreviated_lib_name_for_docs": "My Python Library",
         "author_to_email_map": author_to_email_map,
         "maintainer_to_email_map": maintainer_to_email_map,
         "copyright_owner": "Sunnyvale Trailer Park",
         "namespace_url": "https://github.com/tpb",
         "doc_root_url": "https://mrfitzpa.github.io/tpb-my-py-lib",
         "gist_id": "5klmds090sdm2jansdu92nrlkjnmsa9r",
         "spdx_id": "MIT",
         "file_header": file_header,
         "gitlab_test_tags": ("test_tag_1", "test_tag_2"),
         "gitlab_doc_tags": ("test_doc_1", "test_doc_2", "test_doc_3"),
         "path_to_directory_to_contain_new_repo": "./test_data"}

    return repo_template_config_params_1



def test_1_of_generate_local_git_repo_template():
    path_to_test_data = "./" + get_default_repo_name()

    try:
        pylibtemplate.generate_local_git_repo_template()
    finally:
        shutil.rmtree(path_to_test_data, ignore_errors=True)

    return None



def test_2_of_generate_local_git_repo_template():
    repo_template_config_params = \
        generate_repo_template_config_params_1()
    path_to_test_data = \
        repo_template_config_params["path_to_directory_to_contain_new_repo"]

    try:
        kwargs = repo_template_config_params
        pylibtemplate.generate_local_git_repo_template(**kwargs)
    finally:
        shutil.rmtree(path_to_test_data, ignore_errors=True)

    return None



def test_3_of_generate_local_git_repo_template():
    repo_template_config_params = \
        generate_repo_template_config_params_1()
    path_to_test_data = \
        repo_template_config_params["path_to_directory_to_contain_new_repo"]

    pathlib.Path(path_to_test_data).mkdir(parents=True, exist_ok=True)
    os.chmod(path_to_test_data, 0o111)

    try:
        with pytest.raises(IOError) as err_info:
            kwargs = repo_template_config_params
            pylibtemplate.generate_local_git_repo_template(**kwargs)
    finally:
        os.chmod(path_to_test_data, 0o711)
        shutil.rmtree(path_to_test_data, ignore_errors=True)

    return None



def test_4_of_generate_local_git_repo_template():
    with pytest.raises(ValueError) as err_info:
        kwargs = {"lib_name_for_imports": "123abc"}
        pylibtemplate.generate_local_git_repo_template(**kwargs)

    with pytest.raises(ValueError) as err_info:
        kwargs = {"abbreviated_lib_name_for_docs": "123abc"}
        pylibtemplate.generate_local_git_repo_template(**kwargs)

    with pytest.raises(ValueError) as err_info:
        kwargs = {"author_to_email_map": {slice(None): "foo"}}
        pylibtemplate.generate_local_git_repo_template(**kwargs)

    with pytest.raises(ValueError) as err_info:
        kwargs = {"maintainer_to_email_map": {slice(None): "foo"}}
        pylibtemplate.generate_local_git_repo_template(**kwargs)

    with pytest.raises(ValueError) as err_info:
        kwargs = {"spdx_id": "foobar"}
        pylibtemplate.generate_local_git_repo_template(**kwargs)

    return None



def test_1_of_run_pylibtemplate_as_an_app():
    repo_template_config_params = \
        generate_repo_template_config_params_1()
    path_to_test_data = \
        repo_template_config_params["path_to_directory_to_contain_new_repo"]
    config_filename = \
        path_to_test_data + "/repo_template_config_params.json"

    pathlib.Path(path_to_test_data).mkdir(parents=True, exist_ok=True)

    with open(config_filename, "w") as file_obj:
        json.dump(repo_template_config_params, file_obj, indent=4)

    params = {"config_filename": config_filename}

    cmd_line_args = []
    for param_name in params:
        cmd_line_arg = "--"+param_name+"="+str(params[param_name])
        cmd_line_args.append(cmd_line_arg)

    try:
        pylibtemplate._run_pylibtemplate_as_an_app(cmd_line_args)

        with pytest.raises(SystemExit) as err_info:
            cmd_line_arg = "--foo=bar"
            cmd_line_args.append(cmd_line_arg)
            pylibtemplate._run_pylibtemplate_as_an_app(cmd_line_args)
    finally:
        shutil.rmtree(path_to_test_data, ignore_errors=True)

    return None



###########################
## Define error messages ##
###########################
