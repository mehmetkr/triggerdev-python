# triggerdev

[![CI](https://github.com/mehmetkr/triggerdev-python/actions/workflows/ci.yml/badge.svg)](https://github.com/mehmetkr/triggerdev-python/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/mehmetkr/triggerdev-python/blob/main/LICENSE)

The first fully typed Python SDK for the [Trigger.dev](https://trigger.dev) management API. Built with Pydantic models generated from the OpenAPI spec, covering 22 Tier 1 endpoints across tasks, runs, and schedules.

> **Status:** Under active development. Not yet published to PyPI.

## Installation

Requires Python 3.10 or later.

The package is not yet on PyPI. Install directly from GitHub:

```sh
uv add git+https://github.com/mehmetkr/triggerdev-python.git
```

Or with pip:

```sh
pip install git+https://github.com/mehmetkr/triggerdev-python.git
```

## Getting started

Set your Trigger.dev secret key as an environment variable:

```sh
export TRIGGER_SECRET_KEY="tr_dev_sk_..."
```

Then trigger your first task:

```python
from triggerdev import Client

with Client() as client:
    result = client.tasks.trigger("my-task", payload={"user_id": 42})
    print(result.id)
```

You can also pass the API key explicitly:

```python
client = Client(api_key="tr_dev_sk_...")
```

## Features

### Trigger tasks

```python
from triggerdev import Client

with Client() as client:
    # Trigger a single task
    result = client.tasks.trigger("send-welcome-email", payload={"user_id": 42})

    # Batch trigger the same task with multiple payloads
    result = client.tasks.batch_trigger("send-welcome-email", items=[
        {"payload": {"user_id": 1}},
        {"payload": {"user_id": 2}},
    ])
```

### List and filter runs

```python
from triggerdev import Client

with Client() as client:
    # List runs with status filter
    runs = client.runs.list(status=["QUEUED", "EXECUTING"])
    for run in runs.data:
        print(f"{run.id}: {run.status}")

    # Retrieve a specific run
    run = client.runs.retrieve("run_1234")
    print(run.task_identifier)
```

### Manage schedules

```python
from triggerdev import Client

with Client() as client:
    # Create a recurring schedule
    schedule = client.schedules.create(
        task="daily-report",
        cron="0 9 * * *",
        deduplication_key="daily-report-prod",
        timezone="America/New_York",
    )
    print(schedule.id)

    # List all schedules
    schedules = client.schedules.list()
    for s in schedules.data:
        print(f"{s.task}: {s.generator.expression}")
```

### Error handling

Every API error maps to a typed exception:

```python
from triggerdev import Client, AuthenticationError, NotFoundError, RateLimitError

with Client() as client:
    try:
        run = client.runs.retrieve("run_nonexistent")
    except NotFoundError as e:
        print(f"Not found: {e}")
    except AuthenticationError:
        print("Invalid API key")
    except RateLimitError:
        print("Rate limited, retry later")
```

## Requirements

- Python 3.10+
- [httpx](https://www.python-httpx.org/) (installed automatically)
- [pydantic](https://docs.pydantic.dev/) v2 (installed automatically)

## Contributing

Contributions are welcome. A contributing guide will be added before the first release.

## License

[MIT](LICENSE)
