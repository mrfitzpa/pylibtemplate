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
r""":mod:`pylibtemplate` (short for 'Python Library Template') is a Python
library that generates ``git`` repository templates for building Python
libraries that are suitable for publication on PyPI.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For converting relative paths to absolute paths, and for making directories.
import pathlib

# For percent-encoding strings for URLs.
import urllib.parse

# For sending HTTP GET requests.
import requests

# For timing the execution of different segments of code.
import time

# For getting the current year.
import datetime

# For pattern matching.
import re

# For removing directories.
import shutil

# For removing files, renaming directories, and getting directory trees.
import os

# For wrapping text.
import textwrap

# For parsing command line arguments.
import argparse

# For reading JSON files.
import json



# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For cloning ``git`` repositories.
import git



# Get version of current package.
from pylibtemplate.version import __version__



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["generate_local_git_repo_template"]



def _check_and_convert_repo_name(params):
    obj_name = "repo_name"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    repo_name = czekitout.convert.to_str_from_str_like(**kwargs)
    
    return repo_name



def _check_and_convert_lib_name_for_imports(params):
    obj_name = "lib_name_for_imports"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    lib_name_for_imports = czekitout.convert.to_str_from_str_like(**kwargs)

    current_func_name = "_check_and_convert_lib_name_for_imports"

    if not lib_name_for_imports.isidentifier():
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise ValueError(err_msg)
    
    return lib_name_for_imports



def _check_and_convert_abbreviated_lib_name_for_docs(params):
    obj_name = \
        "abbreviated_lib_name_for_docs"
    kwargs = \
        {"obj": params[obj_name], "obj_name": obj_name}
    abbreviated_lib_name_for_docs = \
        czekitout.convert.to_str_from_str_like(**kwargs)

    current_func_name = "_check_and_convert_abbreviated_lib_name_for_docs"

    if not abbreviated_lib_name_for_docs.isidentifier():
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise ValueError(err_msg)
    
    return abbreviated_lib_name_for_docs



def _check_and_convert_non_abbreviated_lib_name_for_docs(params):
    obj_name = \
        "non_abbreviated_lib_name_for_docs"
    kwargs = \
        {"obj": params[obj_name], "obj_name": obj_name}
    non_abbreviated_lib_name_for_docs = \
        czekitout.convert.to_str_from_str_like(**kwargs)
    
    return non_abbreviated_lib_name_for_docs



def _check_and_convert_author_to_email_map(params):
    obj_name = "author_to_email_map"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    author_to_email_map = czekitout.convert.to_dict(**kwargs)
    author_to_email_map_copy = author_to_email_map.copy()

    current_func_name = "_check_and_convert_author_to_email_map"

    for author in author_to_email_map:
        try:
            kwargs = {"obj": author,
                      "obj_name": "author"}
            author = czekitout.convert.to_str_from_str_like(**kwargs)
        except:
            unformatted_err_msg = globals()[current_func_name+"_err_msg_1"]
            err_msg = unformatted_err_msg.format(author)
            raise ValueError(err_msg)
        
        kwargs = {"obj": author_to_email_map[author],
                  "obj_name": "author_to_email_map[{}]".format(author)}
        email = czekitout.convert.to_str_from_str_like(**kwargs)

        author_to_email_map_copy[author] = email

    author_to_email_map = author_to_email_map_copy
    
    return author_to_email_map



def _check_and_convert_maintainer_to_email_map(params):
    obj_name = "maintainer_to_email_map"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    maintainer_to_email_map = czekitout.convert.to_dict(**kwargs)
    maintainer_to_email_map_copy = maintainer_to_email_map.copy()

    current_func_name = "_check_and_convert_maintainer_to_email_map"

    for maintainer in maintainer_to_email_map:
        try:
            kwargs = {"obj": maintainer,
                      "obj_name": "maintainer"}
            maintainer = czekitout.convert.to_str_from_str_like(**kwargs)
        except:
            unformatted_err_msg = globals()[current_func_name+"_err_msg_1"]
            err_msg = unformatted_err_msg.format(maintainer)
            raise ValueError(err_msg)
        
        kwargs = {"obj": maintainer_to_email_map[maintainer],
                  "obj_name": "maintainer_to_email_map[{}]".format(maintainer)}
        email = czekitout.convert.to_str_from_str_like(**kwargs)

        maintainer_to_email_map_copy[maintainer] = email

    maintainer_to_email_map = maintainer_to_email_map_copy
    
    return maintainer_to_email_map



def _check_and_convert_copyright_owner(params):
    obj_name = "copyright_owner"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    copyright_owner = czekitout.convert.to_str_from_str_like(**kwargs)
    
    return copyright_owner



def _check_and_convert_namespace_url(params):
    obj_name = "namespace_url"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    namespace_url = czekitout.convert.to_str_from_str_like(**kwargs)
    
    return namespace_url



def _check_and_convert_doc_root_url(params):
    obj_name = "doc_root_url"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    doc_root_url = czekitout.convert.to_str_from_str_like(**kwargs)
    
    return doc_root_url



def _check_and_convert_gist_id(params):
    obj_name = "gist_id"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    gist_id = czekitout.convert.to_str_from_str_like(**kwargs)
    
    return gist_id



def _check_and_convert_spdx_id(params):
    obj_name = "spdx_id"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    spdx_id = czekitout.convert.to_str_from_str_like(**kwargs)

    current_func_name = "_check_and_convert_spdx_id"

    try:
        _ = _get_license_info_from_spdx_id(spdx_id)
    except:
        unformatted_err_msg = globals()[current_func_name+"_err_msg_1"]
        err_msg = unformatted_err_msg.format(spdx_id)
        raise ValueError(err_msg)
    
    return spdx_id



def _get_license_info_from_spdx_id(spdx_id):
    spdx_json_data = _get_spdx_json_data(spdx_id)

    license_name = spdx_json_data.get("name", spdx_id)

    see_also_data = spdx_json_data.get("seeAlso", [])
    fallback_url = "https://spdx.org/licenses/{}.html".format(spdx_id)
    license_page_url = (see_also_data[0]
                        if (len(see_also_data) > 0)
                        else fallback_url)

    badge_label = license_name.replace(" ", "_")
    badge_label_encoded = urllib.parse.quote(badge_label, safe="_")
    license_badge_url = ("https://img.shields.io/badge/License"
                         "-{}-blue.svg".format(badge_label_encoded))

    license_text = spdx_json_data.get("licenseText").splitlines()

    license_info = {"license_name": license_name,
                    "license_page_url": license_page_url,
                    "license_badge_url": license_badge_url,
                    "license_text": license_text}

    return license_info



def _get_spdx_json_data(spdx_id):
    spdx_json_file_url = ("https://raw.githubusercontent.com/spdx"
                          "/license-list-data/main/json/details"
                          "/{}.json".format(spdx_id))

    current_func_name = "_get_spdx_json_data"

    http_get_request_response = requests.get(spdx_json_file_url)
    if http_get_request_response.status_code != 200:
        unformatted_err_msg = globals()[current_func_name+"_err_msg_1"]
        err_msg = unformatted_err_msg.format(spdx_id)
        raise ValueError(err_msg)

    spdx_json_data = http_get_request_response.json()

    return spdx_json_data



def _check_and_convert_file_header(params):
    obj_name = "file_header"
    obj = params[obj_name]

    if isinstance(obj, type(None)):
        file_header = None
    else:
        kwargs = {"obj": obj, "obj_name": obj_name}
        file_header = czekitout.convert.to_tuple_of_strs(**kwargs)
    
    return file_header



def _check_and_convert_gitlab_test_tags(params):
    obj_name = "gitlab_test_tags"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    gitlab_test_tags = czekitout.convert.to_tuple_of_strs(**kwargs)
    
    return gitlab_test_tags



def _check_and_convert_gitlab_doc_tags(params):
    obj_name = "gitlab_doc_tags"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    gitlab_doc_tags = czekitout.convert.to_tuple_of_strs(**kwargs)
    
    return gitlab_doc_tags



def _check_and_convert_path_to_directory_to_contain_new_repo(params):
    obj_name = \
        "path_to_directory_to_contain_new_repo"
    kwargs = \
        {"obj": params[obj_name], "obj_name": obj_name}
    path_to_directory_to_contain_new_repo = \
        czekitout.convert.to_str_from_str_like(**kwargs)
    path_to_directory_to_contain_new_repo = \
        str(pathlib.Path(path_to_directory_to_contain_new_repo).absolute())
    
    return path_to_directory_to_contain_new_repo



_default_repo_name = \
    "pylibtemplate"
_default_lib_name_for_imports = \
    "pylibtemplate"
_default_abbreviated_lib_name_for_docs = \
    "PyLibTemplate"
_default_non_abbreviated_lib_name_for_docs = \
    "Python Library Template"
_default_copyright_owner = \
    "Matthew Fitzpatrick"
_default_author_to_email_map = \
    {_default_copyright_owner: "matthew.rc.fitzpatrick@gmail.com"}
_default_maintainer_to_email_map = \
    _default_author_to_email_map
_default_namespace_url = \
    "https://github.com/mrfitzpa"
_default_doc_root_url = \
    "https://mrfitzpa.github.io/pylibtemplate"
_default_gist_id = \
    "7baba2a56d07b59cc49b8323f44416e5"
_default_spdx_id = \
    "GPL-3.0-or-later"
_default_file_header = \
    None
_default_gitlab_test_tags = \
    tuple()
_default_gitlab_doc_tags = \
    _default_gitlab_test_tags
_default_path_to_directory_to_contain_new_repo = \
    ""



def generate_local_git_repo_template(
        repo_name=\
        _default_repo_name,
        lib_name_for_imports=\
        _default_lib_name_for_imports,
        abbreviated_lib_name_for_docs=\
        _default_abbreviated_lib_name_for_docs,
        non_abbreviated_lib_name_for_docs=\
        _default_non_abbreviated_lib_name_for_docs,
        author_to_email_map=\
        _default_author_to_email_map,
        maintainer_to_email_map=\
        _default_maintainer_to_email_map,
        copyright_owner=\
        _default_copyright_owner,
        namespace_url=\
        _default_namespace_url,
        doc_root_url=\
        _default_doc_root_url,
        gist_id=\
        _default_gist_id,
        spdx_id=\
        _default_spdx_id,
        file_header=\
        _default_file_header,
        gitlab_test_tags=\
        _default_gitlab_test_tags,
        gitlab_doc_tags=\
        _default_gitlab_doc_tags,
        path_to_directory_to_contain_new_repo=\
        _default_path_to_directory_to_contain_new_repo):
    r"""Generate a local ``git`` repository template.

    The primary purpose of generating a local ``git`` repository template is to
    modify it subsequently to develop a new Python library.

    This Python function will perform several actions: First, it will clone the
    ``git`` commit of the ``pylibtemplate`` GitHub repository corresponding to
    the version of ``pylibtemplate`` being used currently, in the directory at
    the path ``path_to_directory_to_contain_new_repo``, i.e. the ``git clone``
    command is executed while the working directory is set temporarily to the
    path ``path_to_directory_to_contain_new_repo``; Next, it will rename the
    cloned repository to ``repo_name`` such that the path to the cloned
    repository becomes ``path_to_directory_to_contain_new_repo+"/"+repo_name``;
    Next, all instances of the string of characters
    ``"https://github.com/mrfitzpa/pylibtemplate"`` are replaced with
    ``namespace_url+"/"+repo_name``; Next, all instances of the string of
    characters ``"https://mrfitzpa.github.io/pylibtemplate"`` are replaced with
    ``doc_root_url``; Next, all instances of the string of characters
    ``"pylibtemplate"`` are replaced with ``lib_name_for_imports``, be it in
    file contents, directory basenames, or file basenames; Next, all instances
    of the string of characters ``"PyLibTemplate"`` are replaced with
    ``abbreviated_lib_name_for_docs``; Next, all instances of the string of
    characters ``"Python Library Template"`` are replaced with
    ``non_abbreviated_lib_name_for_docs``; Next, all copyright statements of the
    form ``"Copyright <current_year> Matthew Fitzpatrick"`` are replaced by
    ``"Copyright <current_year> "+copyright_owner``, where ``<current_year>`` is
    the current year; Next, all instances of ``"Matthew Fitzpatrick"`` are
    replaced by ``copyright_owner``; Next, all instances of the gist ID of
    ``pylibtemplate`` are replaced with ``gist_id``;

    Next, all license
    information is updated to accord with the license specified by the SPDX ID
    ``spdx_id``; Next, if ``file_header`` is set to a sequence (e.g. a Python
    list) of Python strings, then the original file header appearing in the
    files::

    * ``<local_repo_root>/<lib_name_for_imports>/__init__.py``
    * ``<local_repo_root>/setup.py``
    * ``<local_repo_root>/run_tests.sh``
    * ``<local_repo_root>/tests/test_root.py``
    * ``<local_repo_root>/examples/generating_a_git_repository_template.py``
    * ``<local_repo_root>/docs/conf.py``
    * ``<local_repo_root>/docs/build_docs.py``

    with ``<local_repo_root>`` being the root of the new local ``git``
    repository, is replaced by a sequence of lines, where the ``n`` th line in
    this sequence is ``file_header[n]`` (note that the original file header
    starts with ``# -*- coding: utf-8 -*-`` and ends with ``# this program. If
    not, see <https://www.gnu.org/licenses/gpl-3.0.html>.``; Next, all
    authorship information (including author emails) is updated according to the
    ``author_to_email_map`` parameter (see parameter description for details on
    expected form of parameter); Next, all maintainership information (including
    maintainer emails) is updated according to the ``maintainer_to_email_map``
    parameter (see parameter description for details on expected form of
    parameter); Next, if ``gitlab_test_tags`` is a nonempty sequence of Python
    strings, then the section ``tags`` section of the ``test`` job in the file
    ``<local_repo_root>/.gitlab-ci.yml`` is cleared and then repopulated with
    the tags specified in ``gitlab_test_tags``; Next, if ``gitlab_doc_tags`` is
    a nonempty sequence of Python strings, then the section ``tags`` section of
    the ``pages`` job in the file ``<local_repo_root>/.gitlab-ci.yml`` is
    cleared and then repopulated with the tags specified in ``gitlab_doc_tags``;
    And lastly, the following file is removed::

    * ``<local_repo_root>/docs/how_to_create_a_python_library_using_pylibtemplate.rst``

    as well as the following directory::

    * ``<local_repo_root>/.git``

    On a unrelated note, for the purposes of demonstrating the citing of
    literature, we cite Ref. [RefLabel1]_ and [RefLabel2]_.

    Parameters
    ----------
    repo_name : `str`, optional
        The basename of the new repository.
    lib_name_for_imports : `str`, optional
        The name of the new Python library, as it would appear in Python import
        commands. This parameter needs to be a valid Python identifier.
    abbreviated_lib_name_for_docs : `str`, optional
        An abbreviated format of the name of the new Python library that appears
        in documentation pages. This parameter needs to be a valid Python 
        identifier. It can be set to the same value as ``lib_name_for_imports``.
    non_abbreviated_lib_name_for_docs : `str`, optional
        A non-abbreviated format of the name of the new Python library that
        appears in documentation pages.
    author_to_email_map : `dict`, optional
        The author to email map. Each key ``author`` is assumed to be a string
        storing the name of an author, and ``author_to_email_map[author]`` is a
        string storing the corresponding email of the author.
    maintainer_to_email_map : `dict`, optional
        The maintainer to email map. Each key ``maintainer`` is assumed to be a
        string storing the name of an maintainer, and
        ``maintainer_to_email_map[maintainer]`` is a string storing the
        corresponding email of the maintainer.
    copyright_owner : `str`, optional
        The name of the copyright owner of the new repository.
    namespace_url : `str`, optional
        The GitHub namespace url of the new repository.
    doc_root_url : `str`, optional
        The URL of the root of the documentation website of the new Python
        library.
    gist_id : `str`, optional
        The ID of the GitHub gist to be used to record the code coverage from
        your unit tests. See the
        :ref:`how_to_create_a_python_library_using_pylibtemplate_sec` page for
        instructions on how to create a GitHub gist for your new Python library.
    spdx_id : `str`, optional
        The SPDX ID of the license of the new Python library. See `here
        <https://spdx.org/licenses>`_ for a list of valid SPDX IDs.
    file_header : `array_like` (`str, ndim=1) | `None`, optional
        If ``file_header`` is set to ``None``, then the original file header,
        mentioned in the summary documentation above, is left
        unchanged. Otherwise, ``file_header`` is expected to be a sequence of
        lines, where the ``n`` th line in this sequence is ``file_header[n]``
        (note that the original file header starts with ``# -*- coding: utf-8
        -*-`` and ends with ``# this program. If not, see
        <https://www.gnu.org/licenses/gpl-3.0.html>.``. Combined, the lines
        stored in ``file_header`` forms the new file header to be used in the
        new Python library.
    gitlab_test_tags : `array_like` (`str, ndim=1), optional
        The tags of the ``test`` job in the file
        ``<local_repo_root>/.gitlab-ci.yml``, where ``<local_repo_root>`` is the
        root of the new local ``git`` repository.
    gitlab_doc_tags : `array_like` (`str, ndim=1), optional
        The tags of the ``pages`` job in the file
        ``<local_repo_root>/.gitlab-ci.yml``, where ``<local_repo_root>`` is the
        root of the new local ``git`` repository.
    path_to_directory_to_contain_new_repo : `str`, optional
        The path to the directory inside which the ``git`` commit --- of the
        ``pylibtemplate`` GitHub repository corresponding to the version of
        ``pylibtemplate`` being used currently --- is to be cloned, i.e. the
        ``git clone`` command is executed while the working directory is set
        temporarily to ``path_to_directory_to_contain_new_repo``.

    """
    params = locals()

    global_symbol_table = globals()
    for param_name in params:
        func_name = "_check_and_convert_" + param_name
        func_alias = global_symbol_table[func_name]
        params[param_name] = func_alias(params)

    kwargs = params
    result = _generate_local_git_repo_template(**kwargs)

    return None



def _generate_local_git_repo_template(repo_name,
                                      lib_name_for_imports,
                                      abbreviated_lib_name_for_docs,
                                      non_abbreviated_lib_name_for_docs,
                                      author_to_email_map,
                                      maintainer_to_email_map,
                                      copyright_owner,
                                      namespace_url,
                                      doc_root_url,
                                      gist_id,
                                      spdx_id,
                                      file_header,
                                      gitlab_test_tags,
                                      gitlab_doc_tags,
                                      path_to_directory_to_contain_new_repo):
    repo_template_config_params = locals()
    kwargs = {"repo_template_config_params": repo_template_config_params}
    _print_generate_local_git_repo_template_starting_msg(**kwargs)

    start_time = time.time()

    kwargs = {"path_to_directory_to_contain_new_repo": \
              path_to_directory_to_contain_new_repo,
              "repo_name": \
              repo_name}
    _clone_pylibtemplate_repo(**kwargs)
    _rm_file_subset_of_local_git_repo(**kwargs)

    kwargs["lib_name_for_imports"] = lib_name_for_imports
    _mv_directory_subset_of_local_git_repo(**kwargs)

    kwargs = {"path_to_directory_to_contain_new_repo": \
              path_to_directory_to_contain_new_repo,
              "repo_name": \
              repo_name,
              "repo_template_config_params": \
              repo_template_config_params}
    _replace_and_wrap_text(**kwargs)

    del kwargs["repo_template_config_params"]
    kwargs["start_time"] = start_time
    _print_generate_local_git_repo_template_end_msg(**kwargs)

    return None



def _print_generate_local_git_repo_template_starting_msg(
        repo_template_config_params):
    msg = ("Generating a local ``git`` repository with the "
           "following parameters:\n"
           "\n")
    for param_name, param in repo_template_config_params.items():
        msg += ("``{}`` = ``'{}'``\n"
                if isinstance(param, str)
                else "``{}`` = ``{}``\n").format(param_name, param)
    msg += "\n"
    msg += "..."
    msg += "\n"
    print(msg)

    return None



def _clone_pylibtemplate_repo(path_to_directory_to_contain_new_repo, repo_name):
    current_func_name = "_clone_pylibtemplate_repo"

    try:
        kwargs = {"output_dirname": path_to_directory_to_contain_new_repo}
        _make_output_dir(**kwargs)

        github_url = "https://github.com/mrfitzpa/pylibtemplate.git"

        kwargs = {"path_to_directory_to_contain_new_repo": \
                  path_to_directory_to_contain_new_repo,
                  "repo_name": \
                  repo_name}
        path_to_new_repo = _generate_path_to_new_repo(**kwargs)

        tag = _get_pylibtemplate_tag()

        cloning_options = (tuple()
                           if (tag is None)
                           else ("--depth 1", "--branch {}".format(tag)))

        kwargs = {"url": github_url,
                  "to_path": path_to_new_repo,
                  "multi_options": cloning_options}
        git.Repo.clone_from(**kwargs)
    except:
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise IOError(err_msg)

    return None



def _make_output_dir(output_dirname):
    current_func_name = "_make_output_dir"

    try:
        pathlib.Path(output_dirname).mkdir(parents=True, exist_ok=True)
    except:
        unformatted_err_msg = globals()[current_func_name+"_err_msg_1"]
        err_msg = unformatted_err_msg.format(output_dirname)
        raise IOError(err_msg)

    return None



def _generate_path_to_new_repo(path_to_directory_to_contain_new_repo,
                               repo_name):
    path_to_new_repo = "{}/{}".format(path_to_directory_to_contain_new_repo,
                                      repo_name)

    return path_to_new_repo



def _get_pylibtemplate_tag():
    pattern = r"[0-9]\.[0-9]\.[0-9]"
    pylibtemplate_version = __version__    
    pylibtemplate_tag = ("v{}".format(pylibtemplate_version)
                         if re.fullmatch(pattern, pylibtemplate_version)
                         else None)

    return pylibtemplate_tag



def _rm_file_subset_of_local_git_repo(path_to_directory_to_contain_new_repo,
                                      repo_name):
    kwargs = {"path_to_directory_to_contain_new_repo": \
              path_to_directory_to_contain_new_repo,
              "repo_name": \
              repo_name}
    path_to_new_repo = _generate_path_to_new_repo(**kwargs)

    path_to_dir_to_rm = path_to_new_repo + "/.git"
    shutil.rmtree(path_to_dir_to_rm, ignore_errors=True)

    basename = "how_to_create_a_python_library_using_pylibtemplate.rst"
    path_to_file_to_rm = path_to_new_repo + "/docs/" + basename
    os.remove(path_to_file_to_rm)

    return None



def _mv_directory_subset_of_local_git_repo(
        path_to_directory_to_contain_new_repo, repo_name, lib_name_for_imports):
    kwargs = {"path_to_directory_to_contain_new_repo": \
              path_to_directory_to_contain_new_repo,
              "repo_name": \
              repo_name}
    path_to_new_repo = _generate_path_to_new_repo(**kwargs)

    os.rename(path_to_new_repo + "/pylibtemplate",
              path_to_new_repo + "/" + lib_name_for_imports)

    return None



def _replace_and_wrap_text(path_to_directory_to_contain_new_repo,
                           repo_name,
                           repo_template_config_params):
    kwargs = {"path_to_directory_to_contain_new_repo": \
              path_to_directory_to_contain_new_repo,
              "repo_name": \
              repo_name}
    filenames = _get_paths_to_files_in_local_git_repo(**kwargs)

    kwargs = {"repo_template_config_params": repo_template_config_params}
    text_replacement_map = _generate_text_replacement_map(**kwargs)

    for filename in filenames:
        basename = os.path.basename(filename)

        kwargs = {"filename": filename,
                  "text_replacement_map": text_replacement_map,
                  "repo_template_config_params": repo_template_config_params}
        new_file_contents = _generate_new_file_contents(**kwargs)

        with open(filename, "w") as file_obj:
            line_set = new_file_contents
            file_obj.write("\n".join(line_set))

    return None



def _get_paths_to_files_in_local_git_repo(path_to_directory_to_contain_new_repo,
                                          repo_name):
    kwargs = locals()
    path_to_new_repo = _generate_path_to_new_repo(**kwargs)
    
    dir_tree = list(os.walk(path_to_new_repo))

    dirname = os.path.abspath(dir_tree[0][0])
    basename = os.path.basename(dirname)

    filenames = []
    subdirnames = []

    for x in dir_tree:
        subdirname = x[0]
        subdirnames += [subdirname]

        file_basenames = x[2]
        for file_basename in file_basenames:
            filename = subdirname + '/' + file_basename
            filenames += [filename]

        subdirnames.pop(0)

    paths_to_files_in_local_git_repo = filenames

    return paths_to_files_in_local_git_repo



def _generate_text_replacement_map(repo_template_config_params):
    unformatted_func_names = \
        ("_generate_{}_github_repo_url",
         "_generate_{}_doc_root_url",
         "_generate_{}_lib_name_for_imports",
         "_generate_{}_abbreviated_lib_name_for_docs",
         "_generate_{}_non_abbreviated_lib_name_for_docs",
         "_generate_{}_copyright_statement",
         "_generate_{}_copyright_owner",
         "_generate_{}_gist_id",
         "_generate_{}_license_badge_url",
         "_generate_{}_license_page_url",
         "_generate_{}_spdx_id")

    text_replacement_map = dict()
    global_symbol_table = globals()
    for unformatted_func_name in unformatted_func_names:
        func_name_0 = unformatted_func_name.format("old")
        func_name_1 = unformatted_func_name.format("new")
        func_0 = global_symbol_table[func_name_0]
        func_1 = global_symbol_table[func_name_1]
        old_text = func_0()
        new_text = func_1(repo_template_config_params)
        text_replacement_map[old_text] = new_text

    return text_replacement_map



def _generate_old_github_repo_url():
    old_github_repo_url = "https://github.com/mrfitzpa/pylibtemplate"

    return old_github_repo_url



def _generate_new_github_repo_url(repo_template_config_params):
    namespace_url = repo_template_config_params["namespace_url"]
    repo_name = repo_template_config_params["repo_name"]
    new_github_repo_url = namespace_url + "/" + repo_name

    return new_github_repo_url



def _generate_old_doc_root_url():
    old_doc_root_url = "https://mrfitzpa.github.io/pylibtemplate"

    return old_doc_root_url



def _generate_new_doc_root_url(repo_template_config_params):
    doc_root_url = repo_template_config_params["doc_root_url"]
    new_doc_root_url = doc_root_url

    return new_doc_root_url



def _generate_old_lib_name_for_imports():
    old_lib_name_for_imports = _default_lib_name_for_imports

    return old_lib_name_for_imports



def _generate_new_lib_name_for_imports(repo_template_config_params):
    lib_name_for_imports = repo_template_config_params["lib_name_for_imports"]
    new_lib_name_for_imports = lib_name_for_imports

    return new_lib_name_for_imports



def _generate_old_abbreviated_lib_name_for_docs():
    old_abbreviated_lib_name_for_docs = _default_abbreviated_lib_name_for_docs

    return old_abbreviated_lib_name_for_docs



def _generate_new_abbreviated_lib_name_for_docs(repo_template_config_params):
    abbreviated_lib_name_for_docs = \
        repo_template_config_params["abbreviated_lib_name_for_docs"]
    new_abbreviated_lib_name_for_docs = \
        abbreviated_lib_name_for_docs

    return new_abbreviated_lib_name_for_docs



def _generate_old_non_abbreviated_lib_name_for_docs():
    old_non_abbreviated_lib_name_for_docs = \
        _default_non_abbreviated_lib_name_for_docs

    return old_non_abbreviated_lib_name_for_docs



def _generate_new_non_abbreviated_lib_name_for_docs(
        repo_template_config_params):
    non_abbreviated_lib_name_for_docs = \
        repo_template_config_params["non_abbreviated_lib_name_for_docs"]
    new_non_abbreviated_lib_name_for_docs = \
        non_abbreviated_lib_name_for_docs

    return new_non_abbreviated_lib_name_for_docs



def _generate_old_copyright_statement():
    old_copyright_statement = "Copyright {} {}".format(2026,
                                                       _default_copyright_owner)

    return old_copyright_statement



def _generate_new_copyright_statement(repo_template_config_params):
    copyright_owner = repo_template_config_params["copyright_owner"]
    current_year = datetime.date.today().year
    new_copyright_statement = "Copyright {} {}".format(current_year,
                                                       copyright_owner)

    return new_copyright_statement



def _generate_old_copyright_owner():
    old_copyright_owner = _default_copyright_owner

    return old_copyright_owner



def _generate_new_copyright_owner(repo_template_config_params):
    copyright_owner = repo_template_config_params["copyright_owner"]
    new_copyright_owner = copyright_owner

    return new_copyright_owner



def _generate_old_gist_id():
    old_gist_id = _default_gist_id

    return old_gist_id



def _generate_new_gist_id(repo_template_config_params):
    gist_id = repo_template_config_params["gist_id"]
    new_gist_id = gist_id

    return new_gist_id



def _generate_old_license_badge_url():
    old_license_badge_url = ("https://img.shields.io"
                             "/badge/License-GPLv3-blue.svg")

    return old_license_badge_url



def _generate_new_license_badge_url(repo_template_config_params):
    spdx_id = repo_template_config_params["spdx_id"]
    new_license_info = _get_license_info_from_spdx_id(spdx_id)
    new_license_badge_url = new_license_info["license_badge_url"]

    return new_license_badge_url



def _generate_old_license_page_url():
    old_license_page_url = "https://www.gnu.org/licenses/gpl-3.0"

    return old_license_page_url



def _generate_new_license_page_url(repo_template_config_params):
    spdx_id = repo_template_config_params["spdx_id"]
    new_license_info = _get_license_info_from_spdx_id(spdx_id)
    new_license_page_url = new_license_info["license_page_url"]

    return new_license_page_url



def _generate_old_spdx_id():
    old_spdx_id = _default_spdx_id

    return old_spdx_id



def _generate_new_spdx_id(repo_template_config_params):
    spdx_id = repo_template_config_params["spdx_id"]
    new_spdx_id = spdx_id

    return new_spdx_id



def _generate_new_file_contents(filename,
                                text_replacement_map,
                                repo_template_config_params):
    with open(filename, "r") as file_obj:
        line_set = file_obj.read().splitlines()
        original_file_contents = line_set

    kwargs = {"line_set_to_modify": original_file_contents,
              "text_replacement_map": text_replacement_map}
    modified_line_set = _apply_text_replacements_to_line_set(**kwargs)
    modified_file_contents = modified_line_set

    basename = pathlib.Path(filename).name
    file_ext = pathlib.Path(filename).suffix

    kwargs = {"repo_template_config_params": repo_template_config_params}
    if file_ext in (".sh", ".py"):
        kwargs["file_contents"] = modified_file_contents
        modified_file_contents = _update_file_header(**kwargs)
    if basename == "LICENSE":
        kwargs["file_contents"] = modified_file_contents
        modified_file_contents = _update_license_file_text(**kwargs)
    if basename == "pyproject.toml":
        kwargs["file_contents"] = modified_file_contents
        modified_file_contents = _update_author_and_maintainer_info(**kwargs)
    if basename == ".gitlab-ci.yml":
        kwargs["file_contents"] = modified_file_contents
        modified_file_contents = _update_git_test_and_doc_info(**kwargs)

    kwargs = {"line_set_to_modify": modified_file_contents,
              "filename": filename}
    modified_line_set = _apply_text_wrapping_to_line_set(**kwargs)
    modified_file_contents = modified_line_set

    new_file_contents = modified_file_contents

    return new_file_contents



def _apply_text_replacements_to_line_set(line_set_to_modify,
                                         text_replacement_map):
    modified_line_set = line_set_to_modify.copy()
    for line_idx, line_to_modify in enumerate(line_set_to_modify):
        modified_line = line_to_modify.rstrip()
        for old_substring, new_substring in text_replacement_map.items():
            modified_line = modified_line.replace(old_substring, new_substring)
        modified_line_set[line_idx] = modified_line
        if ((re.fullmatch("=+", modified_line)
             or re.fullmatch("-+", modified_line)
             or re.fullmatch("~+", modified_line))
            and (len(modified_line) > 3)):
            modified_line_set[line_idx] = (modified_line[0]
                                           * len(modified_line_set[line_idx-1]))

    return modified_line_set



def _apply_text_wrapping_to_line_set(line_set_to_modify, filename):
    file_extension = os.path.splitext(filename)[1]

    if file_extension == ".py":
        func_alias = _apply_text_wrapping_to_line_set_of_py_file
    elif file_extension in (".md", ".rst"):
        func_alias = _apply_text_wrapping_to_line_set_of_md_or_rst_file
    elif file_extension == ".sh":
        func_alias = _apply_text_wrapping_to_line_set_of_sh_file

    kwargs = {"line_set_to_modify": line_set_to_modify}
    modified_line_set = (func_alias(**kwargs)
                         if (file_extension in (".py", ".md", ".sh", ".rst"))
                         else line_set_to_modify.copy())

    return modified_line_set



def _apply_text_wrapping_to_line_set_of_py_file(line_set_to_modify):
    modified_line_set = line_set_to_modify.copy()

    pattern_1 = r"#\ ((Copyright)|(For\ setting\ up))\ .*"
    pattern_2 = r"\s*((lib_name)|(project)|(copyright_owner))\ =\ \".+"
    pattern_3 = r"\s*r\"\"\".+\ ``.+``.+"

    end_of_file_has_not_been_reached = True
    line_idx = 0
    
    while end_of_file_has_not_been_reached:
        modified_line = modified_line_set[line_idx].rstrip()

        if re.fullmatch(pattern_1, modified_line):
            func_alias = _apply_text_wrapping_to_single_line_python_comment
        elif re.fullmatch(pattern_2, modified_line):
            func_alias = _apply_text_wrapping_to_single_line_variable_assignment
        elif re.fullmatch(pattern_3, modified_line):
            func_alias = _apply_text_wrapping_to_single_line_partial_doc_str
        else:
            func_alias = None

        kwargs = {"line_to_modify": modified_line}
        modified_line_subset = ([modified_line]
                                if (func_alias is None)
                                else func_alias(**kwargs))

        modified_line_set = (modified_line_set[:line_idx]
                             + modified_line_subset
                             + modified_line_set[line_idx+1:])
        
        line_idx += len(modified_line_subset)
        if line_idx >= len(modified_line_set):
            end_of_file_has_not_been_reached = False

    return modified_line_set



_char_limit_per_line = 80



def _apply_text_wrapping_to_single_line_python_comment(line_to_modify):
    modified_line = line_to_modify.rstrip()
    
    char_idx = len(modified_line) - len(modified_line.lstrip())
    indent = " "*char_idx
    
    modified_line = modified_line.lstrip()[2:]

    kwargs = {"text": modified_line,
              "width": _char_limit_per_line-char_idx-2,
              "break_long_words": False}
    lines_resulting_from_text_wrapping = textwrap.wrap(**kwargs)
    
    for line_idx, line in enumerate(lines_resulting_from_text_wrapping):
        lines_resulting_from_text_wrapping[line_idx] = indent + "# " + line

    return lines_resulting_from_text_wrapping



def _apply_text_wrapping_to_single_line_variable_assignment(line_to_modify):
    modified_line = line_to_modify.rstrip()

    if len(modified_line) <= _char_limit_per_line:
        lines_resulting_from_text_wrapping = [modified_line]
    else:
        char_idx_1 = modified_line.find("=")
        char_idx_2 = _char_limit_per_line - (char_idx_1+4)
        
        indent = " "*(char_idx_1+3)
        
        modified_line = modified_line[char_idx_1+2:]

        line_resulting_from_text_wrapping = (line_to_modify[:char_idx_1+2]
                                             + "(\""
                                             + modified_line[1:char_idx_2]
                                             + "\"")
        lines_resulting_from_text_wrapping = [line_resulting_from_text_wrapping]

        modified_line = modified_line[char_idx_2:]

        while len(indent+modified_line)+2 > _char_limit_per_line:
            line_resulting_from_text_wrapping = \
                indent + "\"" + modified_line[:char_idx_2-1] + "\""
            lines_resulting_from_text_wrapping += \
                [line_resulting_from_text_wrapping]

            modified_line = modified_line[char_idx_2-1:]

        line_resulting_from_text_wrapping = \
            indent + "\"" + modified_line + ")"
        lines_resulting_from_text_wrapping += \
            [line_resulting_from_text_wrapping]

    return lines_resulting_from_text_wrapping



def _apply_text_wrapping_to_single_line_partial_doc_str(line_to_modify):
    modified_line = line_to_modify.rstrip()
    
    char_idx = len(modified_line) - len(modified_line.lstrip())
    indent = " "*char_idx

    modified_line = line_to_modify.lstrip()

    kwargs = {"text": modified_line,
              "width": _char_limit_per_line - char_idx,
              "break_long_words": False}
    lines_resulting_from_text_wrapping = textwrap.wrap(**kwargs)

    for line_idx, line in enumerate(lines_resulting_from_text_wrapping):
        lines_resulting_from_text_wrapping[line_idx] = indent + line

    return lines_resulting_from_text_wrapping



def _apply_text_wrapping_to_line_set_of_md_or_rst_file(line_set_to_modify):
    modified_line_set = line_set_to_modify.copy()

    pattern_1 = (r"((\[!\[)|(\s+)|(\*\ )|(\-\ \`)|(\.\.\ )|(\{\%)"
                 r"|(\{\{)|(##)|(#\ \-)|(----+)|(====+)|(~~~~+)).*")
    pattern_2 = r"((----+)|(====+)|(~~~~+))"

    end_of_file_has_not_been_reached = True
    line_idx = 1
    
    while end_of_file_has_not_been_reached:
        modified_line_1 = modified_line_set[line_idx].rstrip()

        if (re.fullmatch(pattern_1, modified_line_1)
            or (modified_line_1 in ("", "#"))):
            modified_line_subset = [modified_line_1]
        else:
            end_of_paragraph_has_not_been_reached = True

            modified_line_2 = ""
            while end_of_paragraph_has_not_been_reached:
                if line_idx+1 < len(modified_line_set):
                    modified_line_2 = modified_line_set[line_idx+1].rstrip()
                    if (re.fullmatch(pattern_1, modified_line_2)
                        or (modified_line_2 in ("", "#"))):
                        end_of_paragraph_has_not_been_reached = False
                    else:
                        modified_line_1 += " " + modified_line_2.lstrip()
                        modified_line_set.pop(line_idx+1)
                else:
                    end_of_paragraph_has_not_been_reached = False

            if re.fullmatch(pattern_2, modified_line_2):
                modified_line_subset = [modified_line_1]
            else:
                kwargs = {"text": modified_line_1,
                          "width": _char_limit_per_line,
                          "break_long_words": False}
                modified_line_subset = textwrap.wrap(**kwargs)

        modified_line_set = (modified_line_set[:line_idx]
                             + modified_line_subset
                             + modified_line_set[line_idx+1:])

        line_idx += len(modified_line_subset)
        end_of_file_has_not_been_reached = (line_idx < len(modified_line_set))

    lines_resulting_from_text_wrapping = modified_line_set

    return lines_resulting_from_text_wrapping



def _apply_text_wrapping_to_line_set_of_sh_file(line_set_to_modify):
    modified_line_set = line_set_to_modify.copy()

    pattern = r"#\ .+"

    end_of_file_has_not_been_reached = True
    line_idx = 2
    
    while end_of_file_has_not_been_reached:
        modified_line_1 = modified_line_set[line_idx].rstrip()

        if re.fullmatch(pattern, modified_line_1):
            prefix = "# "
            end_of_paragraph_has_not_been_reached = True
            
            while end_of_paragraph_has_not_been_reached:
                modified_line_2 = modified_line_set[line_idx+1].rstrip()
                if re.fullmatch(pattern, modified_line_2):
                    modified_line_1 += " " + modified_line_2.lstrip(prefix)
                    modified_line_set.pop(line_idx+1)
                else:
                    end_of_paragraph_has_not_been_reached = False

            kwargs = {"text": modified_line_1,
                      "width": _char_limit_per_line,
                      "subsequent_indent": prefix,
                      "break_long_words": False}
            modified_line_subset = textwrap.wrap(**kwargs)
        else:
            modified_line_subset = [modified_line_1]

        modified_line_set = (modified_line_set[:line_idx]
                             + modified_line_subset
                             + modified_line_set[line_idx+1:])

        line_idx += len(modified_line_subset)
        if line_idx >= len(modified_line_set):
            end_of_file_has_not_been_reached = False

    lines_resulting_from_text_wrapping = modified_line_set

    return lines_resulting_from_text_wrapping



def _update_file_header(repo_template_config_params, file_contents):
    line_idx = -1
    substring_0 = "Copyright"
    substring_1 = ">."
    
    beg_of_file_header_has_not_been_found = True
    while beg_of_file_header_has_not_been_found:
        line_idx += 1
        line = file_contents[line_idx]
        beg_of_file_header_has_not_been_found = (substring_0 not in line)
    start = line_idx

    end_of_file_header_has_not_been_found = True
    while end_of_file_header_has_not_been_found:
        line_idx += 1
        line = file_contents[line_idx]
        end_of_file_header_has_not_been_found = (substring_1 not in line)
    stop = line_idx+1

    lines_before_old_file_header = file_contents[:start]
    old_file_header = file_contents[start:stop]
    lines_after_old_file_header = file_contents[stop:]

    new_file_header = repo_template_config_params["file_header"]
    new_file_header = (list(new_file_header)
                       if (new_file_header is not None)
                       else old_file_header)

    modified_file_contents = (lines_before_old_file_header
                              + new_file_header
                              + lines_after_old_file_header)

    return modified_file_contents



def _update_license_file_text(repo_template_config_params, file_contents):
    spdx_id = repo_template_config_params["spdx_id"]

    license_info = _get_license_info_from_spdx_id(spdx_id)
    license_text = license_info["license_text"]

    modified_file_contents = license_text

    return modified_file_contents



def _update_author_and_maintainer_info(repo_template_config_params,
                                       file_contents):
    line_idx = -1
    substring_0 = "authors = ["
    substring_1 = "license ="
    
    beg_of_author_and_maintainer_info_has_not_been_found = True
    while beg_of_author_and_maintainer_info_has_not_been_found:
        line_idx += 1
        line = file_contents[line_idx]
        beg_of_author_and_maintainer_info_has_not_been_found = (substring_0
                                                                not in
                                                                line)
    start = line_idx

    end_of_author_and_maintainer_info_has_not_been_found = True
    while end_of_author_and_maintainer_info_has_not_been_found:
        line_idx += 1
        line = file_contents[line_idx]
        end_of_author_and_maintainer_info_has_not_been_found = (substring_1
                                                                not in
                                                                line)
    stop = line_idx

    lines_before_old_author_and_maintainer_info = file_contents[:start]
    old_author_and_maintainer_info = file_contents[start:stop]
    lines_after_old_author_and_maintainer_info = file_contents[stop:]
    
    new_author_and_maintainer_info = []
    for key_category in ("author", "maintainer"):
        config_param_name = key_category+"_to_email_map"
        name_to_email_map = repo_template_config_params[config_param_name]
        new_author_and_maintainer_info += [key_category+"s = ["]
        for name, email in name_to_email_map.items():
            line = "    {name = \""+name+"\", email = \""+email+"\"},"
            new_author_and_maintainer_info += [line]
        new_author_and_maintainer_info += ["]"]

    modified_file_contents = (lines_before_old_author_and_maintainer_info
                              + new_author_and_maintainer_info
                              + lines_after_old_author_and_maintainer_info)

    return modified_file_contents



def _update_git_test_and_doc_info(repo_template_config_params, file_contents):
    line_idx = -1
    substring = "    - <INSERT"
    modified_file_contents = file_contents.copy()

    eof_has_not_been_reached = True

    while eof_has_not_been_reached:
        tag_sec_search_has_not_been_completed = True
        while tag_sec_search_has_not_been_completed:
            line_idx += 1
            line = modified_file_contents[line_idx]
            current_total_line_count = len(modified_file_contents)
            eof_has_not_been_reached = (line_idx < current_total_line_count-1)
            tag_sec_search_has_not_been_completed = (eof_has_not_been_reached
                                                     and
                                                     (substring not in line))

        if substring in line:
            tag_category = line.split("_")[1].lower()

            start = line_idx
            stop = start+1
    
            lines_before_old_tag_info = modified_file_contents[:start]
            old_tag_info = modified_file_contents[start:stop]
            lines_after_old_tag_info = modified_file_contents[stop:]

            config_param_name = "gitlab_"+tag_category+"_tags"
            tags = repo_template_config_params[config_param_name]
            new_tag_info = []
            for tag in tags:
                new_tag_info += ["    - "+tag]
            new_tag_info = (new_tag_info
                            if (len(new_tag_info) > 0)
                            else old_tag_info)
        
            modified_file_contents = (lines_before_old_tag_info
                                      + new_tag_info
                                      + lines_after_old_tag_info)

            current_total_line_count = len(modified_file_contents)
            eof_has_not_been_reached = (line_idx < current_total_line_count-1)

    return modified_file_contents



def _print_generate_local_git_repo_template_end_msg(
        start_time,
        path_to_directory_to_contain_new_repo,
        repo_name):
    elapsed_time = time.time() - start_time
    path_to_local_git_repo_template = (path_to_directory_to_contain_new_repo
                                       + "/"
                                       + repo_name)

    unformatted_msg = ("Finished generating the local ``git`` repository, "
                       "which is located at the path ``'{}'``. Time taken to "
                       "generate the local ``git`` repository: {} "
                       "s.\n\n\n")
    msg = unformatted_msg.format(path_to_local_git_repo_template,
                                 elapsed_time)
    print(msg)

    return None



def _run_pylibtemplate_as_an_app(cmd_line_args=None):
    converted_cmd_line_args = _parse_and_convert_cmd_line_args(cmd_line_args)
    config_filename = converted_cmd_line_args["config_filename"]

    with open(config_filename, "r", encoding="utf-8") as file_obj:
        config = json.load(file_obj)

    kwargs = config
    generate_local_git_repo_template(**kwargs)

    return None



def _parse_and_convert_cmd_line_args(cmd_line_args):
    current_func_name = "_parse_and_convert_cmd_line_args"

    try:
        parser = argparse.ArgumentParser()
        arg_names = ("config_filename",)
        for arg_name in arg_names:
            parser.add_argument("--"+arg_name, type=str, required=True)
        args = parser.parse_args(cmd_line_args)
        config_filename = args.config_filename
    except:
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise SystemExit(err_msg)

    converted_cmd_line_args = {"config_filename": config_filename}
    
    return converted_cmd_line_args



###########################
## Define error messages ##
###########################

_check_and_convert_lib_name_for_imports_err_msg_1 = \
    ("The object ``lib_name_for_imports`` must be a string that is a valid "
     "identifier.")

_check_and_convert_abbreviated_lib_name_for_docs_err_msg_1 = \
    _check_and_convert_lib_name_for_imports_err_msg_1

_check_and_convert_author_to_email_map_err_msg_1 = \
    ("The key ``'{}'`` in the dictionary ``author_to_email_map`` must be a "
     "string.")

_check_and_convert_maintainer_to_email_map_err_msg_1 = \
    ("The key ``'{}'`` in the dictionary ``maintainer_to_email_map`` must be a "
     "string.")

_check_and_convert_spdx_id_err_msg_1 = \
    ("The object ``spdx_id``, which was set to ``'{}'``, must be a string that "
     "is a valid SPDX ID identifier that is also supported by "
     "``pylibtemplate``.")

_get_spdx_json_data_err_msg_1 = \
    ("The object ``spdx_id``, which was set to ``'{}'``, must be a string that "
     "is a valid SPDX ID identifier.")

_make_output_dir_err_msg_1 = \
    ("An error occurred in trying to make the directory ``'{}'``: see "
     "traceback for details.")

_clone_pylibtemplate_repo_err_msg_1 = \
    ("An error occurred while trying to clone the ``pylibtemplate`` "
     "repository: see the traceback for details.")

_parse_and_convert_cmd_line_args_err_msg_1 = \
    ("The correct form of the command is:\n"
     "\n"
     "    pylibtemplate "
     "--config_filename=<config_filename>\n"
     "\n"
     "where ``<config_filename>`` is a path to a configuration file, which is "
     "expected to be a JSON file that stores a valid instance of each "
     "parameter of the function "
     "``pylibtemplate.generate_local_git_repo_template``. For details, see the "
     "documentation for the library ``pylibtemplate`` via the link "
     "link https://mrfitzpa.github.io/pylibtemplate, and navigate the "
     "reference guide for the version of the library that is installed.")



#########################
## Main body of script ##
#########################

_ = (_run_pylibtemplate_as_an_app()
     if (__name__ == "__main__")
     else None)
