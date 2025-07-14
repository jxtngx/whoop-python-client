# Initial Context

you are an expert python engineer writing a python client for the REST API found in [openapi-spec.json](.knowledge/openapi-spec.json).

this document describes hard [PROJECT REQUIREMENTS](#project-requirements) and simple [DEVELOPMENT INSTRUCTIONS](#development-instructions).

read the document carefully and create a plan to implement the client based on the [PROJECT REQUIREMENTS](#project-requirements) and [DEVELOPMENT INSTRUCTIONS](#development-instructions). before starting, share the plan in a document titled PLAN.md in the [.knowledge](.knowledge) directory. update the plan as you implement the plan.


# PROJECT REQUIREMENTS
you shall use [pydantic](https://docs.pydantic.dev/latest/) to generate models for the client requests and responses.
you shall use [httpx](https://www.python-httpx.org/) to write the client.
you shall use type hints and write google format docstrings for each model and method.
you shall use [mkdocstrings](https://mkdocstrings.github.io/) compatible markdown for documentation.
you shall use [mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/) to generate the documentation.

# DEVELOPMENT INSTRUCTIONS
first read the [api reference](https://www.python-httpx.org/api/), then, for each endpoint in the OpenAPI spec:

- generate pydantic models in [src/whoop_client/models/](src/whoop_client/models/) based on the expected request and response bodies
- generate a client in [src/whoop_client/client.py](src/whoop_client/client.py) that uses the models
- generate a test in [tests/](tests/) without stopping to test. proceed with the next instruction
- document the client method in [docs/endpoints/](docs/endpoints/) using mkdocstrings compatible markdown

when finished, do the following:

- write a getting started guide in docs/getting-started.md and include any relevant information about usage, limitations, or future improvements.
- generate the documentation using mkdocs-material and ensure it is well-structured and easy to navigate.
- copy the contents of this file to [.knowledge/CLAUDE.initial.md](.knowledge/CLAUDE.initial.md) and then update the contents of this file to reflect the current state of the project.
# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.