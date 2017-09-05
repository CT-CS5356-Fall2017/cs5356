#!/bin/bash
USAGE="A cute little grading script for Assignment 1.\n\
Call the script like, \n\n\
$ bash $0 <netid>\n\n\
If the output is '<netid> Success', then you are good!\n"
set -e
if [ $# -lt 1 ]; then
    echo -e $USAGE
    exit -1
fi

giturl='https://raw.githubusercontent.com/CT-CS5356-Fall2017/cs5356/master/README.md'
function get_url() {
    # curl --silent $giturl | grep "$1" | awk -F' - ' '{print $2, $3}' |  sed 's/\(\w*\)*\s\+\[.*\](\(.*\))/\1 \2/g'
    curl --silent $giturl | grep "$1" | awk -F' - ' '{print $2, $3}' |  perl -pe 's/(\w+) \[.*\]\((.*)\)/\1 \2/g'
}

r=$(get_url $1)
netid=$(echo $r | cut -d' ' -f1)
url=$(echo $r | cut -d' ' -f2)
echo "URL found form GitHub: $url"


function connection_check() {
    url=$1
    if curl --silent --fail -r 0-10 "$url"; then
        echo "Connection Succeeded" >&2
    else
        echo "Could not reach: $url" >&2
        exit -1
    fi
}


ret=$(connection_check $url)
if [ "$ret" == "$netid" ]; then
    echo "Congrats! Everything works fine."
else
    echo "The netid in the server ($ret) and in the github ($netid) does not match"
fi
set +e