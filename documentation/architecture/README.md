# National Address Database Submission Tool Architecture

### Entry Points

Users can work with the National Address Database Submission Tool by way of:

- **Flask Web Server**: Primary interface for web-based interactions for Data
  Producers and NAD Administrator.
- **CLI**: Command line interface allowing NAD Administrator to perform
  administrative tasks.

### Application Core

Logic concerning business rules, data validation and profiling, and other
application concerns. The core is unaware of how its entry points and its
infrastructure dependencies are implemented.

### Infrastructure Dependencies

The current remote development environment uses [services provided by cloud.gov](https://cloud.gov/docs/services/intro/).

- **Object Storage**: Storage for datasets submitted by users, via
  [S3](https://cloud.gov/docs/services/s3/).
- **Relational Database**: Persistence for application data and data validation
  reports, via [RDS PostgreSQL database](https://cloud.gov/docs/services/relational-database/).
- **Task Queue Broker**: Manages queue of data validation tasks for Celery, via
  [AWS Elasticache Redis](https://cloud.gov/docs/services/aws-elasticache/).

### System diagram

```mermaid
flowchart TB
    %% NAD System Boundary
    subgraph NAD_CH [NAD CH]
        direction TB
        %% Application and AWS Infrastructure
        app[[Python/Flask Server]]

        %% Storage Backends
        postgres[(RDS Postgres)]
        redis{{AWS Redis}}
        s3[/S3 Bucket/]

        %% Connections from Flask Application
        app -.->|Stores provider and submission metadata| postgres
        app -.->|Enqueues tasks| redis
        app -.->|Reads and writes submissions| s3

        %% Job Runner positioned below storage backends
        job_runner[[Job Runner]]
        job_runner -.->|Reads tasks| redis
        job_runner -.->|Reads and writes data| s3
    end

    %% CI/CD System
    cicd[(GitHub or GitLab)]
    cicd -->|Deploys application stack - HTTPS| NAD_CH

    %% External Components and Users
    login[(Login.gov)]
    data_provider{{Data Provider}}
    nad_admin{{NAD Administrator}}

    %% Interactions and Connections
    data_provider -- Uploads Data Extracts - HTTPS --> app
    nad_admin -- Manages Submissions & Providers - HTTPS --> app
    app -->|Authenticates users - HTTPS| login
```
