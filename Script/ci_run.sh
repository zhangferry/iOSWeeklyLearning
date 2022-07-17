#!/bin/bash

path=$(cd $(dirname $0); pwd)
deploy="${path}/deploy.py"
python3 ${deploy}
