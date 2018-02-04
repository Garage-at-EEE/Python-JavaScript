class Human:
# class Human(object):
	def talk(self):
		print('I can talk')
	def walk(self):
		print('I can walk')
	def eat(self):
		print('I can eat')

class Teacher(Human):
	def teach(self):
		print('I can teach')

class Honored_Teacher(Teacher):
	def __init__(self,number):
		self.number = number
	def prize(self,k):
		print(f"I received {self.number} prizes.")

Tom = Human()
Tom.talk()
Bob = Teacher()
Bob.talk()
Bob.teach()

Kyle = Honored_Teacher(3)
Kyle.talk()
Kyle.prize()
