import os.path
import sys

import dulwich.repo
import dulwich.porcelain
import dulwich.client
import dulwich.index

from dulwich.index import get_unstaged_changes
from dulwich.refs import LOCAL_BRANCH_PREFIX
from dulwich.objectspec import parse_tree
from dulwich.porcelain import get_tree_changes, update_head, get_untracked_paths

LOCAL_REMOTE_PREFIX = b"refs/remotes/"

here = os.path.abspath(os.path.dirname(__file__))


def setup_resources():
    url = "https://github.com/hsorby/sparc-dataset-curation-test-resources.git"
    environment_location = os.environ.get("SPARC_DATASET_CURATION_TEST_RESOURCES", "<not-set>")
    default_resources_path = os.path.join(here, "resources")
    readme_file = os.path.join(default_resources_path, "README.rst")
    if os.path.isfile(os.path.join(environment_location, "README.rst")):
        repo = dulwich.repo.Repo(environment_location, bare=False)
    elif os.path.isfile(readme_file):
        repo = dulwich.repo.Repo(default_resources_path, bare=False)
    else:
        repo = dulwich.porcelain.clone(url, os.path.join(here, "resources"))
        if not os.path.isfile(readme_file):
            sys.exit(1)

    return repo


def dulwich_checkout(repo, target):
    checkout(repo, target)


class DirNotCleanError(Exception):
    """Indicates that the working directory is not clean while trying to checkout."""


def checkout(repo, target: bytes, force: bool = False):
    """switch branches or restore working tree files
    Args:
      repo: dulwich Repo object
      target: branch name or commit sha to checkout
      force: true or not to force checkout
    """
    # Check repo status.
    if not force:
        index = repo.open_index()
        for file in get_tree_changes(repo)['modify']:
            if file in index:
                raise DirNotCleanError('trying to checkout when working directory not clean')

        normalizer = repo.get_blob_normalizer()
        filter_callback = normalizer.checkin_normalize

        unstaged_changes = list(get_unstaged_changes(index, repo.path, filter_callback))
        for file in unstaged_changes:
            if file in index:
                raise DirNotCleanError('trying to checkout when working directory not clean')

    current_tree = parse_tree(repo, repo.head())
    target_tree = parse_tree(repo, target)

    # Update head.
    if target == b'HEAD':  # Do not update head while trying to checkout to HEAD.
        pass
    elif target in repo.refs.keys(base=LOCAL_BRANCH_PREFIX):
        update_head(repo, target)
    else:
        # If checking out a remote branch, create a local one without the remote name prefix.
        config = repo.get_config()
        name = target.split(b"/")[0]
        section = (b"remote", name)
        if config.has_section(section):
            checkout_target = target.replace(name + b"/", b"")
            try:
                dulwich.porcelain.branch_create(repo, checkout_target, (LOCAL_REMOTE_PREFIX + target).decode())
            except dulwich.porcelain.Error:
                pass
            update_head(repo, LOCAL_BRANCH_PREFIX + checkout_target)
        else:
            update_head(repo, target, detached=True)

    # Un-stage files in the current_tree or target_tree.
    tracked_changes = []
    for change in repo.open_index().changes_from_tree(repo.object_store, target_tree.id):
        file = change[0][0] or change[0][1]  # No matter whether the file is added, modified, or deleted.
        try:
            current_entry = current_tree.lookup_path(repo.object_store.__getitem__, file)
        except KeyError:
            current_entry = None
        try:
            target_entry = target_tree.lookup_path(repo.object_store.__getitem__, file)
        except KeyError:
            target_entry = None

        if current_entry or target_entry:
            tracked_changes.append(file.decode())

    repo.unstage(tracked_changes)

    target_sha = target_tree.sha()
    repo.reset_index(target_sha.hexdigest())

    # Remove the untracked file which are in the current_file_set.
    for file in get_untracked_paths(repo.path, repo.path, repo.open_index(), exclude_ignored=True):
        try:
            current_tree.lookup_path(repo.object_store.__getitem__, file.encode())
        except KeyError:
            pass
        else:
            os.remove(os.path.join(repo.path, file))
