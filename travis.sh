#!/usr/bin/env bash
set -e

# Script is necessary because Travis doesn't fail-fast without setting -e for all build steps.

docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
make build
python3 ci-tools/cloud/docker_build.py
