from web3.geth import GethMiner

from web3 import Web3
import json

config = json.load(open("../../config.json"))


w3 = Web3(Web3.HTTPProvider(f'http://{config["node1"]["ip"]}:{config["node1"]["port"]}'))
w3.eth.default_account = w3.eth.accounts[0]
if not w3.isConnected():
    exit()
print(w3.eth.accounts)
miner = GethMiner(w3)

miner.start(1)