# 10x National Address Database Submission Tool (NAD-ST)

## Data Landing Zone

The purpose of the landing zone is to provide a location to store intemediate mapped data that is generated during the validation step and needs to be written to a remote cloud storage such as AWS s3.

NOTE: This folder will likely not be deployed to production environments because it is only needed for local development. Instead a folder should be created outside of the repository and in the file system used by the server hosting the application in production. The path to that folder will be configured within the application so that the app can recognize the location and writes data to the correct path.
