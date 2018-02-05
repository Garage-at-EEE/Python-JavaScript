from math import *
print(pi)
# LEGB & LBYL & EAFP #


# LEGB : local enclosing global built-in#
# local
# x = 3
# def outer_function():
# 	def inner_function():
# 		print(x)
# 	inner_function()
# 	print(str(x)+'!')
# outer_function()
# print(x)
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
# 	print()
# 	x = input("enter an expression for adding two double digit numbers")
# 	input_validate = True
	# for element in x.split('+'):
	# 	element = element.strip()
	# 	if element not in [str(i) for i in range(100)]:
	# 		input_validate = False
	# 		break
	# if input_validate:
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
# 	except error:
# 		print("wrong input1")
# 	except othererrors:
# 		print("wrong input2")
# 	except Exception:
# 		print("wrong input2")
# 	else:
# 		print("right input")
# 	finally:
# 		print("i run")

# Duck typing

in C

# int C_function(int var_1,char var_2 ); //function decleration
# int C_function(var_1,var_2){
# 	function_concerning_integer(var1)
# 	function_concerning_character(var2)
# 	return integer type
# }
# C_function('a',b)

# def Py_function(var1, var2):
# 	print(var1+var2)

# function and method
def function(x):
	print(1+x)
class funcs:
	def function(x):
		print(1+x)
function(2)
funcs.function(2)