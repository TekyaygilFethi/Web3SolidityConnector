from itertools import chain
from web3 import Web3
import os
from dotenv import load_dotenv
import global_variables
import json

from ContractOps import ContractOps

load_dotenv()

try:
    with open(
        f"{global_variables.GLOBAL_COMPILATION_PATH}/compiled_abi.json", "r"
    ) as file:
        abi = file.read()

    with open(
        f"{global_variables.GLOBAL_COMPILATION_PATH}/compiled_bytecode.txt", "r"
    ) as file:
        bytecode = file.read()

except FileNotFoundError:
    raise FileNotFoundError(
        "You need to compile first! To compile, you need to run: python compile.py"
    )

chain_id = int(os.getenv("CHAIN_ID"))
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

contractOps = ContractOps(
    "RINKEBY_RPC_URL", my_address=my_address, abi=abi, chain_id=chain_id
)

signed_contract_create_txn_hash_receipt = contractOps.createContract(
    bytecode, private_key
)

print("New Contract Transaction has been created!", end="\n\n")
print(signed_contract_create_txn_hash_receipt, end="\n\n")
print(
    f"Contract Address: {signed_contract_create_txn_hash_receipt.contractAddress}",
    end="\n\n",
)
