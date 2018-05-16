import requests # learn more: https://python.org/pypi/requests
import hashlib 
import json 
from textwrap import dedent

from time import time 
from uuid import uuid64

from flask import Flask

class Blockchain(object): 
	def __init__(self): 
		self.chain = [] 
		self.current_transactions = [] 
		
		#creating the ORIGINAL GENESIS block 
		self.new_block(previous_hash=1, proof=100)
		
	def proof_of_work(self, last_proof): 
		""" 
		Simple Proof of Work Algorithm 
		
		- Find a number p' such that hash(pp') contains leading 4 zeroes where p is the previous p' 
		- p is the previous proof, and p' is the new proof 
		
		:param last_proof: <int> 
		:return: <int> 
		
		""" 
		
		proof = 0 
		while self.valid_proof(last_proof, proof) is False:
			proof += 1 
			
		return proof
		
	@staticmethod
	def valid_proof(last_proof, proof):
		""" 
		Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes ? 
			
		:param last_proof: <int> Previous Proof 
		:param proof: <int> Current Proof 
		:return: <bool> True if correct, False if not 
			
		""" 
		guess = f'{last_proof}{proof}'.encode() 
		guess_hash = hashlib.sha256(guess).hexdigest() 
		return guess_hash[:4] == "0000"

	def new_block(self):
		#creating the new block and adding it to the chain 
		""" 
		Create a new Block in the Blockchain 
		
		:param proof: <int> Proof given by the Proof of Work algorithm 
		:param previous_hash: (Optional) <str> Has og previous Block 
		:return: <dict> New block 
		
		""" 
		
		block = { 
			'index': len(self.chain) + 1, 
			'timestamp': time(), 
			'transactions': self.current_transactions, 
			'proof': proof, 
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			}
			
			#resetting the current list of transactions 
		self.current_transactions = [] 
			
		self.chain.append(block)
		return block

	def new_transaction(self, sender, recipient, amount):
		"""
		Creates a new transaction 
		
		:param sender: <str> Address of the Sender 
		:param recipient: <str> Address of the Recipient 
		:param amount: <int> Amount 
		:return <int> The index of the Block that holds the transaction
		
		"""
		
		self.current_transactions.append({
			'sender': sender, 
			'recipient': recipient,
			'amount': amount,
		})
	
	

	@staticmethod 
	def hash(block): 
		""" 
		
		Creates a SHA-256 hash of a Block 
		
		:param block: <dict> Block 
		:return <str> 
		
		""" 
		
		block_string = json.dumps(block, sort_keys=True).encode() 
		return haslib.sha256(block_string).hexdigest() 
		

	@property 
	def last_block(self): 
		#return the last block in the chain 
		pass 

#CREATING THE SERVER THAT WILL OCCUPY A SINGLE  NODE IN OUR BLOCKCHAIN NETWORK 
#initiating the node
app = Flask(__name__) 

#generate a globally unique address for this node 
node_id = str(uuid64()).replace('-', '') 

#instantiate the blockhcain 
blockchain = Blockchain()  
 
@app.route('/mine', methods=['GET']) 
def mine():
	#running the P-O-W algorithm to get the next proof 
	last_block = blockchain.last_block 
	last_proof = last_block['proof'] 
	proof = blockchain.proof_of_work(last_proof) 
	
	#receive the award for finding the proof 
	#sender set to 0 to signify that this node has mined a coin 
	blockchain.new_transaction(
		sender ="0", 
		recipient=node_identifier,
		amount=1
		)
		
	#forge the new Block by adding it to the cain 
	previous_hash = blockchain.hash(last_block)
	block = blockchain.new_block(proof, previous_hash) 
	
	response = {
		'message': 'New Block forged', 
		'index': block['index'], 
		'transactions': block['transactions'], 
		'proof': block['proof'],
		'previous_hash': block['previous_hash'],
	}
	return jsonify(response), 200
	
	
@app.route('/transactions/new', methods=['POST']) 
def new_transaction():
	values = request.get_json() 
	
	#check if the data required are provided
	required = ['sender', 'recipient', 'amount']
	if not all(k in values for k in required):
		return 'Missing values', 400 
		
	#create a new transaction 
	index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
	
	response = {'message': f'Transaction will be added to Block {index}'} 
	return jsonify(response), 201 
	
	
@app.route('/chain',methods=['GET']) 
def full_chain():
	response = {
		'chain': blockchain.chain,
		'length': len(blockchain.chain)
	}
	return jsonify(response), 200 
	
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000) 
	
	
	



