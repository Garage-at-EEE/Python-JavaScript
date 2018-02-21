class Human:
# class Human(object):
	def talk(self):
		print('I can talk')
	def walk(self):
		print('I can walk')
	def eat(self):
		print('I can eat')
class Teacher():
	def teach(self):
		print('I can teach')

class Honored_Teacher(Teacher,Human):
	def __init__(self,number):
		self.number = number
	def prize(self):
		print(f"I received {self.number} prizes.")

Tom = Human()
Tom.talk()

Tom2 = Human()
Tom2.talk()
Bob = Teacher()
Bob.teach()

Kyle = Honored_Teacher(3)
Kyle.talk()
Kyle.teach()
Kyle.prize()
