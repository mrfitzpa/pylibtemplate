# -*- coding: utf-8 -*-
# Copyright 2025 Matthew Fitzpatrick.
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
r"""Configuration file for the Sphinx documentation builder.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For importing libraries.
import importlib

# For aborting the python script with a specific error code.
import sys

# For accessing terminal environment variables.
import os

# For running terminal commands.
import subprocess

# For pattern matching.
import re



##############################################
## Define classes, functions, and constants ##
##############################################

## Project information.

project = "pylibtemplate"
author = "Matthew Fitzpatrick"
copyright = "2025, {}".format(author)



## General configuration.

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = ["sphinx.ext.autodoc",
              "sphinx.ext.autosummary",
              "sphinx.ext.extlinks",
              "sphinx.ext.intersphinx",
              "sphinx.ext.todo",
              "sphinx.ext.coverage",
              "sphinx.ext.mathjax",
              "sphinx.ext.viewcode",
              "sphinx_autodoc_typehints",
              "sphinx.ext.githubpages",
              "numpydoc"]



# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]



# Avoid a bunch of warnings when using properties with doc strings in classes.
# see https://github.com/phn/pytpm/issues/3#issuecomment-12133978
numpydoc_show_class_members = True
numpydoc_show_inherited_class_members = True
numpydoc_class_members_toctree = False



autosummary_generate = True
autoclass_content = "both"
html_show_sourcelink = False
autodoc_inherit_docstrings = True
set_type_checking_flag = True
add_module_names = False



# For equation numbering by section.
numfig = True
math_numfig = True
numfig_secnum_depth = 6



# Cross links to other sphinx documentation websites.
intersphinx_mapping = \
    {"python": ("https://docs.python.org/3", None),
     "numpy": ("https://numpy.org/doc/stable", None)}



# External links.
extlinks = {"arxiv": ("https://arxiv.org/abs/%s", "arXiv:%s"),
            "doi": ("https://dx.doi.org/%s", "doi:%s")}



## Options for HTML output.

html_theme = "sphinx_rtd_theme"
html_theme_options = {"display_version": False}



# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]



# If not "", a "Last updated on:" timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"



# Override some CSS settings.
html_css_files = ["readthedocs_custom.css"]



## Defining functions to be used in the main body of script.

def import_project_lib(project):
    try:
        _ = importlib.import_module(name=project)
    except:
        unformatted_err_msg = "ERROR: can't import ``{}``."
        err_msg = unformatted_err_msg.format(project)
        print(err_msg)
        sys.exit(1)
        
    return None



def extract_major_minor_from_version(version):
    major, minor, patch = ((None, None, None)
                           if (version == "latest")
                           else version.split("."))
    major_minor = "latest" if (major is None) else "{}.{}".format(major, minor)

    return major_minor



def generate_version_subset():
    cmd_output_as_bytes = subprocess.check_output("git tag", shell=True)
    cmd_output = cmd_output_as_bytes.decode("utf-8")
    tag_set = cmd_output.rstrip("\n").split("\n")

    pattern = r"v[0-9]+\.[0-9]+\.[0-9]+"
    release_tag_set = tuple(tag
                            for tag
                            in tag_set
                            if re.fullmatch(pattern, tag))

    version_subset = dict()
    for tag in release_tag_set:
        version = tag[1:]
        major, minor, patch = [int(int_as_str)
                               for int_as_str
                               in version.split(".")]
        version_subset.setdefault(major, dict())
        version_subset[major].setdefault(minor, 0)
        version_subset[major][minor] = max(version_subset[major][minor], patch)

    return version_subset



###########################
## Define error messages ##
###########################

_import_project_lib_err_msg_1 = \
    ("Error: cannot import ``{}``.")



#########################
## Main body of script ##
#########################

## Check to see whether the project library can be imported.
import_project_lib(project)



# Adapted from
# ``https://github.com/ThoSe1990/SphinxExample/blob/main/docs/conf.py``.
build_all_docs = os.environ.get("build_all_docs", None)
pages_root = os.environ.get("pages_root", "")

if build_all_docs is not None:
    current_language = os.environ.get("current_language")    
    current_version = os.environ.get("current_version")

    kwargs = {"version": current_version}
    current_major_minor = extract_major_minor_from_version(**kwargs)

    html_context = {"current_language" : current_language,
                    "languages" : [],
                    "current_version" : current_major_minor,
                    "versions" : []}

    if current_version == "latest":
        html_context["languages"].append(["en", pages_root])

    if current_language == "en":
        html_context["versions"].append(["latest", pages_root])

    version_subset = generate_version_subset()

    if current_version != "latest":
        language = "en"
        path = pages_root+"/"+current_major_minor+"/"+language
        html_context["languages"].append([language, path])

    for major in sorted(version_subset.keys()):
        for minor in sorted(version_subset[major].keys()):
            major_minor = "{}.{}".format(major, minor)
            path = pages_root+"/"+major_minor+"/"+current_language
            html_context["versions"].append([major_minor, path])
