#!/bin/bash

cd /home/wilson/Programovani/ZNS/docs/
if [[ -d "../__venv__" ]]
then
    . ../__venv__/bin/activate
fi

make html
