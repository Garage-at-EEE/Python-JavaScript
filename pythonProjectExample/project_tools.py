'''

This module has three purpose:
1. change the user input to a list
2. change a dictionary to a list of strings
3. create another way for keyboard button, facilitate the process of calling a keyboard.

'''
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

class Tools:
	@staticmethod
	def msg_processor(raw_info):
		field_component = raw_info.split(",")
		field = []
		for item in field_component:
			if item != '':
				field.append(item)
		return field

	@staticmethod
	def dict_processor(dict):
		string = str(dict)
		list = string.strip('{}').replace(':','   ：   ').split(',')
		return list



	# this is the normal keyboard, parameters are multiple lists which will have both text and callback data	
	@staticmethod
	def keyboard(*args):
		kb_list=[]
		for item in args:
			if item != []:
				kb_list.append([InlineKeyboardButton(text=item[0],callback_data=item[1])])
		return InlineKeyboardMarkup(inline_keyboard=kb_list)

	# this is a special keyboard with one column of keyboard button, taking a list of values of text.
	# text will be set as callback data
	@staticmethod
	def dynamic_keyboard_1(list):
		kb_list=[]
		for item in list:
			kb_list.append([InlineKeyboardButton(text=str(item),callback_data=str(item))])
		return InlineKeyboardMarkup(inline_keyboard=kb_list)

	# function is the same as the dynamic_keyboard_1
	# but will show two columns of keyboard butotn
	@staticmethod
	def dynamic_keyboard_2(list):
		kb_list=[]
		for i in range(0,len(list),2):
			try:
				a=[InlineKeyboardButton(text=list[i],callback_data=list[i])]
				a.extend([InlineKeyboardButton(text=list[i+1],callback_data=list[i+1])])
				kb_list.append(a)
			except Exception:
				kb_list.append(a)
		# kb_list.append(InlineKeyboardButton(text='Exit',callback_data='exit'))
		return InlineKeyboardMarkup(inline_keyboard=kb_list)
