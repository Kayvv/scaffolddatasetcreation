
SPARC Dataset Creation
======================

A package to help with creating SPARC datasets.
Currently, support is available to create scaffold based SPARC datasets.

Install
-------

SPARC dataset tools can be installed from PyPi.org with the following command::

  pip install sparc-dataset-tools

Usage
-----

How to use (can also be found using :code:`create-scaffold-dataset -h`):

usage: :code:`create-scaffold-dataset [-h] dataset_dir mesh_config_file argon_document`

Create a Scaffold based SPARC dataset from a scaffold description file and an Argon document.

**positional arguments:**

================== =================================================
  dataset_dir       root directory for new dataset.
  mesh_config_file  mesh config json file to generate scaffold.
  argon_document    argon document file to generate webGL files.
================== =================================================

**optional arguments:**

=============     =================================
 -h, --help        show this help message and exit
=============     =================================

Run
---

To run the application create a virtual environment.

::

  python -m venv venv_sparc

Activate the virtual environment::

  source venv_sparc/bin/activate

For bash shells, or::

  venv_sparc\Scripts\activate

For a windows :code:`cmd` prompt.

With the activated virtual environment install the package.

::

  pip install sparc-dataset-tools

Then execute the application to print out the usage information to test the script.

::

  create-scaffold-dataset -h

Examples:
---------

::

  create-scaffold-dataset <dataset_dir> <mesh_config_file> <argon_document>
