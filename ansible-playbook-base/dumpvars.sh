#!/bin/bash

# Lots of hacky scripting to get a valid JSON here.
# If file does not exist, create the initial JSON tag for host_data
# If file exists then append a comma separator and then dump the passed in
# variable.

# TODO: Find more elegant ways to achieve this!

if [ -e "$1" ]
then
        echo "," >> "./$1"
else
        echo "{\"host_data\": [" > "./$1"
fi

cat $2 >> "./$1"
