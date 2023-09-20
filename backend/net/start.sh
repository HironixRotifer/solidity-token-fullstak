#!/usr/bin/bash

bashtrap() {
    echo "CTRL+C Detected !...executing bash trap !"
    exit
    clear;
}

echo "Clear logs..."
rm ./bnode.log
rm ./node1.log
rm ./node2.log

set -eu
clear;

echo "Startig bootnode..."
sleep 0.5;
echo "$(python3 bnode.py > ./bnode.log 2>&1 &)"



echo "Startig node1..."
sleep 3.5;
echo "$(python3 node2.py > ./node2.log 2>&1 &)"

echo "Startig node2..."
sleep 3.5;
echo "$(python3 ./node1.py > ./node1.log 2>&1 &)"
