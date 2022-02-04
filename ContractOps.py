from web3 import Web3
import os
from solcx import compile_standard, install_solc
import json
from functools import wraps

install_solc("0.6.0")


class ContractOps:
    def __init__(self, provider_key):
        # "RINKEBY_RPC_URL"
        self.w3 = Web3(Web3.HTTPProvider(os.getenv(provider_key)))
        self.nonce = 0

    def compile(self, file_path, isJsonDump=False):
        with open(file_path, "r") as file:
            file_contents = file.read()

        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"SimpleStorage.sol": {"content": file_contents}},
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
        bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"][
            "evm"
        ]["bytecode"]["object"]

        # get abi
        abi = json.loads(
            compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
        )["output"]["abi"]

        if isJsonDump:
            with open("compiled_code.json", "w") as file:
                json.dump(compiled_sol, file)

        return (abi, bytecode)

    def createContract(self, abi, bytecode):
        return self.w3.eth.contract(abi=abi, bytecode=bytecode)

    def incrementNonce(self):
        self.nonce += 1

    def decrementNonce(self):
        self.nonce -= 1

    def createTxn(
        self,
        from_address=None,
        chain_id=None,
        contract=None,
        to_address=None,
        gas_price=None,
        contract_address=None,
        contract_abi=None,
    ):
        self.nonce = self.w3.eth.get_transaction_count(from_address)
        if contract_address is None:
            return self.buildTransaction(
                chain_id,
                from_address,
                contract,
                to_address,
                gas_price,
            )
        else:
            return self.w3.eth.contract(address=contract_address, abi=contract_abi)

    def buildTransaction(
        self,
        chain_id,
        from_address,
        contract=None,
        to_address=None,
        gas_price=None,
        contract_function=None,
    ):
        build_transaction_parameters = {
            "chainId": chain_id,
            "nonce": self.nonce,
            "from": from_address,
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

    # create a new contract
    def _buildCreateContract(self, contract, build_transaction_parameters):
        return contract.constructor().buildTransaction(build_transaction_parameters)

    # call a state changer function
    def _buildTransactionFunction(
        self, contract_function, build_transaction_parameters
    ):
        return contract_function.buildTransaction(build_transaction_parameters)

    def signTransaction(self, txn, private_key):
        return self.w3.eth.account.sign_transaction(txn, private_key)

    def sendRawTransaction(self, signed_txn):
        sent_txn = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(sent_txn)
        self.incrementNonce()
        return receipt

    def callFunction(self, contract_function):
        return contract_function.call()
