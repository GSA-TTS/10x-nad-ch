#!/bin/bash

# Append to the existing PYTHONPATH, preserving the buildpack's modifications
# Followed the suggestion here: https://github.com/cloudfoundry/python-buildpack/issues/140#issuecomment-520449355
export PYTHONPATH=/home/vcap/app
