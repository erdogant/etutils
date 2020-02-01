"""Make new release on github and pypi."""

import argparse
import os
import re
import numpy as np
import urllib.request
import yaml
import shutil
from packaging import version
yaml.warnings({'YAMLLoadWarning': False})
TWINE_PATH = 'C://Users/Erdogan/AppData/Roaming/Python/Python36/Scripts/twine.exe upload dist/*'


def github_version(githubname, packagename, verbose=3):
    """Get latest github version for package.

    Parameters
    ----------
    githubname : String
        Name of the github account.
    packagename : String
        Name of the package.
    verbose : int, optional
        Print message. The default is 3.

    Returns
    -------
    github_version : String
        Version number of the latest github package.

    """
    # Pull latest from github
    print('[release] git pull')
    os.system('git pull')
    # Get latest version of github release
    try:
        github_url = 'https://api.github.com/repos/' + githubname + '/' + packagename + '/releases/latest'
        if verbose>=4: print('[release] Github url: %s' %(github_url))
        github_page = urllib.request.urlopen(github_url)
        github_data = github_page.read()
        github_version = yaml.load(github_data)['tag_name']

        if verbose>=3: print('[release] Github version: %s' %(github_version))
        if verbose>=3: print('[release] Github version requested from: %s' %(github_url))
    except:
        if verbose>=1: print('[release] ERROR: Can not find the latest github version!\nPrivate repo? or doest not exists? or there is no release yet?: [https://github.com//%s/%s]' %(githubname, packagename))
        github_version = '9.9.9'

    return github_version


def _make_build_and_install(packagename, current_version):
    # Make new build
    print('Making new wheel..')
    os.system('python setup.py bdist_wheel')
    # Make new build
    print('Making source build..')
    os.system('python setup.py sdist')
    # Install new wheel
    print('Installing new wheel..')
    os.system('pip install -U dist/' + packagename + '-' + current_version + '-py3-none-any.whl')


def _github_set_tag_and_push(current_version, verbose=3):
    # git commit
    if verbose>=3: print('[release] git add->commit->push')
    os.system('git add .')
    os.system('git commit -m v' + current_version)
    # os.system('git push')
    # Set tag for this version
    if verbose>=3: print('Set new version tag: %s' %(current_version))
    # git tag -a v0.1.0 -d v0.1.0
    os.system('git tag -a v' + current_version + ' -m "v' + current_version + '"')
    # os.system('git tag -a ' + current_version + ' -m "' + current_version + '"')
    os.system('git push origin --tags')
    if verbose>=2: print('[release] WARNING: WHAT NEEDS TO BE DONE: Go to your github most recent releases (this one) and [edit tag] > the set the version nubmer in the [Release title].')


def _make_clean(packagename, clean=True, verbose=3):
    if clean:
        if verbose>=3: print('[release] Removing local build directories..')
        if os.path.isdir('dist'): shutil.rmtree('dist')
        if os.path.isdir('build'): shutil.rmtree('build')
        if os.path.isdir(packagename + '.egg-info'): shutil.rmtree(packagename + '.egg-info')


def _package_name(packagename, verbose=3):
    # Infer name of the package by excluding all known-required-files-and-folders.
    if packagename is None:
        if verbose>=4: print('[release] Infer name of the package from the directory..')
        # List all folders in dir
        filesindir = np.array(os.listdir())
        getdirs = filesindir[list(map(lambda x: os.path.isdir(x), filesindir))]
        # Remove all the known not relevant files and dirs
        exclude = np.array(['depricated','__pycache__','_version','.git','.gitignore','build','dist','docs'])  # noqa
        Iloc = np.isin(np.array(list(map(str.lower, getdirs))), exclude)==False  # noqa
        if np.any(Iloc):
            packagename = getdirs[Iloc][0]

    if verbose>=4: print('[release] Done! Working on package: [%s]' %(packagename))
    return(packagename)


# %% def main(githubname, packagename=None, verbose=3):
def main(githubname, packagename, makeclean, verbose):
    """Make new release on github and pypi.

    Description
    -----------
    A new release is created by taking the underneath steps:
        1. List all files in current directory and exclude all except the directory-of-interest
        2. Extract the version from the __init__.py file
        3. Remove old build directories such as dist, build and x.egg-info
        4. Git pull
        5. Get latest version from github
        6. Check if the current version is newer then github lates--version.
            a. Make new wheel, build and install package
            b. Set tag to newest version and push to git
            c. Upload to pypi (credentials required)

    Parameters
    ----------
    githubname : str
        Name of the github account.
    packagename : str
        Name of the package.
    makeclean : bool
        Clean local distribution files for packaging.
    verbose : int
        Print message. The default is 3.

    Returns
    -------
    None.

    """
    # Get package name
    packagename = _package_name(packagename, verbose=verbose)
    assert packagename is not None, print('[release] ERROR: Package directory does not exists.')
    # Get init file from the dir of interest
    initfile = os.path.join(packagename, "__init__.py")

    if verbose>=3:
        print('[release] Package: %s' %packagename)
        print('[release] init file: %s' %initfile)

    # Find version now
    if os.path.isfile(initfile):
        if verbose>=3: input("[release] Press Enter to get version from init file and github..")
        # Extract version from __init__.py
        getversion = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", open(initfile, "rt").read(), re.M)
        if getversion:
            # Version found, lets move on:
            current_version = getversion.group(1)
            # Remove build directories
            _make_clean(packagename, clean=makeclean, verbose=verbose)
            if verbose>=3: print('[release] Current local version from __init__.py: %s' %(current_version))
            # Get latest version of github release
            githubversion = github_version(githubname, packagename, verbose=verbose)

            # Continue with the process of building a new version if the current version is newer then the one on github.
            VERSION_OK = version.parse(current_version)>version.parse(githubversion)
            if VERSION_OK:
                if verbose>=3: input("Press Enter to make build and tag on github...")
                # Make build and install
                _make_build_and_install(packagename, current_version)
                # Set tag to github and push
                _github_set_tag_and_push(current_version, verbose=verbose)
                # Upload to pypi
                if verbose>=3: input("Press Enter to upload to pypi...")
                print('Upload to pypi..')
                os.system(TWINE_PATH)
            else:
                if githubversion != '9.9.9':
                    print('[release] WARNING: Not released! You need to increase your version: [%s]' %(initfile))

        else:
            print("[release] ERROR: Unable to find version string in %s. Make sure that the operators are space seperated eg.: __version__ = '0.1.0'" % (initfile,))
    else:
        print('[release] __init__.py File not found: %s' %(initfile))


# %% Main function
if __name__ == '__main__':
    # main
    parser = argparse.ArgumentParser()
    parser.add_argument("github", type=str, help="github account name")
    parser.add_argument("-p", "--package", type=str, help="Package name your want to release.")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3, 4, 5], help="Output verbosity, higher number tends to more information.")
    parser.add_argument("-c", "--clean", type=int, choices=[0, 1], help="Remove local builds: [dist], [build] and [x.egg-info] before creating new ones.")
    args = parser.parse_args()

    # Default verbosity value is 0
    if args.verbosity is None:
        args.verbosity=3
    if args.clean is None or args.clean==1:
        args.clean=True
    else:
        args.clean=False

    # Clean screen
    if args.verbosity>=3:
        os.system('cls')
        print('[release] github    : %s' %args.github)
        print('[release] Cleaning  : %s' %args.clean)
        print('[release] Package   : %s' %args.package)
        print('[release] Verbosity : %s' %args.verbosity)

    main(args.github, args.package, args.clean, args.verbosity)
