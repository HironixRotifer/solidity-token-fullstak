#!/usr/bin/bash

set -eu

clear;

b="$(ps -a | grep bootnode | pgrep bootnode)"
n1="$(ps -a | grep geth | pgrep geth)"
n2="$(ps -a | grep python3 | pgrep python3)"


kill $n2
kill $b
kill $n1

echo "[+] EVM stoped "
