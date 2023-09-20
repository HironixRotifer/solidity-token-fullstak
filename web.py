from web3 import Web3
import json

config = json.load(open("./config.json"))
w3 = Web3(Web3.HTTPProvider(f'http://{config["node1"]["ip"]}:{config["node1"]["port"]}'))
contract = w3.eth.contract(address=config["contract"]["address"], abi=config["contract"]["abi"])

# проверка на подключение
if w3.isConnected():
    print("connecteon")
else:
    print("disconnecnt")

print(contract.all_functions())


# разблакировка аккаунта и ключа
def unlock(acc, key):
    account = w3.toChecksumAddress(acc)
    w3.eth.default_account = account
    w3.geth.personal.unlock_account(acc, key, 10)

def addOneMinuteToTimeDiff(acc, key):
    try:
        unlock(acc, key)
        res = contract.functions.addOneMinuteToTimeDiff().transact()
        return res
    except Exception as e:
        return str(e)

def Time_start():
    try:
        res = contract.functions.Time_start().call()
        return res
    except Exception as e:
        return str(e)

def ReturnFaze():
    try:
        res = contract.functions.ReturnFaze().call()
        return res
    except Exception as e:
        return str(e)

# функция регистрации пользователя
def Registration(acc, key, name, password):
    try:
        unlock(acc, key)
        res = contract.functions.Registration(name, password).transact()
        return res
    except Exception as e:
        return str(e)

# функция регистрации пользователя
def Authorization(acc, key, name, password):
    try:
        w3.eth.default_account = w3.toChecksumAddress(acc)
        print(key)
        res = contract.functions.Authorization(name, password).call()
        return res
    except Exception as e:
        return str(e)

def ReturnUserInfo():
    try:
        res = contract.functions.ReturnUserInfo().call()
        return res
    except Exception as e:
        return str(e)
    
def returnPublicTokenBalance():
    try:
        res = contract.functions.returnPublicTokenBalance().call()
        return res
    except Exception as e:
        return str(e)

def returnPrivateTokenBalance():
    try:
        res = contract.functions.returnPrivateTokenBalance().call()
        return res
    except Exception as e:
        return str(e)
    
def returnSeedTokenBalance():
    try:
        res = contract.functions.returnSeedTokenBalance().call()
        return res
    except Exception as e:
        return str(e)

def returnBalanceEther():
    try:
        res = contract.functions.returnBalanceEther().call()
        return res
    except Exception as e:
        return str(e)

def PricePublicToken():
    try:
        res = contract.functions.PricePublicToken().call()
        return res
    except Exception as e:
        return str(e)

def BuyPublicToken(amount, acc, key):
    try:
        unlock(acc, key)
        price = PricePublicToken()
        w3.eth.send_transaction({
            'to': w3.eth.coinbase,
            'from': acc,
            'value': int(amount) * int(price)
        })
        res = contract.functions.BuyPublicToken(int(amount)).transact()
        print(res)
        return res
    except Exception as e:
        return str(e)
    
def BuyPrivateToken(amount, acc, key):
    try:
        unlock(acc, key)
        w3.eth.send_transaction({
            'to': w3.eth.coinbase,
            'from': acc,
            'value': int(amount)
        })
        res = contract.functions.BuyPrivateToken(int(amount)).transact()
        return res
    except Exception as e:
        return str(e)
    
def TransferPublicTokenOnUser(to, amount, acc, key):
    try:
        unlock(acc, key)
        res = contract.functions.TransferPublicTokenOnUser(to, int(amount)).transact()
        return res
    except Exception as e:
        return str(e)

def TransferPrivateTokenOnUser(to, amount, acc, key):
    try:
        unlock(acc, key)
        res = contract.functions.TransferPrivateTokenOnUser(to, int(amount)).transact()
        return res
    except Exception as e:
        return str(e)
    
def SendPublicTokens(amount, account,acc, key):
    try:
        unlock(acc, key)
        res = contract.functions.SendPublicTokens(int(amount), account).transact()
        return res
    except Exception as e:
        return str(e)
    
def ViewArrayRequests():
    try:
        res = contract.functions.ViewArrayRequests().call()
        return res
    except Exception as e:
        return str(e)  

def AddRequestInArray(acc, key):
    try:
        unlock(acc, key)
        res = contract.functions.AddRequestInArray().transact()
        print(res)
        return res
    except Exception as e:
        return str(e) 

def RemoveRequestInArray(acc, key, index):
    try:
        unlock(acc, key)
        res = contract.functions.RemoveRequestInArray(int(index)).transact()
        return res
    except Exception as e:
        return str(e)   
    
def AccessRequest(acc, key, index):
    try:
        unlock(acc, key)
        res = contract.functions.AccessRequest(int(index)).transact()
        return res
    except Exception as e:
        return str(e)
    
def ChangePriceForPublicTokens(acc, key, newPrice):
    try:
        unlock(acc, key)
        res = contract.functions.ChangePriceForPublicTokens(int(newPrice)).transact()
        return res
    except Exception as e:
        return str(e)
