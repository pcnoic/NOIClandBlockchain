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