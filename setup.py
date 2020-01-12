import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     install_requires=['numpy','pandas','tqdm','matplotlib','path'],
     python_requires='>=3',
     name='etutils',  
     version='0.1.0',
#     version=versioneer.get_version(),    # VERSION CONTROL
#     cmdclass=versioneer.get_cmdclass(),  # VERSION CONTROL
     author="Erdogan Taskesen",
     author_email="erdogant@gmail.com",
     description="etutils is Python package with helper functions that are used across various other packages. Installing this package on itself may not be so interesting.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/erdogant/etutils",
	 download_url = 'https://github.com/erdogant/etutils/archive/0.1.0.tar.gz',
     packages=setuptools.find_packages(), # Searches throughout all dirs for files to include
     include_package_data=True, # Must be true to include files depicted in MANIFEST.in
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent",
     ],
 )
