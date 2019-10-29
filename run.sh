#!/bin/bash

python anchor.py > /dev/null 2>&1 &
python tag.py > /dev/null 2>&1 &
python map.py > /dev/null 2>&1 &
