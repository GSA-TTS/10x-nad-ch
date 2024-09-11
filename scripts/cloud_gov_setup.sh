#!/bin/bash

set -e

# Variables for creating the service
SERVICE_TO_CREATE="cloud-gov-identity-provider"
SERVICE_PLAN="oauth-client"
SERVICE_NAME=""
KEY_NAME=""

TARGET_SPACE="sandbox-gsa"

# Check if the current active space is the target space
# The 'cf target' command provides information about the current target space
CURRENT_SPACE=$(cf target | grep "space:" | awk '{print $2}')

# If the current space is not the target space, switch to the target space
if [ "$CURRENT_SPACE" != "$TARGET_SPACE" ]; then
  echo "Targeting space: $TARGET_SPACE"
  cf target -s $TARGET_SPACE
else
  echo "Already in space: $TARGET_SPACE"
fi

# Create a service:
# cf create-service SERVICE PLAN SERVICE_INSTANCE [-b BROKER] [-c PARAMETERS_AS_JSON] [-t TAGS]
# See https://cli.cloudfoundry.org/en-US/v7/create-service.html
cf create-service $SERVICE_TO_CREATE $SERVICE_PLAN $SERVICE_NAME

# Create a service key:
# cf create-service-key SERVICE_INSTANCE SERVICE_KEY [-c PARAMETERS_AS_JSON]
# See https://cli.cloudfoundry.org/en-US/v7/create-service-key.html
cf create-service-key $SERVICE_NAME $KEY_NAME \
-c '{
  "redirect_uri": [
    "http://localhost:8080/auth/authorize/cloudgov",
    "http://localhost:8080/auth/callback/cloudgov",
    "http://localhost:8080/auth/logout/cloudgov"
  ]
}'

# Bind key to service
cf service-key $SERVICE_NAME $KEY_NAME
