from web3 import Web3
import json

import os
from dotenv import load_dotenv

from ContractOps import ContractOps

load_dotenv()
contractOps = ContractOps("RINKEBY_RPC_URL")

abi, bytecode = contractOps.compile("./SimpleContract.sol")

chain_id = int(os.getenv("CHAIN_ID"))
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = contractOps.createContract(abi, bytecode)

contract_create_txn = contractOps.createTxn(
    my_address,
    chain_id=chain_id,
    contract=SimpleStorage,
)

signed_contract_create_txn = contractOps.signTransaction(
    contract_create_txn, private_key
)

signed_contract_create_txn_hash_receipt = contractOps.sendRawTransaction(
    signed_contract_create_txn
)

# working with deployed contract

deployed_contract = contractOps.createTxn(
    from_address=my_address,
    contract_address=signed_contract_create_txn_hash_receipt.contractAddress,
    contract_abi=abi,
)

print(deployed_contract.functions.getInfoByName("Obi-Wan Kenobi").call())
"""
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
"""
