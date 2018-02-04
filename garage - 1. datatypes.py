from pprint import pprint

# data type #
integer_number = 1
print("integer_number:")
print(integer_number,'\n')

floating_number = 4.3
print("floating_number:")
print(floating_number,'\n')

string = 'garage'
print("string:")
print(string,'\n')

a_list = [1,2,'x',[1,2,3,'5']]
print("a_list:")
print(a_list,'\n')
print('list is mutable','\n')

a_tupple = (1,2,'r',[3,4])
print("a_tupple:")
print(a_tupple,'\ntupple is immutable','\n')

a_set = {4,3,'2',1}
print("a_set:")
pprint(a_set)

a_dictionary = {
				"name":"Zayn Jarvis",
				"School":"EEE",
				"hobby":{
					"sport":"basketball",
					"food":"meat"
				},
				(3,4):0
				}

print("a_dictionary:")
pprint(a_dictionary)