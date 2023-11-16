"""
	@Program		: Python Bank Script
	@Author 		: Adam Hussein
	@Author School	: Virginia Commonwealth University
	@Author Major	: Computer Science
	@Description	: This is the Bank module that sets up the BOH system.
					  It will be used to set up the bank class and functions that
					  are there to help the user use the system.
					  ***This is a personal project that is not intended for public use nor
					  for solving any real world problems.***
"""

from random import randint
from Email import send_email
import datetime

# Have file name here in case we change it in the future
file_name = 'people.txt'

# Open file with user data. Make one if it does not exist.
try:
	file = open(file_name)
except FileNotFoundError:
	file = open(file_name, 'a+')
	file.write('NAME, EMAIL, NOTIFICATIONS, ACCOUNT#, ROUTING#, USERNAME, PASSWORD, BALANCE')

# Bank routing number
routing_num = '947623558'
# Gather the total amount of people who have an account with us
# We subtract one since the first line of text file is a header
user_count = 0
for line in file:
	user_count += 1
user_count -= 1
file.close()

# The Bank class and all the functions associated with it
class Bank:
	def __init__(self, name, email, notifications, accnum, routnum, uname, pw, balance):
		"""Represents a person object for a bank account.
			:param name: str
			:param email: str
			:param notifications: str
			:param accnum: str
			:param routnum: str
			:param uname: str
			:param pw: str
			:param balance: float"""
		self.name = name
		self.email = email
		self.notifications = notifications
		self.account_num = accnum
		self.routing_num = routnum
		self.username = uname
		self.password = pw
		self.balance = balance

	def __str__(self):
		"""If the user wishes to view their account details, this
		function will return their details
		:param self: user object"""
		name = self.name
		balance = self.balance
		accnum = self.account_num
		routnum = self.routing_num
		email = self.email
		uname = self.username
		notifications = self.notifications
		return '\nName: %s\nBalance: $%.2f\nAccount #: %s\nRouting #: %s\nEmail: %s\nUsername: %s\n' \
			   'Deposit and Withdrawal Notifications: %s' % (name, balance, accnum, routnum, email, uname, notifications)

	@staticmethod
	def create_account():
		"""Creates an account"""
		global user_count
		global routing_num

		# Gather all the information needed and generate account and routing numbers
		f = open(file_name, 'a')
		n = input('Enter your first name: ').strip()
		n = n + ' ' + input('Enter your last name: ').strip()

		# For the email, we must check to make sure it is a real, unused, and valid email
		e = input('Enter your email: ')
		email_validity = Bank.is_valid_email(e)
		while not email_validity == 'valid':
			e = input('The email you entered is %s. Please enter a different one: ' % email_validity)
			email_validity = Bank.is_valid_email(e)
		account_num = Bank.generate_account_number()
		username = input('Create a username: ')
		while not Bank.is_valid_username(username):
			username = input('Username is already in use. Try another: ')
		pw = input('Create a password: ')
		pw_check = input('Re-type your password to confirm: ')
		while pw_check != pw:
			pw_check = input('Passwords do not match. Please re-type your password: ')
		amount = input('How much will you be depositing to start? $')
		while not Bank.is_valid_amount(amount):
			amount = input('Please enter a valid number: $')
		amount = float(amount)
		notifications = input('Would you like to receive notifications via email regarding changes to your account'
							 ' (deposits and withdrawals)? ').upper()
		while notifications != 'YES' and notifications != 'NO':
			notifications = input('Please say "yes" or "no": ').upper()

		# Now, we add person to our text file and increment total amount of users
		f.write('\n%s, %s, %s, %s, %s, %s, %s, %.2f' % (n, e, notifications, account_num, routing_num, username, pw, amount))
		f.close()
		print('\nSuccess! Your account was created.\n')
		user_count += 1
		p = Bank(n, e, notifications, account_num, routing_num, username, pw, amount)

		# Now we email the user to confirm everything
		p.send_confirmation_email()

	def update_account(self, info, new_info):
		"""We use this function to update the file with the new user
		information. The 'info' parameter will be based on the index of the
		info in the file. For example, if info = 0, that means the user is
		changing their name.
		:param self: user object
		:param info: int
		:param new_info: str"""
		f = open(file_name, 'r')

		# We will use an index variable to find out which line user is in
		# Email is unique, so we will use that
		index = 0
		for user in f:
			if user.split(', ')[1] == self.email:
				f.close()
				break
			index += 1

		# Now that we have the user, lets change the info
		f = open(file_name, 'r')
		users = f.readlines()
		f.close()

		# We hold a temporary version of the user so that we can change it
		temp_user = users[index].split(', ')
		temp_user[info] = new_info
		temp_user = ', '.join(temp_user)
		users[index] = temp_user
		f = open(file_name, 'w')
		f.writelines(users)
		f.close()

	def send_confirmation_email(self):
		"""This function sends a confirmation email to the user when they
		create an account.
		:param self: user object"""

		# Here we gather all the info: Date when account is created, a subject line, and a message
		dt = datetime.date.today().strftime("%m/%d/%Y")
		subject = 'Account Confirmation'
		body = "This is to confirm that your account for BOH was created! Here are your account details:\n\nName: %s" \
			   "\nUsername: %s\nAccount #: ******%s\nRouting #: *****%s\nDate Created: %s\n" \
			   % (self.name, self.username, self.account_num[6:], self.routing_num[5:], dt)
		if self.notifications == 'YES':
			body = body + 'You have signed up to receive updates regarding deposits and withdrawals.\n'
		else:
			body = body + 'You have chosen not to receive updates regarding deposits and withdrawals.\n'
		body = body + "\nIf you do not recognize this activity, please reply to this email and our customer " \
					  "service team will assist you. Otherwise, welcome to BOH!!"

		# Get user email then send
		recipients = [self.email]
		send_email(subject, body, recipients)

	def send_transaction_email(self, dep_or_with, amount):
		"""Sends a notification to user (if opted) regarding a deposit
		or withdrawal made. It includes the type, the date, and amount.
		:param self: user object
		:param dep_or_with: 'deposit' or 'withdrawal'
		:param amount: float"""

		# Here we gather all the info: Date of transaction, type of transaction, a subject line, and a message
		dt = datetime.date.today().strftime("%m/%d/%Y")
		subject = dep_or_with[0].upper() + dep_or_with[1:] + ' made on ' + dt
		body = "This is a confirmation of a %s made on your account. Details are below:\n\n" \
			   "Date of Transaction: %s\nAmount: $%.2f\nNew Balance: $%.2f\n\nIf you do not recognize this activity, " \
			   "please reply to this email and our customer service team will assist you. Otherwise, " \
			   "you may ignore this email." % (dep_or_with, dt, float(amount), self.balance)
		recipients = [self.email]
		send_email(subject, body, recipients)

	def send_account_change_email(self, change):
		"""We email the user letting them know either
		their username, password, or email was changed and the date.
		:param self: user object
		:param change: str"""

		# Here we gather all the info: Date change, type of change, a subject line, and a message
		dt = datetime.date.today().strftime("%m/%d/%Y")
		subject = change[0].upper() + change[1:] + ' change made on ' + dt
		body = "This email is letting you know your %s was changed on %s\n\n" \
			   "If you do not recognize this activity, please reply to this email and our " \
			   "customer service team will assist you. Otherwise, you may ignore this email." % (change, dt)
		recipients = [self.email]
		send_email(subject, body, recipients)

	@staticmethod
	def is_valid_email(email):
		"""We check to see if user has entered a valid and unused email
		address. We return 'invalid' if email is invalid or 'used' if
		email is used. If all are good, we return 'valid'
		:param email: str"""

		# We have our email domains to use when creating accounts to verify emails
		email_domains = ['@gmail.com', '@yahoo.com', '@hotmail.com']

		# Email is immediately invalid without an '@'
		if '@' not in email:
			return 'invalid'

		# Here we check to make sure email is not used already in system
		f = open(file_name)
		for p in f:
			# Split the line into its component variables
			person = list(map(str, p.split(', ')))
			if person[1] == email:
				f.close()
				return 'used'
		f.close()

		# We will find the index of the last occurrence of the '@'
		# This way, the user can have a '@' in their email if they wish
		index = email.rfind('@')

		# Finally, we check if whatever after '@' is a valid domain
		if email[index:len(email)] not in email_domains:
			return 'invalid'

		# If we reach this point, the email is ok to use
		return 'valid'

	@staticmethod
	def is_valid_username(uname):
		"""We check to see if user has entered an unused username.
		We return True if valid and False otherwise.
		:param uname: str"""

		# Here we check to make sure username is not used already in system
		f = open(file_name)
		for p in f:
			# Split the line into its component variables
			person = list(map(str, p.split(', ')))
			if person[5] == uname:
				f.close()
				return False
		f.close()
		return True

	@staticmethod
	def is_valid_amount(amount):
		"""We check to see if user has entered a valid number
		for an amount when doing first deposit, regular
		deposits, and withdrawals then return 'True' or 'False'
		:param amount: str"""

		# Make sure customer enters something
		if amount == '' or amount == '.':
			return False

		# We have a string containing valid values for a number when depositing
		nums = '1234567890.'
		for digit in amount:
			if digit not in nums:
				return False
		return True

	@staticmethod
	def generate_account_number():
		"""Generates and returns a random, unused, 10-digit
		account number in the form of a string"""

		# Generate number
		num = ''
		for i in range(10):
			num = num + str(randint(0, 9))

		# Make sure account number is unused
		f = open(file_name)
		for p in f:
			person = tuple(map(str, p.split(', ')))
			if person[3] == num:
				f.close()
				return Bank.generate_account_number()
		f.close()
		return num

	def change_username(self):
		"""User can change their username.
		:param self: user object"""

		# Prompt user for new username then make sure it's unused
		new_uname = input('Enter a new username: ')
		while not Bank.is_valid_username(new_uname):
			new_uname = input('Username is already in use. Try another: ')
		print('Success! Username has been changed.\n')
		self.username = new_uname
		self.update_account(5, new_uname)
		self.send_account_change_email('username')
		return Bank.sign_in()

	def change_password(self):
		"""User can change their password.
		:param self: user object"""

		# Have user enter old password then the new one
		old_pw = input("Enter your old password: ")
		while not old_pw == self.password:
			old_pw = input('Password incorrect, please try again: ')
		new_pw = input('Enter a new password: ')
		pw_check = input('Re-type your password to confirm: ')
		while pw_check != new_pw:
			pw_check = input('Passwords do not match. Please re-type your password: ')

		# Update it
		print('Success! Password has been changed.\n')
		self.password = new_pw
		self.update_account(6, new_pw)
		self.send_account_change_email('password')
		return Bank.sign_in()

	def change_email(self):
		"""User can change their email.
		:param self: user object"""

		# Prompt user for new email and make sure it's valid
		new_email = input('Enter a new email: ')
		while not Bank.is_valid_email(new_email):
			new_email = input('Email is already in use. Try another: ')

		# Update it
		print('Success! Email has been changed.\n')
		self.send_account_change_email('email')
		self.email = new_email
		self.update_account(1, new_email)
		return Bank.sign_in()

	def change_notify_setting(self):
		"""User can change their notification setting.
		:param self: user object"""

		# See what the user currently has as their setting, then get the opposite of that
		if self.notifications == 'YES':
			notify_on_or_off = 'on'
			opposite = 'off'
		else:
			notify_on_or_off = 'off'
			opposite = 'on'

		# Ask user if they want to change it
		print("You currently have notifications about deposits and withdrawals %s." % notify_on_or_off)
		confirmation = input('Would you like to turn them %s ("yes" or "no")? ' % opposite).upper()
		while not confirmation == 'YES':
			if confirmation == 'NO':
				return
			confirmation = input('Please type "yes" or "no": ')
		if self.notifications == 'YES':
			self.notifications = 'NO'
		else:
			self.notifications = 'YES'
		print('Success! Your notification settings about deposits and withdrawals has been changed.')

		# Notify user of change and update account
		# Here we gather all the info: Date change, type of change, a subject line, and a message
		dt = datetime.date.today().strftime("%m/%d/%Y")
		subject = 'Notification settings for deposits and withdrawals change made on ' + dt
		body = "This email is letting you know your notification settings was changed on %s. They have been turned " \
			   "%s.\n\nIf you do not recognize this activity, please reply to this email and our " \
			   "customer service team will assist you. Otherwise, you may ignore this email." % (dt, opposite)
		recipients = [self.email]
		send_email(subject, body, recipients)
		self.update_account(2, self.notifications)

	def delete_account(self):
		"""We use this to set the user up with deleting their
		account. An email will be sent to the user letting them know that
		their account will be deleted unless cancelled within 24 hours.
		:param self: user object"""
		confirmation = input('We are sad to see you go! Are you sure you would like to proceed?\nIf you say yes, '
							 'your account will be deleted within 24 hours unless you reverse it. Please type '
							 '"yes" or "no": ').upper()
		while not confirmation == 'YES':
			if confirmation == 'NO':
				return
			confirmation = input('Please type "yes" or "no": ').upper()
		dt = datetime.date.today().strftime("%m/%d/%Y")
		subject = 'Request to delete account made on ' + dt
		body = "This email is letting you know your account is scheduled for deletion. This request " \
			   "was made on %s.\n\nIf you do not recognize this activity, please reply to this email and our " \
			   "customer service team will assist you. Otherwise, you may ignore this email, but we are sad to see " \
			   "you go! Your account will be deleted in 24 hours." % dt
		recipients = [self.email]
		send_email(subject, body, recipients)

	def menu(self):
		"""The user will be sent here when 'View Account' is chosen.
		The user will have an option to either: change username, change
		password, change email, or delete account. The user will be
		notified via email of any change that occurs."""

		# We have a list to display the options available for the user to change their account
		options = ['Change Username', 'Change Password', 'Change Email', 'Change Notification Settings', 'Delete Account']
		while True:
			print(self)
			print('You have options to change your account in the following ways. Type either one or "exit" to exit menu:')
			for option in options:
				print(option)
			option = input().lower()
			if option == options[0].lower():
				self.change_username()
				return
			elif option == options[1].lower():
				self.change_password()
				return
			elif option == options[2].lower():
				self.change_email()
			elif option == options[3].lower():
				self.change_notify_setting()
			elif option == options[4].lower():
				self.delete_account()
				return
			elif option == 'exit':
				return
			else:
				print('We were unable to process your request. Please try again')

	def deposit(self):
		"""Adds money to bank account
		:param self: user object"""
		amount = input('How much would you like to deposit? $')

		# Check to make sure user enters a valid number
		if not Bank.is_valid_amount(amount):
			print('Please enter a valid numerical value.\n')
			return self.deposit()
		amount = float(amount)
		self.balance = float(self.balance)
		self.balance += amount
		print('SUCCESS! $%.2f was added to your account.\n' % amount)
		if self.notifications == 'YES':
			self.send_transaction_email('deposit', amount)

		# Update the file
		self.update_account(7, str(self.balance) + '\n')

	def withdrawal(self):
		"""Removes money from bank account, if possible
		:param self: user object"""
		amount = input('How much would you like to withdrawal? Or, if you wish to cancel, please type "cancel" $')
		if amount.lower() == 'cancel':
			print('Withdrawal has been cancelled.\n')
			return

		# Check to make sure user enters a valid number
		if not self.is_valid_amount(amount):
			print('Please use only numerical values in your request or "cancel" to cancel.\n')
			return self.withdrawal()
		amount = float(amount)
		if self.balance < amount:
			print('ERROR: Insufficient funds.\n')
			return
		else:
			self.balance -= amount
			print('SUCCESS! $%.2f was withdrawn from your account.\n' % amount)
		if self.notifications == 'YES':
			self.send_transaction_email('withdrawal', amount)

		# Update the file
		self.update_account(7, str(self.balance) + '\n')

	@staticmethod
	def sign_in():
		"""Initiates a sign-in process"""
		f = open(file_name)
		global user_count
		a = input('Please enter your username: ')

		# We begin a check to make sure user has entered an existing account
		while True:
			# We have this empty list to use when we finally find the user account
			acc = []

			# We use this count, 'count2', as a way to check if we have checked through the entire list of
			# registered users. It is initially -1 since the first line of file is a header
			count2 = -1
			for p in f:
				# Split the line into its component variables
				person = list(map(str, p.split(', ')))

				# The 5th column of the file is the username
				if a == person[5]:
					acc = person
					break
				else:
					count2 += 1

				# Check to see if we reached the end!
				if count2 > user_count:
					print('No account is associated with that username. Please try again.\n')
					return Bank.sign_in()
			break

		# If we make it here, username is valid, and now we need the password
		pw = input("Please enter your password: ")

		# The 6th column of the file is the user password
		while pw != acc[6].strip():
			pw = input('The password you entered does not match. Please try again: ')
		f.close()

		# We now know who this user is, and they validated using their password
		# Now, return their information
		return Bank(acc[0], acc[1], acc[2], acc[3], acc[4], acc[5], acc[6], float(acc[7]))

	def initiate(self):
		"""Initiates the methods on the user
		:param self: user object"""

		# We have the options that our customers can do
		methods = ['Deposit', 'Withdrawal', 'View account']

		# We welcome the user then inform them of what they can do
		index = self.name.index(' ')
		print('\nWelcome, %s. Please choose an option from below:' % self.name[0:index])
		print('Here is what you can do with your account:')
		while True:
			for i in range(len(methods)):
				print('%d. %s' % (i + 1, methods[i]))
			option = input('To do any of the above, simply enter what it says. To sign-out, just enter "sign out": ').lower()
			if option == methods[0].lower():
				self.deposit()
			elif option == methods[1].lower():
				self.withdrawal()
			elif option == methods[2].lower():
				self.menu()
			elif option == 'sign out':
				print('You have been signed out.\n')
				break
			else:
				print('We were unable to process your request. Please try again.\n')