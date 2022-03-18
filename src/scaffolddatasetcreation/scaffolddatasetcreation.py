import argparse
import os
import json
from opencmiss.zinc.context import Context

from scaffoldmaker.scaffolds import Scaffolds
from scaffoldmaker.scaffoldpackage import ScaffoldPackage

import scaffoldmaker.scaffolds as sc

from opencmiss.exporter.webgl import ArgonSceneExporter as WebGLExporter
from opencmiss.exporter.thumbnail import ArgonSceneExporter as ThumbnailExporter

def create_dataset(dataset_dir, mesh_config_file, argon_document):
    create_folders(dataset_dir)
    generate_mesh(os.path.join(dataset_dir, "primary"), mesh_config_file)
    generate_webGL((os.path.join(dataset_dir, "derivative", "Scaffold")), argon_document)

def create_folders(path):
    folder_dir = []
    folder_dir.append(os.path.join(path, "derivative", "Scaffold"))
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

def generate_mesh(output_dir, mesh_config_file):
    context = Context("MeshGenerator")
    region = context.createRegion()
    f = open(mesh_config_file)
    scaffoldConfig = json.load(f)
    scaffoldType = scaffoldConfig["generator_settings"]["scaffoldPackage"]
    scaffoldPackage = sc.Scaffolds_decodeJSON(scaffoldType)
    scaffoldPackage.generate(region, applyTransformation=False)
    file_name = os.path.join(output_dir, "scaffold_mesh.exf")
    region.writeFile(file_name)

def generate_webGL(output_dir, argon_document):
    exporter = WebGLExporter(output_dir)
    exportFile(exporter, argon_document)
    exporter = ThumbnailExporter(output_dir)
    exportFile(exporter, argon_document)

def exportFile(exporter, argon_document):
    exporter.set_filename(argon_document)
    exporter.set_parameters({
        "prefix": 'prefix',
        "numberOfTimeSteps": None,
        "initialTime": None,
        "finishTime": None,
    })
    exporter.export()

def main():
    parser = argparse.ArgumentParser(description='Create a SPARC dataset.')
    parser.add_argument("dataset_dir", help='directory to create.')
    parser.add_argument("mesh_config_file", help='mesh config json file to generate mesh exf file.')
    parser.add_argument("argon_document", help='argon document file to generate webGL files.')

    args = parser.parse_args()
    dataset_dir = args.dataset_dir
    mesh_config_file = args.mesh_config_file
    argon_document = args.argon_document

    # Create dataset
    create_dataset(dataset_dir, mesh_config_file, argon_document)


if __name__ == "__main__":
    main()