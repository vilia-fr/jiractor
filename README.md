# Jiractor is a JIRA extractor

A simple command-line tool to extract the result of a JQL query in 
simple human-readable JSON with history and links.

## Installation

The tool requires a reasonably recent Python 3 installation.

```shell
pip install -r requirements.txt
```

## Usage

Specify your JIRA credentials in the `.env` file. Then execute:

```shell
python jira_extract.py '<JQL>' <output.json>
```

The tool will generate a large `output.json` file with all issues, and 
a bunch of `ISSUE-123.json` files in `issues` folder.

## Known bugs and limitations

1. Jira API returns maximum 1000 issues, so for the large projects you will need 
to split your query like this: `project = MYPROJECT and key >= 'MYPROJECT-2000' and key < 'MYPROJECT-3000'`  


Copyright (C) 2021 Constantine Kulak (ck@vilia.fr)
