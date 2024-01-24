# 4. Handle GIS Data Processing via Task Queue

Date: 2024-01-23

## Status

Accepted

## Context

In order to complete relatively compute-heavy and time-consuming GIS data analysis
tasks, without affecting the user's expereince, we will need to use a task queue
to manage these sorts of tasks.

## Decision

We will use Celery as the task queue for this project. Celery is open source,
relatively straightforward to configure, and actively maintained. It also
allows tasks to be executed concurrently across multiple workers, which is
good for scaling.

## Consequences

- **Architecture**: Use of Celery will be limited to the `infrastructure`
  directory.
- **Choice of Broker**: In order to leverage our remote development environment's
  services, we will use Redis as a broker, keeping in mind the [caveats](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html#caveats)
  highlighted in Celery's documentation.
