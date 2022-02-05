from web3 import Web3
import os
from solcx import compile_standard, install_solc
import json
from functools import wraps
import global_variables

install_solc("0.6.0")


class ContractOps:
    def __init__(self, provider_key, my_address=None, abi=None, chain_id=None):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv(provider_key)))
        self.nonce = 0
        self.my_address = my_address
        self.abi = abi
        self.chain_id = chain_id

    def compile(self, file_path, isJsonDump=False):
        with open(file_path, "r") as file:
            file_contents = file.read()
        source_file_name = os.path.basename(file_path)

        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {source_file_name: {"content": file_contents}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": [
                                "abi",
                                "metadata",
                                "evm.bytecode",
                                "evm.bytecode.sourceMap",
                            ]
                        }
                    }
                },
            },
            solc_version="0.6.0",
        )

        # get bytecode
        bytecode = compiled_sol["contracts"][source_file_name][source_file_name[:-4]][
            "evm"
        ]["bytecode"]["object"]

        # get abi
        abi = json.loads(  # source_file_name[:-4] = contract name
            compiled_sol["contracts"][source_file_name][source_file_name[:-4]][
                "metadata"
            ]
        )["output"]["abi"]

        if isJsonDump:
            with open(
                f"{global_variables.GLOBAL_COMPILATION_PATH}/compiled_code.json", "w"
            ) as file:
                json.dump(compiled_sol, file)

            with open(
                f"{global_variables.GLOBAL_COMPILATION_PATH}/compiled_abi.json",
                "w",
            ) as file:
                json.dump(abi, file)

            with open(
                f"{global_variables.GLOBAL_COMPILATION_PATH}/compiled_bytecode.txt",
                "w",
            ) as file:
                # json.dump(bytecode, file)
                file.write(bytecode)

    def executeContractFunction(self, contract_function, private_key):
        function_txn = self._createTxn(contract_function=contract_function)

        signed_function_txn = self._signTransaction(function_txn, private_key)

        signed_function_txn_hash_receipt = self._sendRawTransaction(signed_function_txn)

        print("Function executed successfully!")
        return signed_function_txn_hash_receipt

    def callContractFunction(self, contract_function):
        return contract_function.call()

    def getContract(self, contract_address):
        # working with deployed contract
        return self._createTxn(
            contract_address=contract_address,
        )

    def createContract(self, bytecode, private_key):
        contract_object = self._createContractObject(bytecode)

        contract_create_txn = self._createTxn(
            contract=contract_object,
        )

        signed_contract_create_txn = self._signTransaction(
            contract_create_txn, private_key
        )

        signed_contract_create_txn_hash_receipt = self._sendRawTransaction(
            signed_contract_create_txn
        )

        return signed_contract_create_txn_hash_receipt

    def _createContractObject(self, bytecode):
        return self.w3.eth.contract(abi=self.abi, bytecode=bytecode)

    def _incrementNonce(self):
        self.nonce += 1

    def _createTxn(
        self,
        contract=None,
        to_address=None,
        gas_price=None,
        contract_address=None,
        contract_function=None,
    ):
        if contract_address is None:
            self.nonce = self.w3.eth.get_transaction_count(self.my_address)

            build_transaction_parameters = {
                "chainId": self.chain_id,
                "nonce": self.nonce,
                "from": self.my_address,
                "gasPrice": self.w3.eth.gas_price,
            }

            if to_address is not None:
                build_transaction_parameters["to"] = to_address

            if gas_price is not None:
                build_transaction_parameters["gasPrice"] = gas_price

            if contract_function is not None:  # call a function inside a contract
                return self._buildTransactionFunction(
                    contract_function, build_transaction_parameters
                )

            return self._buildCreateContract(contract, build_transaction_parameters)

        else:
            return self.w3.eth.contract(address=contract_address, abi=self.abi)

    # create a new contract
    def _buildCreateContract(self, contract, build_transaction_parameters):
        return contract.constructor().buildTransaction(build_transaction_parameters)

    # call a state changer function
    def _buildTransactionFunction(
        self, contract_function, build_transaction_parameters
    ):
        return contract_function.buildTransaction(build_transaction_parameters)

    def _signTransaction(self, txn, private_key):
        return self.w3.eth.account.sign_transaction(txn, private_key)

    def _sendRawTransaction(self, signed_txn):
        sent_txn = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(sent_txn)
        self._incrementNonce()
        return receipt
