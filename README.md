# template2instance

## Description
The `template2instance` is a tool to generate a new project instance from a template.

## Installation
First install poetry (see [poetry documentation](https://python-poetry.org/docs/)):
``` bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then install the package:
``` bash
poetry install
```

## Usage

The most simple way to use the tool is to run the following command:
``` bash
poetry run create template_folder new_package_name
```
It should ask questions and generate a new project instance at the 
path ``new_package_name``.
Automatically, it will save the answers in a file called 
`pkg_generation_config.json` in the generated project instance.


If you want to reuse some answers, you can use the following command:
``` bash
poetry run create template_folder new_package_name --config pkg_generation_config.json
```
Any variable that would have triggered a question and that has a value in the
`pkg_generation_config.json` file will be used directly and will not trigger a question.

## Features
 - [ ] Automatically it will create a new git repository and commit the changes.

## Roadmap
 1. Automatically it will create a new git repository and commit the changes.