from time import time
import json
import hashlib
from flask import Flask,jsonify,request
from uuid import uuid4
import sys
from urllib.parse import urlparse


class BlockChain():
    def __init__(self):
        self.chain = []
        self.current_trxs = []
        self.nodes = set()
        self.new_block(proof=100 , previous_hash= 1)

    def new_block(self , proof , previous_hash = None):
        """ creat new block """

        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'trxs' : self.current_trxs,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
        }
        
        self.current_trxs = []
        self.chain.append(block)
        return block


    def new_trx(self , sender , reciever , amount):
        """ add a new transaction to the mempool """
        
        self.current_trxs.append({'sender': sender , 'reciever': reciever , 'amount': amount})

        return self.last_block['index'] + 1

    def register_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self,chain):
        """ chacking for validation of chain """

        current_index = 1
        last_block = chain[0]
        while current_index < len(chain):
            block = chain[current_index]
            
            if not block['previous_hash'] == self.hash(last_block):
                return False

            if not self.valid_proof(last_block['proof'],block['proof']):
                return False

            current_index += 1
            last_block = block

        return True

    @staticmethod
    def hash(block):
        """ hash a block """

        block_string = json.dumps(block , sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ return last block """
        return self.chain[-1]

    def valid_proof(self,last_proof , proof):
        """ chack if this proof is fine or not """
        this_proof = f'{proof}{last_proof}'.encode()
        this_proof_hash = hashlib.sha256(this_proof).hexdigest()
        return this_proof_hash[:4] == '0000'

    def proof_of_work(self,last_proof):
        """ shows that the work is done """
        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof += 1
        return proof

class b():
    def __init__(self):
        self.w = 5


app = Flask(__name__)

node_id = str(uuid4())

blockchain = BlockChain()


@app.route('/mine')
def mine():
    """ this will mine one block and will add it to the chain """
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_trx(sender='0',reciever='saeed',amount='12.5')
    block = blockchain.new_block(proof=proof)
    res = {
        "message":"I mined!!!",
        "index":block['index'],
        "trx":block['trxs'],
        "proof":block['proof']
    }
    return jsonify(res)

@app.route('/new_trxs', methods=['POST'])
def new_trx():
    """ will add a new transaction """
    values = request.get_json()
    print(values)
    this_block = blockchain.new_trx(sender=values['sender'],reciever=values['reciever'],amount=values['amount'])
    res = {'message': f'it will be added to {this_block}'}
    return jsonify(res),201
    


@app.route('/chain')
def full_chain():
    """ return all the chain """
    res = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain),
    }
    return jsonify(res),200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=sys.argv[1])