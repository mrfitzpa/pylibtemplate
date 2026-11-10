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
r"""Build the static documentation website files.

To generate the documentation, you will also need to install several other
packages. This can be done by running the following command from the root of the
repository::

  pip install .[docs]

Next, assuming that you are in the root of the repository, and that you have
installed all the prerequisite packages, you can generate the static
documentation website files by issuing the following commands::

  cd docs
  python build_docs --root_url=<root_url> --doc_dir_basename=<doc_dir_basename>

where ``<root_url>`` is the URL of the root of your documentation webpage, and
``<doc_dir_basename>`` is the basename of the directory in which the generated
static documentation files will be stored, the full path being
``<repo_root>/<doc_dir_basename>``, with ``<repo_root>`` being the root of the
repository. The default values of ``<root_url>`` and ``<doc_dir_basename>`` are
``<repo_root>/pages`` and ``pages`` respectively.

The code below was adopted from
``https://github.com/ThoSe1990/SphinxExample/blob/main/docs/build_docs.py``.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For parsing command line arguments.
import argparse

# For running terminal commands.
import subprocess

# For storing terminal environment variables and getting the path to current
# script.
import os

# For creating path objects.
import pathlib

# For pattern matching.
import re



#####################################
## Load libraries/packages/modules ##
#####################################

# For parsing command line arguments.
import argparse

# For running terminal commands.
import subprocess

# For storing terminal environment variables and getting the path to current
# script.
import os

# For creating path objects.
import pathlib

# For pattern matching.
import re



##################################
## Define classes and functions ##
##################################

def _parse_and_convert_cmd_line_args():
    path_to_current_script = pathlib.Path(os.path.realpath(__file__))
    default_doc_dir_basename = "pages"
    default_root_url = (str(path_to_current_script.parents[1])
                        + "/" + default_doc_dir_basename)

    current_func_name = "_parse_and_convert_cmd_line_args"

    try:
        parser = argparse.ArgumentParser()
        arg_names = ("root_url", "doc_dir_basename")
        default_values = (default_root_url, default_doc_dir_basename)
        for arg_name, default_value in zip(arg_names, default_values):
            parser.add_argument("--"+arg_name, default=default_value)
        args = parser.parse_args()
        root_url = args.root_url
        doc_dir_basename = args.doc_dir_basename
    except:
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise SystemExit(err_msg)

    converted_cmd_line_args = {"root_url": root_url,
                               "doc_dir_basename": doc_dir_basename}
    
    return converted_cmd_line_args



def _check_that_worktree_is_clean():
    git_status_output = subprocess.check_output("git status --porcelain",
                                                shell=True)

    current_func_name = "_check_that_worktree_is_clean"

    if len(git_status_output.strip()) > 0:
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise SystemExit(err_msg)

    return None



def _build_doc(version, language, tag):
    os.environ["current_version"] = version
    os.environ["current_language"] = language

    if tag is not None:
        subprocess.run("git checkout " + tag,
                       shell=True)
        subprocess.run("git checkout main -- conf.py",
                       shell=True)
        subprocess.run("git checkout main -- _templates/versions.html",
                       shell=True)

    subprocess.run("cd ..; pip install .; cd docs", shell=True)

    os.environ["SPHINXOPTS"] = "-D language='{}'".format(language)
    subprocess.run("make html", shell=True)

    if tag is not None:
        subprocess.run("git checkout -f main", shell=True)

    return None



def _mvdir(src, dst):
    subprocess.run(["mkdir", "-p", dst])
    subprocess.run("mv "+src+"* "+dst, shell=True)

    return None



###########################
## Define error messages ##
###########################

_parse_and_convert_cmd_line_args_err_msg_1 = \
    ("The correct form of the command is:\n"
     "\n"
     "    python build_docs "
     "--root_url=<root_url> "
     "--doc_dir_basename=<doc_dir_basename>\n"
     "\n"
     "where ``<root_url>`` must be a valid URL, and ``<doc_dir_basename>`` "
     "must be a valid directory basename.")

_check_that_worktree_is_clean_err_msg_1 = \
    ("The building of the documentation website files has been aborted because "
     "the working tree has uncommited changes: commit or stash these changes "
     "first.")



#########################
## Main body of script ##
#########################

converted_cmd_line_args = _parse_and_convert_cmd_line_args()
root_url = converted_cmd_line_args["root_url"]
doc_dir_basename = converted_cmd_line_args["doc_dir_basename"]

_check_that_worktree_is_clean()

os.environ["build_all_docs"] = str(True)
os.environ["pages_root"] = root_url.rstrip("/")

_build_doc("latest", "en", None)
_mvdir("./_build/html/",
       "./"+doc_dir_basename+"/")

cmd_output_as_bytes = subprocess.check_output("git tag", shell=True)
cmd_output = cmd_output_as_bytes.decode("utf-8")
tag_set = cmd_output.rstrip("\n").split("\n")

pattern = r"v[0-9]+\.[0-9]+\.[0-9]+"
release_tag_set = tuple(tag for tag in tag_set if re.fullmatch(pattern, tag))

version_subset = dict()
for tag in release_tag_set:
    version = tag[1:]
    major, minor, patch = [int(int_as_str) for int_as_str in version.split(".")]
    version_subset.setdefault(major, dict())
    version_subset[major].setdefault(minor, 0)
    version_subset[major][minor] = max(version_subset[major][minor], patch)

for major in sorted(version_subset.keys()):
    for minor in sorted(version_subset[major].keys()):
        patch = version_subset[major][minor]
        version = "{}.{}.{}".format(major, minor, patch)
        tag = "v"+version
        major_minor = "{}.{}".format(major, minor)
        language = "en"
        _build_doc(version, language, tag)
        _mvdir("./_build/html/",
               "./"+doc_dir_basename+"/"+major_minor+"/"+language+"/")

subprocess.run("cd ..; pip install .; cd docs", shell=True)
_mvdir("./"+doc_dir_basename+"/",
       "../"+doc_dir_basename+"/")
