[![Python application](https://github.com/wwu-mmll/photonai_module_template/actions/workflows/lindandtest.yml/badge.svg)](https://github.com/wwu-mmll/photonai_module_template/actions/workflows/lindandtest.yml)
[![Coverage Status](https://coveralls.io/repos/github/wwu-mmll/photonai_module_template/badge.svg?branch=master)](https://coveralls.io/github/wwu-mmll/photonai_module_template?branch=master)
![GitHub](https://img.shields.io/github/license/wwu-mmll/photonai_module_template)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=wwu-mmll_photonai_module_template&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=wwu-mmll_photonai_module_template)

# How to use this template
This repository is a quick start template for new photonai modules. To get started simply follow these steps:
1. Klick "Use this template" button
2. Fill in details for the new photonai module
3. Wait for the repository to be created
4. Wait for the Github Actions to run once
5. As soon as the "✅ Ready to clone and code." commit appears in your repository you are ready to start coding
6. (optional) Remove "rename_project.yml" workflow from .github/workflows
7. (optional) Remove "rename_project.sh" from .github
8. Remove this how to section from readme

## Included features
- [X] Code testing and coverage calculation (if coveralls secret **COVERALLS_REPO_TOKEN** is set)
- [X] Continous Integration for testing and documentation updates based on Github Actions.
- [X] MkDocs-Material based documentation template
- [X] Photonai compatible **init.py** with boilerplate code for registration of new module
- [X] pbr based auto-versioning for python releases 
- [X] blueprint action for pypi publishing (on github release)

# How to implement a photonai module

Take a look at some of our modules like [photonai neuro](https://github.com/wwu-mmll/photonai_neuro) 
or [photonai graph](https://github.com/wwu-mmll/photonai_graph).
Most importantly: Feel free to reach out via issues in case of problems, e.g. by creating an issue at the [photonai repo](https://github.com/wwu-mmll/photonai)

##  Development workflow: Add new algorithms
In order to add a new Algorithm / Feature to your project you can follow the steps below. By providing unit tests, a documentation and an example you maximize code quality and usability of your module.  
- [ ] Develop your learning algorithm / transformer / utility code (remember to adhere to the scikit-learn object API as [documented here](https://wwu-mmll.github.io/photonai/getting_started/custom_algorithm/))
- [ ] Test your algorithms in a respective test file in the `test` folder 
- [ ] Document algorithms in the `docs` folder by copying and adapting the provided .md file
- [ ] Provide an example on how to use your algorithms in an appropriately named file in the examples folder.
- [ ] Expose the algorithm to photonai by adding it to the the `photonai_conformal/photonai_conformal.json` file with the full path. An example is provided within this repository.  Thereby, the algorithm can be imported via its name, as defined in the json file. Make sure to pick a unique name. 

**In order to access your algorithms and functions in photonai you have to import your module once in your final script. This triggers the registration process in the photonai core module!**

## Release a version of your software (on pypi)
We suggest releasing via the github website. Simply create a release and an according tag.
The tag is then used as version number and (if configured) the desired version is immediately build and released on pypi.

Documentation avaiable at: [Documentation](https://wwu-mmll.github.io/photonai_module_template/)
