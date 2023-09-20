#!/usr/bin/bash

set -eu

b="$(ps -a | grep bootnode | pgrep bootnode)"
n1="$(ps -a | grep geth | pgrep geth)"

kill $b
kill $n1
