# 4. Handle GIS Data Processing via Task Queue

Date: 2024-01-23

## Status

Accepted

## Context

In order to complete relatively compute-heavy and time-consuming GIS data analysis
tasks, without affecting the user's expereince, we will need to use a task queue
to manage these sorts of tasks.

## Decision

We will use Celery as the task queue for this project.

## Consequences

- **Architecture**: Use of Celery will be limited to the `infrastructure`
  directory.
