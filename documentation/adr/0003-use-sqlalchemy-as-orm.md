# 3. Use SQLAlchemy as ORM

Date: 2023-12-13

## Status

Accepted

## Context

In order to persist and retrieve data to and from disk without reinventing the
wheel, we will need to use a tool that abstracts persistence functionality.

## Decision

We will use SQLAlchemy as the Object Relational Mapper (ORM) for this project.

## Consequences

- **Architecture**: Use of SQLAlchemy will be limited to the `infrastructure`
  directory.
