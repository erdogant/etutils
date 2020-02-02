"""Make new release on github and pypi."""

import os
import re
import platform
import argparse
import numpy as np
import urllib.request
import shutil
from packaging import version
# import yaml
# yaml.warnings({'YAMLLoadWarning': False})


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
        x.x.x. : Version number of the latest github package.
        0.0.0  : When repo has no tag/release yet.
        9.9.9  : When repo is private or package/user does not exists.

    """
    # Pull latest from github
    print('[release] git pull')
    os.system('git pull')
    github_version = '9.9.9'

    # Check whether username/repo exists and not private
    try:
        github_page = None
        github_url = 'https://api.github.com/repos/' + githubname + '/' + packagename + '/releases'
        github_page = str(urllib.request.urlopen(github_url).read())
        tag_name = re.search('"tag_name"', github_page)
    except:
        if verbose>=1: print('[release] ERROR: github %s does not exists or is private.' %(github_url))
        return github_version

    # Continue and check whether this is the very first tag/release or a multitude are readily there.
    if tag_name is None:
        if verbose>=4: print('[release.debug] github exists but tags and releases are empty [%s]' %(github_url))
        # Tag with 0.0.0 to indicate that this is a very first tag
        github_version = '0.0.0'
    else:
        # exists
        try:
            # Get the latest release
            github_url = 'https://api.github.com/repos/' + githubname + '/' + packagename + '/releases/latest'
            github_page = str(urllib.request.urlopen(github_url).read())
            tag_name = re.search('"tag_name"', github_page)
            # Find the next tag by the seperation of the comma. Do +20 or so to make sure a very very long version would also be included.
            # github_version = yaml.load(github_page)['tag_name']
            tag_ver = github_page[tag_name.end() + 1:(tag_name.end() + 20)]
            get_next_comma = re.search(',',tag_ver)
            github_version = tag_ver[:get_next_comma.start()].replace('"','')
        except:
            if verbose>=1: print('[release] ERROR: Can not find the latest github version!\nPrivate repo? or doest not exists? or there is no release yet?: [https://github.com//%s/%s]' %(githubname, packagename))
            github_version = '9.9.9'

    if verbose>=4: print('[release] Github version: %s' %(github_version))
    if verbose>=4: print('[release] Github version requested from: %s' %(github_url))
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


def _make_clean(packagename, verbose=3):
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
def main(githubname, packagename, makeclean=False, twine=None, verbose=3):
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
    twine : str
        Filepath to the executable of twine.
    verbose : int
        Print message. The default is 3.

    Returns
    -------
    None.


    References
    ----------
    * https://dzone.com/articles/executable-package-pip-install
    * https://blog.ionelmc.ro/presentations/packaging/#slide:8

    """

    # Get package name
    packagename = _package_name(packagename, verbose=verbose)
    assert packagename is not None, print('[release] ERROR: Package directory does not exists.')
    # Get init file from the dir of interest
    initfile = os.path.join(packagename, "__init__.py")

    if verbose>=3:
        os.system('cls')
        print('[release] github    : %s' %githubname)
        print('[release] Package   : %s' %packagename)
        print('[release] Cleaning  : %s' %makeclean)
        print('[release] Verbosity : %s' %verbose)
        print('[release] init file : %s' %initfile)

    # Find version
    if os.path.isfile(initfile):
        # Extract version from __init__.py
        getversion = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", open(initfile, "rt").read(), re.M)
        if getversion:
            # Remove build directories
            if verbose>=3 and makeclean:
                input("[release] Press Enter to clean previous local builds from the package directory..")
                _make_clean(packagename, verbose=verbose)
            # Version found, lets move on:
            current_version = getversion.group(1)
            # Get latest version of github release
            githubversion = github_version(githubname, packagename, verbose=verbose)
            if verbose>=3: print('[release] Current local version from __init__.py: %s and from github: %s' %(current_version, githubversion))

            # Continue with the process of building a new version if the current version is newer then the one on github.
            if githubversion=='0.0.0':
                if verbose>=3: print("[release] Very first release for [%s]" %(packagename))
                VERSION_OK = True
            elif githubversion=='9.9.9':
                if verbose>=3: print("[release] %s/%s not available for [%s]" %(githubname, packagename))
                VERSION_OK = False
            elif version.parse(current_version)>version.parse(githubversion):
                VERSION_OK = True
            else:
                VERSION_OK = False

            # Continue is version is TRUE
            if VERSION_OK:
                if verbose>=3: input("Press Enter to make build and release [%s] on github..." %(current_version))
                # Make build and install
                _make_build_and_install(packagename, current_version)
                # Set tag to github and push
                _github_set_tag_and_push(current_version, verbose=verbose)
                # Upload to pypi
                if os.path.isfile(twine):
                    if verbose>=3: input("Press Enter to upload to pypi...")
                    os.system(twine + ' upload dist/*')

                if verbose>=2: print('[release] ALL RIGHT! Everything is succesfully done!\nBut you still need to do one more thing.\nGo to your github most recent releases (this one) and [edit tag] > the set the version nubmer in the [Release title].')

            else:
                if githubversion != '9.9.9':
                    print('[release] WARNING: Not released! You need to increase your version or make an active repo: [%s]' %(initfile))

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
    parser.add_argument("-c", "--clean", type=int, choices=[0, 1], help="Remove local builds: [dist], [build] and [x.egg-info] before creating new ones.")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3, 4, 5], help="Output verbosity, higher number tends to more information.")
    parser.add_argument("-t", "--twine", type=str, help="Path to twine that is used to upload to pypi.")
    args = parser.parse_args()

    # Default verbosity value is 0
    if args.verbosity is None:
        args.verbosity=3
    if args.clean is None or args.clean==1:
        args.clean=True
    else:
        args.clean=False
    if args.twine is None:
        args.twine = ''
        if platform.system().lower()=='windows':
            args.twine = os.environ['TWIN.EXE']
            # TWINE_PATH = 'C://Users/<USER>/AppData/Roaming/Python/Python36/Scripts/twine.exe'

    main(args.github, args.package, makeclean=args.clean, twine=args.twine, verbose=args.verbosity)
