import json
import os

config = json.load(open("./config.json"))

os.system(f'bootnode -nodekey backend/net/boot.key -addr {config["bootnode"]["ip"]}:{config["bootnode"]["bootport"]} -verbosity 9')

