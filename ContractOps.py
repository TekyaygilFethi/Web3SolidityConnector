from http.client import NON_AUTHORITATIVE_INFORMATION
from web3 import Web3
import os


class ContractOps():
    def __init__(self, provider_key):
        # "RINKEBY_RPC_URL"
        self.w3 = Web3(Web3.HTTPProvider(os.getenv(provider_key)))
        self.nonce = self.w3.eth.get_transaction_count()

    def CreateContract(self, abi, bytecode):
        return self.w3.eth.contract(abi=abi, bytecode=bytecode)

    def IncrementNonce(self):
        self.nonce += 1

    def DecrementNonce(self):
        self.nonce -= 1

    def createTxn(self, contract, chain_id, from_address, to_address=None, gas_price=None, txn_address=None, txn_abi=None):
        build_transaction_parameters = {
            "chain_id": chain_id,
            "nonce": self.nonce,
            "from_address": from_address,
            "gas_price": self.w3.eth.gas_price
        }

        if to_address is not None:
            build_transaction_parameters["to_address"] = to_address

        if gas_price is not None:
            build_transaction_parameters["gas_price"] = gas_price

        try:
            self.IncrementNonce()
            if txn_address == None:
                return contract.constructor.buildTransaction(build_transaction_parameters)
            else:
                return self.w3.eth.contract(address=txn_address, abi=txn_abi)
        except:
            self.DecrementNonce()

    def SignTransaction(self, txn, private_key):
        return self.w3.eth.account.sign_transaction(txn, private_key)

    def SendRawTransaction(self, signed_txn):
        sent_txn = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.w3.eth.wait_for_transaction_receipt(sent_txn)
