import os
import shutil
import tempfile
import uuid
from contextlib import contextmanager


@contextmanager
def tmp_directory():
    # I am pretty sure the uuid here does nothjing, but lets make sure the
    # tmpdir is always unique
    tmp_dir = tempfile.mkdtemp('_recipe_h' + uuid.uuid4().hex[0:6])
    yield tmp_dir
    shutil.rmtree(tmp_dir)


# https://stackoverflow.com/questions/6194499/pushd-through-os-system
@contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


def parse_conda_pkg(pkg):
    """Parse a conda package into its parts.

    code due to Isuru F. and CJ Wright

    Returns platform, name, version and build string
    """
    if not pkg.endswith(".tar.bz2"):
        raise RuntimeError("Package must end with .tar.bz2!")
    pkg = pkg[:-8]
    plat, pkg_name = pkg.split(os.path.sep)
    name_ver, build = pkg_name.rsplit('-', 1)
    name, ver = name_ver.rsplit('-', 1)
    return plat, name, ver, build
