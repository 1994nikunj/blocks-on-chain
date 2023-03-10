import hashlib
import time


class Transaction:
    """
    Class to define the structure of a transaction.
    """
    def __init__(self, sender, receiver, amount):
        """
        Initialize a transaction instance.

        Parameters:
        sender (str): The address of the sender.
        receiver (str): The address of the receiver.
        amount (int): The amount to be transferred.
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount


class Block:
    """
    Class to define the structure of a block in the blockchain.
    """
    def __init__(self, previous_hash, transactions, timestamp, nonce=0):
        """
        Initialize a block instance.

        Parameters:
        previous_hash (str): The hash of the previous block in the blockchain.
        transactions (list): List of transactions to be included in this block.
        timestamp (int): Unix timestamp representing the time this block was created.
        nonce (int, optional): A random number used in the proof-of-work algorithm. Defaults to 0.
        """
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculates the hash of this block.
        """
        data = self.previous_hash + str(self.timestamp) + str(self.nonce) + str([t.__dict__ for t in self.transactions])
        sha = hashlib.sha256()
        sha.update(data.encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty):
        """
        Mines this block using the proof-of-work algorithm.

        Parameters:
        difficulty (int): Difficulty level used in the proof-of-work algorithm.
        """
        start_time = time.time()
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        end_time = time.time()
        print(f"Block mined in {end_time - start_time:.2f} seconds")


class Blockchain:
    """
    Blockchain class represents the blockchain data structure.
    It consists of a chain of blocks and maintains a list of pending transactions.
    """
    def __init__(self, difficulty=2):
        """
        Initialize a new instance of the Blockchain class.
        :param difficulty: Difficulty level for mining a block. The number of leading zeros required in the hash.
        """
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = difficulty

    @staticmethod
    def create_genesis_block():
        """
        Create and return the genesis block of the blockchain.
        :return: A Block instance that represents the genesis block.
        """
        return Block("0", [], 0, 0)

    def add_block(self, block):
        """
        Add a block to the blockchain.
        :param block: The Block instance to be added.
        """
        self.chain.append(block)

    def mine_pending_transactions(self, miner_address):
        """
        Mine the pending transactions and add the block to the blockchain.
        :param miner_address: The address of the miner who mines the block.
        """
        timestamp = int(time.time())
        block = Block(self.get_last_block().hash, self.pending_transactions, timestamp)
        block.mine_block(self.difficulty)
        print(f"Block mined: {block.hash}")
        self.add_block(block)
        self.pending_transactions = [Transaction(None, miner_address, 1)]

    def add_transaction(self, transaction):
        """
        Add a transaction to the pending transactions list.
        :param transaction: The Transaction instance to be added.
        """
        self.pending_transactions.append(transaction)

    def get_last_block(self):
        """
        Get the latest block in the blockchain.
        :return: The latest Block instance in the blockchain.
        """
        return self.chain[-1]

    def get_balance(self, address):
        """
        Get the balance of a particular address.
        :param address: The address for which the balance is needed.
        :return: The balance of the address.
        """
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        return balance

    def is_chain_valid(self):
        """
        Check if the blockchain is valid.
        :return: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                print("Current block hash does not match")
                return False
            if previous_block.hash != current_block.previous_hash:
                print("Previous block hash does not match")
                return False
        return True


if __name__ == '__main__':
    blockchain = Blockchain()

    print("Mining block 1...")
    blockchain.add_transaction(Transaction("A", "B", 100))
    blockchain.mine_pending_transactions("miner1")

    print("Mining block 2...")
    blockchain.add_transaction(Transaction("C", "D", 10))
    blockchain.mine_pending_transactions("miner2")
