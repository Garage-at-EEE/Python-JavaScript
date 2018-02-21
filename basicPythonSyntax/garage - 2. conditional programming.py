# conditional programming #
loop_var = 4
if loop_var>0:
	print("here is loop_var", loop_var)
	print("here is loop_var", loop_var)
	print("here is loop_var", loop_var)
	print("here is loop_var", loop_var)


# for (;loop_var>0;loop_var-=1) does not exist!!!!

while loop_var>0:
	loop_var-=1
	print('x')

a_list = ['2','4','9']
for wudhaoiwhdawho in range(10,20,2):
	print(wudhaoiwhdawho)
	print(wudhaoiwhdawho)
	print(wudhaoiwhdawho)
	print(wudhaoiwhdawho)
	# break and continue works


# list comprehension 
new_list = [[x,y,x*y] for x in range(5) for y in [1,1,2,2] if x == 3]
print(new_list)


