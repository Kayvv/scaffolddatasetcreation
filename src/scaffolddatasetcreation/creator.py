import argparse
import os
import json
from opencmiss.zinc.context import Context

from scaffoldmaker.scaffolds import Scaffolds
from scaffoldmaker.scaffoldpackage import ScaffoldPackage

import scaffoldmaker.scaffolds as sc

from opencmiss.exporter.webgl import ArgonSceneExporter as WebGLExporter
from opencmiss.exporter.thumbnail import ArgonSceneExporter as ThumbnailExporter

from sparc.curation.tools.manifests import ManifestDataFrame
from sparc.curation.tools.ondisk import OnDiskFiles
from sparc.curation.tools.utilities import convert_to_bytes
from sparc.curation.tools.scaffold_annotations import get_errors, fix_error, get_confirmation_message

def create_dataset(dataset_dir, mesh_config_file, argon_document):
    # Create dataset
    create_folders(dataset_dir)
    generate_mesh(os.path.join(dataset_dir, "primary"), mesh_config_file)
    generate_webGL((os.path.join(dataset_dir, "derivative", "Scaffold")), argon_document)
    # Dataset annotation
    annotateScaffold(dataset_dir)

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

def annotateScaffold(dataset_dir):
    errors = getCurrentErrors(dataset_dir)
    previous_error = []
    while len(errors) != 0:
        for error in errors:
            print(error.get_error_message())
            fix_error(error)
            if error.get_error_message() in previous_error:
                print("This error can't be fixed automatically.")
                break
            else:
                previous_error.append(error.get_error_message())
        errors = getCurrentErrors(dataset_dir)

def getCurrentErrors(dataset_dir):
    max_size = convert_to_bytes('3MiB')
    OnDiskFiles().setup_dataset(dataset_dir, max_size)
    ManifestDataFrame().setup_dataframe(dataset_dir)
    return get_errors()

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