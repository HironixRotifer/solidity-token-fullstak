import json
import os

config = json.load(open("./config.json"))

os.system(f'geth --datadir backend/net/node2/ --networkid 999 --syncmode "full" --allow-insecure-unlock --ipcdisable --http --http.addr "{config["node2"]["ip"]}" --authrpc.port "{config["node2"]["port"]}" --http.corsdomain "*" --bootnodes "{config["bootnode"]["enode"]}{config["bootnode"]["ip"]}:{config["bootnode"]["bootport"]}" --port "{config["node2"]["bootport"]}" --http.api web3,eth,net,personal,miner')







