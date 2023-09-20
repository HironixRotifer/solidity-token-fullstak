from web3 import Web3
from web3.geth import GethMiner
import json

config = json.load(open("./config.json"))


w3 = Web3(Web3.HTTPProvider(f'http://{config["node1"]["ip"]}:{config["node1"]["port"]}'))

w3.eth.default_account = w3.eth.accounts[0]
print("Owner: " + w3.eth.default_account)

miner = GethMiner(w3)
miner.set_etherbase(w3.eth.accounts[0])
miner.start(1)

hello_contract = w3.eth.contract(abi=config["contract"]["abi"], bytecode=config["contract"]["bytecode"])

w3.geth.personal.unlock_account(w3.eth.default_account, "123")

hello_hash = hello_contract.constructor().transact()

hello_receipt = w3.eth.wait_for_transaction_receipt(hello_hash, 300)

config["contract"]["address"] = hello_receipt.contractAddress

json.dump(config, open('./config.json', 'w'), indent=4) 

print(hello_receipt.contractAddress)
print("Contract deployd!")