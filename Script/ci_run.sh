#!/bin/bash

path=$(cd $(dirname "$0"); pwd)
deploy="${path}/deploy.py"

if [ -n "$1" ]; then
  python3 "${deploy}" --index "$1"
else
  python3 "${deploy}"
fi