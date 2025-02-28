from web3 import Web3
from config import Config

class BlockchainClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(Config.ETH_NODE_URL))
        # print(f"Connected to Ganache: {self.w3.is_connected()}")
        self.checksum_address = self.w3.to_checksum_address(Config.CONTRACT_ADDRESS)
        # print(f"Contract Address: {self.checksum_address}")
        bytecode = self.w3.eth.get_code(self.checksum_address).hex()
        # print(f"Bytecode at address: {bytecode}")
        self.contract = self.w3.eth.contract(address=self.checksum_address, abi=Config.CONTRACT_ABI)
        self.account = self.w3.eth.account.from_key(Config.PRIVATE_KEY)
        self.owner_account = self.w3.eth.account.from_key(Config.PRIVATE_KEY)
        self.owner_address = self.owner_account.address
        # print(f"Owner Account Address: {self.account.address}")
        self.ganache_accounts = self.w3.eth.accounts  # List of Ganache accounts

    def pay_for_session(self, student_address, amount_wei):
        nonce = self.w3.eth.get_transaction_count(student_address)
        print(f"Nonce for {student_address}: {nonce}")
        tx = self.contract.functions.payForSession().build_transaction({
            "from": student_address,
            "value": amount_wei,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": self.w3.to_wei("20", "gwei"),
        })
        return tx

    def update_progress(self, student_address, lessons, score, path):
        tx = self.contract.functions.updateProgress(
            student_address, lessons, score, path
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 200000,
            "gasPrice": self.w3.to_wei("20", "gwei"),
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, Config.PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def complete_challenge(self, student_address, challenge_id):
        tx = self.contract.functions.completeChallenge(
            student_address, challenge_id
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 200000,
            "gasPrice": self.w3.to_wei("20", "gwei"),
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, Config.PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def store_chat_message(self, student_address, prompt, response, path, timestamp):
        nonce = self.w3.eth.get_transaction_count(self.owner_address)
        print(f"Nonce for owner {self.owner_address}: {nonce}")
        print(f"Storing chat message for student {student_address}, prompt={prompt}, response={response}, path={path}, timestamp={timestamp}")
        tx = self.contract.functions.storeChatMessage(
            student_address, prompt, response, path, timestamp
        ).build_transaction({
            "from": self.owner_address,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": self.w3.to_wei("20", "gwei"),
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, Config.PRIVATE_KEY)
        print(f"Transaction signed with owner key: {Config.PRIVATE_KEY[:10]}...")
        try:
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Chat message tx hash: {tx_hash.hex()}, Receipt: {receipt}")
        except Exception as e:
            print(f"Chat message storage failed: {str(e)}")
            raise Exception(f"Chat message storage failed: {str(e)}")    

    def get_stats(self, student_address):
        return self.contract.functions.getStudentStats(student_address).call()