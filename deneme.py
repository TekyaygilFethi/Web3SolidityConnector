from web3 import Web3
import json
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

from ContractOps import ContractOps

load_dotenv()

with open("./SimpleContract.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing")
install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

contractOps = ContractOps("RINKEBY_RPC_URL")

chain_id = 1337
my_address = "0x1E105B337D22Dfdc2C23F97cD67Ff3E2530056D2"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = contractOps.CreateContract(abi, bytecode)

contract_create_txn = contractOps.createTxn(
    SimpleStorage, chain_id, my_address)

signed_contract_create_txn = w3.eth.account.sign_transaction(
    contract_create_txn, private_key)

signed_contract_create_txn_hash = w3.eth.send_raw_transaction(
    signed_contract_create_txn.rawTransaction)

signed_contract_create_txn_hash_receipt = w3.eth.wait_for_transaction_receipt(
    signed_contract_create_txn_hash)


# working with deployed contract
simple_storage_contract = w3.eth.contract(
    address=signed_contract_create_txn_hash_receipt.contractAddress, abi=abi)

nonce += 1

simple_storage_txn = simple_storage_contract.functions.addHero("Obi-Wan Kenobi", "Blue", 29).buildTransaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "nonce": nonce,
    "from": my_address
})

signed_simple_storage_txn = w3.eth.account.sign_transaction(
    simple_storage_txn, private_key)

signed_simple_storage_txn_hash = w3.eth.send_raw_transaction(
    signed_simple_storage_txn.rawTransaction)

signed_simple_storage_txn_hash_receipt = w3.eth.wait_for_transaction_receipt(
    signed_simple_storage_txn_hash)

print(simple_storage_contract.functions.getInfoByName("Obi-Wan Kenobi").call())


nonce += 1
simple_storage_txn = simple_storage_contract.functions.addHero("Anakin Skywalker", "Green", 19).buildTransaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "nonce": nonce,
    "from": my_address
})

signed_simple_storage_txn = w3.eth.account.sign_transaction(
    simple_storage_txn, private_key)

signed_simple_storage_txn_hash = w3.eth.send_raw_transaction(
    signed_simple_storage_txn.rawTransaction)

signed_simple_storage_txn_hash_receipt = w3.eth.wait_for_transaction_receipt(
    signed_simple_storage_txn_hash)

print(simple_storage_contract.functions.getInfoByName("Anakin Skywalker").call())
