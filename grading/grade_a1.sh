#!/bin/bash
USAGE="A cute little grading script for Assignment 1.\n\
Call the script like, \n\n\
$ bash $0 <your url>\n\n\
If the output is '<netid> Success', then you are good!\n"

if [ $# -lt 1 ]; then
    echo -e $USAGE
    exit 1
fi

url=$1

if curl --silent --fail -r 0-10 "$url"; then
    echo "   Success";
else
    echo "Could not reach: $url";
fi

