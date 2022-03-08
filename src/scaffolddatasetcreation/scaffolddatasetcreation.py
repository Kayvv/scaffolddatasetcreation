import argparse
import os


def create_dataset(dataset_dir):
    create_folders(dataset_dir)

def create_folders(path):
    folder_dir = []
    folder_dir.append(os.path.join(path, "files", "derivative", "Scaffold"))
    folder_dir.append(os.path.join(path, "files", "derivative"))
    folder_dir.append(os.path.join(path, "files", "docs"))
    folder_dir.append(os.path.join(path, "files", "primary"))
    for filename in folder_dir:
        create_folder(filename)

def create_folder(path):
    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)


def main():
    parser = argparse.ArgumentParser(description='Create a SPARC dataset.')
    parser.add_argument("dataset_dir", help='directory to create.')

    args = parser.parse_args()
    dataset_dir = args.dataset_dir

    # Create folders
    create_dataset(dataset_dir)


if __name__ == "__main__":
    main()