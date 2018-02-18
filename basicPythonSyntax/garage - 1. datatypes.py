from pprint import *

# data type #
integer_number = 1
print("integer_number:")
print(integer_number,'\n')

floating_number = 4.3
print("floati\ng_number:")
print(floating_number,'\n')

string = f'o'
print("string:")
print(string,'\n',end = '')

a_list = [1,2,'x',[1,2,3,'5']]
print("a_list:")
print(a_list,'\n')
print('list is mutable','\n')

a_tupple = (1,2,'r',[3,4])
print("a_tupple:")
print(a_tupple,'\ntupple is immutable','\n')

a_set = {4,3,'2',1,1,1,1}
print("a_set:")
pprint(a_set)

a_dictionary = {
				"name":"Zayn Jarvis",
				"School":"MAE",
				"School":"EEE",
				"hobby":{
					"sport":"basketball",
					"food":''
				},
				8:90,
				(3,4):0
				}
a_food = input("your f f")
a_dictionary["hobby"]["food"] = a_food

print("a_dictionary:")
print(a_dictionary)
pprint(a_dictionary)