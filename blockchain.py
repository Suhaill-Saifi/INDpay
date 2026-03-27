from hashlib import sha256


def updatehash(*args):
    h = sha256()
    h.update("".join(str(a) for a in args).encode('utf-8'))
    return h.hexdigest()


class Block:
    def __init__(self, number=0, previous_hash="0" * 64, data=None, nonce=0):
        self.number        = number
        self.previous_hash = previous_hash
        self.data          = data
        self.nonce         = nonce

    def hash(self):
        return updatehash(self.number, self.previous_hash, self.data, self.nonce)

    def __str__(self):
        return (
            f"Block#: {self.number}\n"
            f"Hash: {self.hash()}\n"
            f"Previous: {self.previous_hash}\n"
            f"Data: {self.data}\n"
            f"Nonce: {self.nonce}\n"
        )


class Blockchain:
    difficulty = 4

    def __init__(self):
        self.chain = []

    def add(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.remove(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass
        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block)
                break
            block.nonce += 1

    def is_valid(self):
        for i in range(1, len(self.chain)):
            if (self.chain[i].previous_hash != self.chain[i - 1].hash() or
                    self.chain[i - 1].hash()[:self.difficulty] != "0" * self.difficulty):
                return False
        return True
