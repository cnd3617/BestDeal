#!/bin/bash

PYTHON_MAJOR=3
PYTHON_MINOR=8
PYTHON_MICRO=2

docker build -f dockerfile.cpython \
       -t bestdeal/cpython:$PYTHON_MAJOR.$PYTHON_MINOR.$PYTHON_MICRO \
       --build-arg PYTHON_MAJOR=$PYTHON_MAJOR \
       --build-arg PYTHON_MINOR=$PYTHON_MINOR \
       --build-arg PYTHON_MICRO=$PYTHON_MICRO \
       .
