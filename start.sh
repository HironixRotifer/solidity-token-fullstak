#!/usr/bin/bash

bashtrap() {
    echo "CTRL+C Detected !...executing bash trap !"
    exit
    clear;
}

set -eu
clear;

rm -rf ./backend/net/node1/geth
rm -rf ./backend/net/node2/geth

echo ""
geth --datadir ./backend/net/node2 init backend/net/genesis.json
geth --datadir ./backend/net/node1 init backend/net/genesis.json

clear;

echo "[+] Start EVM Private network"


echo "Startig bootnode..."
sleep 0.5;
echo "$(python3 backend/net/bootnode.py > ./logs/bootnode.log 2>&1 &)"
echo "[+] bootnode is start!"


echo "Startig node1..."
sleep 3.5;
echo "$(python3 backend/net/node2.py > ./logs/node2.log 2>&1 &)"
echo "[+] node1 is start!"


echo "Startig node2..."
sleep 3.5;
echo "$(python3 backend/net/node1.py > ./logs/node1.log 2>&1 &)"
echo "[+] node2 is start!"

sleep 3.5;


echo "Deploy contract..."
echo "$(python3 ./backend/contract/deploy.py)"


sleep 20;

echo "$(python3 ./main.py)"

sleep 1.5;

echo "$(firefox http://127.0.0.1:8080)"
