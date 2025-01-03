"""
	@Program		: Python Main Script
	@Author 		: Adam Hussein
	@Author School	: Virginia Commonwealth University
	@Author Major	: Physics
	@Description	: This is the main module that runs the BOH system
					  It is an infinite loop that will only terminate if done forcefully.
					  ***This is a personal project that is not intended f public use nor
					  for solving any real world problems.***
"""

from Bank import Bank

while True:
	print('To sign in, please type "sign in"')
	c = input('To create an account, please type "create." Type "exit" to exit.\n')
	if c.lower() == 'create':
		Bank.create_account()
		continue
	elif c.lower() == 'sign in':
		p = Bank.sign_in()
		Bank.initiate(p)
	elif c.lower() == 'exit':
		break
