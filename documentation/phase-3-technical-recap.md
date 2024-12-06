# 10x NAD Submission Tool Technical Recap

## Intent

This document provides a high-level overview of the 10x National Address Database Submission Tool Phase 3 to
help developers joining the team for Phase 4, as well as other stakeholders,
understand the history of the effort.

In addition to providing context, this document summarizes:

- The technical decisions that were made during Phase 3 of 10x National Address Database Submission Tool
  development
- The state of the codebase at the conclusion of Phase 3
- The next steps for Phase 4 in terms of tasks and decision making

## Context

The 10x process involves four phases:

- Phase 1: Investigation
- Phase 2: Discovery
- Phase 3: Develop
- Phase 4: Scale

According to the [10x website](https://10x.gsa.gov/about/what-we-do/):

> Most 10x projects end after Phase 3, when the product
> is handed off to its agency product owner. However, a few select projects
> require more funding and resources so they move on to the next phase of work,
> Phase 4, Scale.

10x National Address Database Submission Tool is one of those cases where additional development effort is
necessary. The codebase is more a proof of concept than a minimum viable
product as there is a good deal of work needed to get the application up and
running for real-world users.

## Technical Decisions

Architectural Decision Records (ADRs) describing technical decisions made during
Phase 3 are stored in this repository (`documentation/adr`).

More broadly speaking, the codebase follows the design guidelines of Robert
Martin's [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
concept: dependencies were intended to be isolated from one another so that
concrete decisions such as which particular database, web UI approach, and
authentication mechanism to use could be deferred while the core functionality
of the application was under development.

Working from the ground up in such a way has the significant downside of
introducing significant architectural complexity into the codebase. It is
possible that the Phase 4 team may conclude that a less loosely coupled design
is necessary to deliver value to users.

## State of the Codebase

Key challenges faced during Phase 3 include managing architectural complexity
and ensuring scalability. Known issues include incomplete integration of certain
dependencies.

### Application Code

The application resides in the `nad_ch` directory. That directory is
structured as follows:

```
nad_ch
├── application
│   ├── use_cases
│   ├── validation_files
│   └── ...
├── config
│   └── ...
├── controllers
│   ├── web
│   └── ...
├── core
│   └── ...
└── infrastructure
    └── ...
```

#### Core

The "core" layer attempts to encapsulate domain-specific concepts and business
logic. Currently, this layer is somewhat ["anemic"](https://martinfowler.com/bliki/AnemicDomainModel.html).
It contains:

- Domain Entities: Represent the primary business entities and their behavior.
- Repositories: Interfaces for data access, to be implemented in the
  infrastructure layer.

#### Application

The "application" layer defines use cases that orchestrate objects from both the
core layer and the infrastructure layer in order to enable user actions. Other
application concerns such as exceptions, validation, and view models are in
this layer as well.

#### Infrastructure

The "infrastructure" layer isolates dependencies such as database,
messaging queue, storage, and external APIs.

- Database: PostgreSQL
- Messaging Queue: Redis
- Storage: AWS S3 (Minio in local)

#### Config

The `ApplicationContext` class for each environment is exported from this
directory. This is where secrets are loaded from environment variables so that
dependencies can be used.

### Supporting Code

The application runs locally using Docker. The `Dockerfile` defines the
operating environment of the application, and `compose.yml` defines the services
needed for the application to run (see the "Infrastructure" section above).

Database migrations are stored in the `alembic` directory.

# Next Steps

## A: Infrastructure

1. Work with stakeholders to confirm infrastructure dependencies (database,
   queue, storage, authentication mechanism). Then, incorporate the secrets
   needed to use these dependencies in the `config` directory and update the
   `ApplicationContext` class and the implementation details in the
   infrastructure layer to integrate these dependencies.

2. Once an authentication mechanism is in place, build out the UI such that
   whatever administrative tasks concerning users that the admin role should
   have can be accomplished in the browser.

## B: Toward End-To-End Functionality

1. Request a nominal dataset from stakeholders that would pass the validation
   rules defined in the application layer. Ensure that the dataset meets the
   necessary criteria before proceeding.

2. Build out the UI so that data submission, validation, and profiled use
   cases can be triggered from the browser, and so that users can monitor the
   progress and view the results in the browser.
