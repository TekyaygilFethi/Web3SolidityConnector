from itertools import chain
from ContractOps import ContractOps
import global_variables
import os
from dotenv import load_dotenv
import sys

load_dotenv()
private_key = os.getenv("PRIVATE_KEY")

with open(f"{global_variables.GLOBAL_COMPILATION_PATH}/compiled_abi.json", "r") as file:
    abi = file.read()

contract_address = sys.argv[1]

contractOps = ContractOps(
    "RINKEBY_RPC_URL",
    my_address=os.getenv("MY_ADDRESS"),
    abi=abi,
    chain_id=int(os.getenv("CHAIN_ID")),
)

contract = contractOps.getContract(contract_address)

# write functions with their parameters if any after this line inside of executeContractFunction method.
contractOps.executeContractFunction(
    # write your contract functions as contract.functions.{your function}, your private key
    contract.functions.addHero("Obi-Wan Kenobi", "Blue", 29),
    private_key,
)

# If you are about to call a function that only returns a data (view function in Solidity) then you should add .call() at the end
print(contract.functions.getInfoByName("Obi-Wan Kenobi").call())

contractOps.executeContractFunction(
    contract.functions.addHero("Anakin Skywalker", "Blue", 19),
    private_key,
)
contractOps.executeContractFunction(
    contract.functions.addHero("Darth Maul", "Red", 32),
    private_key,
)
contractOps.executeContractFunction(
    contract.functions.addHero("Count Dooku", "Red", 80),
    private_key,
)
print(contract.functions.getAllHeroes().call())
