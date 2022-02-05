from web3 import Web3
import os
from dotenv import load_dotenv
import global_variables
import sys

from ContractOps import ContractOps

load_dotenv()


sol_path = sys.argv[1]
print(f"{global_variables.GLOBAL_SOL_PATH}/{sol_path}")
contractOps = ContractOps("RINKEBY_RPC_URL")

if os.path.isdir(global_variables.GLOBAL_COMPILATION_PATH) == False:
    os.mkdir(global_variables.GLOBAL_COMPILATION_PATH)
    print("Compilation folder created!")

contractOps.compile(f"{global_variables.GLOBAL_SOL_PATH}/{sol_path}", isJsonDump=True)

print("Compiled successfully!")
