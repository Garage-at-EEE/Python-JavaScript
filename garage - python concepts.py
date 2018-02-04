from math import *
# LEGB & LBYL & EAFP #


# # LEGB : local enclosing global built-in#
# # local
# def outer_function():
# 	def inner_function():
# 		x = 3
# 		print(x)
# 	inner_function()
# 	print(x)

# outer_function()
# # enclosing

# def outer_function():
# 	x = 3
# 	def inner_function():
# 		print(x)
# 	print(x)

# # global

# x = 3
# def outer_function():
# 	def inner_function():
# 		print(x)
# 	print(x)

# # built-in

# def outer_function():
# 	def inner_function():
# 		print(pi)
# 	inner_function()

# outer_function()

# LBYL : Look before you leap #


# while 1:
# 	print("enter an expression for adding two double digit numbers")
# 	x = input()
# 	input_validate = True
# 	for element in x.split('+'):
# 		element = element.strip()
# 		if element not in [str(i) for i in range(100)]:
# 			input_validate = False
# 			break
# 	if input_validate:
# 		exec("result = "+x)
# 		print("correct input!!!")
# 		print(result)
# 		break
# 	else:
# 		print("wrong input")
# 	print()


# EAFP easier to ask forgiveness then permission#

# while 1:
# 	print("enter an expression for adding two double digit numbers")
# 	x = input()
# 	try:
# 		exec("result = "+x)
# 		print("correct input!!!")
# 		print(result)
# 		break
# 	except Exception:
# 		print("wrong input")




