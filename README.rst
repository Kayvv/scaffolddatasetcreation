
SPARC Scaffold Dataset Creation Script
======================================

A script to help with create SPARC datasets.

How to use (can also be found using :code:`python src\scaffolddatasetcreation\scaffolddatasetcreation.py -h`):

usage: :code:`scaffolddatasetcreation.py [-h] dataset_dir mesh_config_file argon_document`

Create a SPARC dataset.

**positional arguments:**

================== =================================================
  dataset_dir       directory to create.
  mesh_config_file  mesh config json file to generate mesh exf file.
  argon_document    argon document file to generate webGL files.
================== =================================================

**optional arguments:**

  -h, --help        show this help message and exit


**Running the script:**

To run the script create a virtual environment with a tool like :code:`virtualenv`. 
Install it with :code:`pip install virtualenv`.

Use :code:`virtualenv` to create a new virtual environment:

::

  virtualenv venv_scaffolddatasetcreation

Activate the virtual environment:

::

  source venv_scaffolddatasetcreation/bin/activate

For bash shells, or:

::

  venv_scaffolddatasetcreation\\Scripts\\activate

For a windows :code:`cmd` prompt.

With the activated virtual environment install the script requirements

::

  pip install -r requirements.txt

Then execute the script to print out the usage information to test the script:

::

  python scaffolddatasetcreation.py -h

Examples:
---------

::

  python scaffolddatasetcreation.py <dataset_dir> <mesh_config_file> <argon_document>
