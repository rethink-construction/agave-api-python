# agave-api-python

Python client for the Agave API.

## Installation

To install the Agave API Python client, run the following command:

```bash
pip install git+https://github.com/rethink-construction/agave-api-python.git
```

## Usage

Creating a client
```
from agave_api import AgaveClient

agave = AgaveClient(client_id, client_secret)
```

Getting projects
```
projects = agave.project_management.projects(account_token=account_token)
```

Getting a single project
```
project = agave.project_management.project(project_id, account_token=account_token)
```

> Documentation is a work in progress