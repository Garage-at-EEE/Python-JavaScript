import webbrowser

with open("Reference.txt",'r') as file:
	for url in file.read().split('\n'):
		webbrowser.open(url)