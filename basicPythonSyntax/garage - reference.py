import webbrowser
listDic = {}
with open("Reference.txt",'r') as file:
	url_list = file.read().split('\n')
	for item in url_list:
		listDic[item.split('\t')[0]] = item.split('\t')[1]
def openUrl(target = 0):
	for key, value in listDic.items():
		if target == 0 or target > len(listDic.keys()):
			webbrowser.open(item)
		elif str(target) == key[0]:
			webbrowser.open(value)


def viewUrl():
	for key in listDic.keys():
		print(f'Title: {key}\nUrl : {listDic[key]}')
		print()

viewUrl()
while 1:
	print("which file to open? Use index number. 0 to quit.")
	choice = int(input())
	if choice == 0:
		break
	openUrl(choice)