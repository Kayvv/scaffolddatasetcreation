import argparse
import os
import json
from opencmiss.zinc.context import Context

from scaffoldmaker.scaffolds import Scaffolds
from scaffoldmaker.scaffoldpackage import ScaffoldPackage

import scaffoldmaker.scaffolds as sc


def create_dataset(dataset_dir, mesh_config_file):
    create_folders(dataset_dir)
    generate_mesh(mesh_config_file)

def create_folders(path):
    folder_dir = []
    folder_dir.append(os.path.join(path, "derivative", "Scaffold"))
    folder_dir.append(os.path.join(path, "derivative"))
    folder_dir.append(os.path.join(path, "docs"))
    folder_dir.append(os.path.join(path, "primary"))
    for filename in folder_dir:
        create_folder(filename)

def create_folder(path):
    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)

def generate_mesh(mesh_config_file):
    context = Context("MeshGenerator")
    region = context.createRegion()
    f = open(mesh_config_file)
    scaffoldConfig = json.load(f)
    scaffoldType = scaffoldConfig["generator_settings"]["scaffoldPackage"]
    scaffoldPackage = sc.Scaffolds_decodeJSON(scaffoldType)
    scaffoldPackage.generate(region, applyTransformation=False)
    file_name = "mesh.exf"
    region.writeFile(file_name)

def main():
    parser = argparse.ArgumentParser(description='Create a SPARC dataset.')
    parser.add_argument("dataset_dir", help='directory to create.')
    parser.add_argument("mesh_config_file", help='mesh config json file to generate mesh exf file.')

    args = parser.parse_args()
    dataset_dir = args.dataset_dir
    mesh_config_file = args.mesh_config_file

    # Create folders
    create_dataset(dataset_dir, mesh_config_file)


if __name__ == "__main__":
    main()