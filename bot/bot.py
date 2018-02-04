import csv
import ast
import time
import telepot
import asyncio
from telepot import DelegatorBot
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open,per_chat_id_in
from telepot.aio.delegate import intercept_callback_query_origin,include_callback_query_chat_id
from telepot.aio.loop import MessageLoop
from telepot.aio.helper import ChatHandler
import telepot.namedtuple
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


'''

User defined modules

'''
from project_tools import Tools
from Data_class import Data
from wiki import wiki
from wiki import wiki_title

#----------------Process One------------------------------------------
initial_process = 'initial_process'
##
initial_stage = 'initial_stage'
create_main_database = 'create_main_database'#for implement of keywords
set_information_database = 'set_information_database'
#----------------------------------------------------------

#----------------Process Two------------------------------------------
club_setting_process = 'club_setting_process'#for group_names.
##
initial_stage = 'initial_stage'
set_group_photo = 'set_group_photo'
group_name_setting = 'group_name_setting'
subcommittee_setting = 'subcommittee_setting'
maincommittee_setting = 'maincommittee_setting'
#----------------------------------------------------------

#----------------Process Three------------------------------------------
creator_profile = 'creator_profile'
##
initial_stage = 'initial_stage'
edit_info = 'edit_info'
#----------------------------------------------------------

'''
normal executing interface 
'''

#----------------Process Four------------------------------------------
working_process = 'working_process'
##
initial_stage = 'initial_stage'
create_member_profile = 'create_member_profile'
edit_info = 'edit_info'
organize_activity='organize_activity'
make_announcement='make_announcement'
show_activity_database='show_activity_database'
change_hierarchy='change_hierarchy'
change_group = 'change_group'
#----------------------------------------------------------

#----------------Process Five------------------------------------------
activity_process = 'activity_process'
##
collect_feedback = 'collect_feedback'
send_feedback = 'send_feedback'
query_stage = 'query_stage'## essential to stop showing main menu when answering queries
#----------------------------------------------------------


class Main(ChatHandler):
	club_name=''
	processing_stage = initial_process
	activity_name = ''
	activity_step = 0
	Dict_group_leaders = dict()
	fieldname=[]
	Hierarchy_0 = ['President']
	Hierarchy_1 = []
	Hierarchy_2 = []
	Hierarchy_3 = ['Member']
	group_names=[]
	activity_buffer = []
	activity_list=[]
	def __init__(self,*args,**kwargs):
		super(Main,self).__init__(*args,**kwargs)
		self.stage = initial_stage
		self.count = 0
		self.ID = 0
		self.query_dict = {}
		self.Dictprofile = {}
		self.edit = ''
		self.info_setting = 0
		if Main.processing_stage == initial_process:# for reading settings everyday after heroku restart.
			try:
				db = Data('Setting',0)
				Main.club_name,\
				Main.processing_stage ,\
				Main.activity_name ,\
				= db.read_file('keys')[:3]
				Main.activity_step = int(db.read_file('keys')[3])
				Main.Dict_group_leaders = ast.literal_eval(db.read_file('keys')[4])
				Main.fieldname = ast.literal_eval(db.read_file('keys')[5])
				Main.Hierarchy_0  = ast.literal_eval(db.read_file('keys')[6])
				Main.Hierarchy_1  = ast.literal_eval(db.read_file('keys')[7])
				Main.Hierarchy_2  = ast.literal_eval(db.read_file('keys')[8])
				Main.Hierarchy_3  = ast.literal_eval(db.read_file('keys')[9])
				Main.group_names = ast.literal_eval(db.read_file('keys')[10])
				Main.activity_buffer  = ast.literal_eval(db.read_file('keys')[11])
				Main.activity_list = ast.literal_eval(db.read_file('keys')[12])
			except Exception:
				pass
########################################################################################################################################################################
########################################################################################################################################################################
	async def on_chat_message(self,msg):
		self.ID = msg['chat']['id']
		content_type, chat_type, chat_id = telepot.glance(msg)
		self.first_name = msg["chat"]["first_name"]
#########################   TOOLS #########################################
		async def _Create_Profile(text):
			try:
				tem = Main.fieldname[self.count]
			except Exception:
				self.Dictprofile[Main.fieldname[int(self.count)-1]]=text
				string_profile = Tools.dict_processor(self.Dictprofile)
				for item in string_profile[3:] :
					await self.sender.sendMessage(item)
				await self.sender.sendMessage('Check whether your profile is correct.',\
				reply_markup = Tools.keyboard(('Yes, the profile is correct.','confirm'),('No, something goes wrong.','wrong'))) #
				self.stage = ''
			else:
				await self.sender.sendMessage(f'Your {Main.fieldname[int(self.count)-1]} is "{text}".\nIf the information is correct, what is your {Main.fieldname[int(self.count)]}'\
										,reply_markup = Tools.keyboard(('Reset','reset')))
				self.Dictprofile[Main.fieldname[int(self.count)-1]]=text
				self.count+=1

		async def _Change_Info(text):
			self.Dictprofile[self.edit]=text
			string_profile = Tools.dict_processor(self.Dictprofile)
			for item in string_profile[3:] :
				await self.sender.sendMessage(item)
			await self.sender.sendMessage('Check whether your profile is correct.',\
			reply_markup = Tools.keyboard(('Yes, the profile is correct.','confirm'),('No, something is wrong.','wrong'))) #
			self.stage = initial_stage

		async def _exit_():
			self.count+=1
			if self.count%4 ==3:
				await self.sender.sendMessage(f'Do your want to start the <b>{Main.club_name}</b> bot now?',reply_markup=Tools.keyboard(('Start Now.','start'),('Exit','exit')),parse_mode = 'HTML')
		
		async def _Create_Member_Profile():
			if self.stage == initial_stage:
				await self.sender.sendMessage(f'You are about to create your own profile for <b>{Main.club_name}</b> now.',reply_markup = Tools.keyboard(('start','start')),parse_mode = 'HTML') #
			elif self.stage == create_member_profile:
				text = msg['text']
				await _Create_Profile(text)
			elif self.stage == edit_info:
				text = msg['text']
				await _Change_Info(text)
#########################   TOOLS #########################################
#########################   Initial Setting   #########################################

		async def _Initial_Process():
			if self.stage == initial_stage:
				if self.count ==0:
					await self.sender.sendMessage('HI! Mr.President.')
					await self.sender.sendMessage('What is the name of our club?')
					self.count = 1
				else:
					Main.club_name = msg['text']
					await self.sender.sendMessage(f'Is our club <b>{Main.club_name}</b>?',reply_markup=Tools.keyboard(('Reset','reset_0'),('Confirm','confirm_0')),parse_mode = 'HTML')

			elif self.stage == set_information_database:
				await self.sender.sendMessage(f'I will help you with creating a database for <b>{Main.club_name}</b>.\n'+\
										'EXCOs will have access to all members information.',reply_markup=Tools.keyboard(\
												('Set the information you need.','create'))\
												,parse_mode = 'HTML')#stage 1 of initialization
			elif self.stage == create_main_database:
				field = Tools.msg_processor(msg['text'])
				Main.fieldname.extend(field)
				tem = str(Main.fieldname)
				await self.sender.sendMessage('Initialized successfully!\nYour keyswords setting includes\n'+\
										f'<b>{tem.strip("[]")}</b>',reply_markup=Tools.keyboard(('Reset','reset'),('Confirm','confirm')),parse_mode = 'HTML')

		async def _Club_Setting_Process():
			if self.stage == 'exit':
				await _exit_()
			elif self.stage == group_name_setting:
				Main.group_names = Tools.msg_processor(msg['text'])
				tem = str(Main.group_names)
				await self.sender.sendMessage(f'The groups in <b>{Main.club_name}</b> are <b>{tem.strip("[]")}</b>',reply_markup=Tools.keyboard(('Reset','reset'),('Confirm','confirm_0')),parse_mode = 'HTML')
			elif self.stage == subcommittee_setting:
				text = msg['text']
				if self.count !=0:
					Main.Dict_group_leaders[Main.group_names[self.count-1]]=Tools.msg_processor(text)
				try:
					await self.sender.sendMessage(f'Please indicate <b>the group leaders</b> of <b>{Main.group_names[self.count]}</b> and seperated them with commas.'\
													,reply_markup = Tools.dynamic_keyboard_1(['reset']),parse_mode = 'HTML')
					self.count+=1
				except Exception:
					for key in Main.Dict_group_leaders.keys():
						tem = str(Main.Dict_group_leaders[key])
						await self.sender.sendMessage(f'<b>{key}</b> has <b>{tem.strip("[]")}</b>',parse_mode = 'HTML')
					await self.sender.sendMessage(f'Check the <b>group leaders</b> setup for each groups.'\
											,reply_markup = Tools.keyboard(('That\'s right.','right'),('Something goes wrong...','wrong')),parse_mode = 'HTML')

		async def _Zero_Profile():
			if self.stage == 'exit':
				await _exit_()
			elif self.stage == initial_stage:
				text = msg['text']
				await _Create_Profile(text)
			elif self.stage == edit_info:
				text = msg['text']
				await _Change_Info(text)
#########################   Initial Setting   #########################################
#########################   EXCOs functions   #########################################
		async def _Working_Process_Managers():
			print(content_type)
			try:
				text=msg['text']
			except Exception:
				pass
			if self.stage == initial_stage or self.stage == collect_feedback:  #when you are in the working process, you can send any message to activate the action keyboard
				button = ['Send an announcement',f'Require {Main.club_name} Database.',f'Change members\' Hierarchy.','Edit profile & Registration']
				if Main.processing_stage != activity_process: # cannot show this button when there is a activity in progress
					button.insert(0,'Initiate a club activity.')
				await self.sender.sendMessage('Hi, manager! What can I help you with?'\
										,reply_markup=Tools.dynamic_keyboard_1(button))

				if Main.activity_step == 1:# use activity step to specify the process of activity setting.
					await self.sender.sendMessage(f'You may terminate registration for <b>{Main.activity_name}</b> at any time.'\
											,reply_markup = Tools.dynamic_keyboard_1(['Terminate registration.']),parse_mode = 'HTML')
				elif Main.activity_step == 2:
					await self.sender.sendMessage(f'After the activity "<b>{Main.activity_name}</b>", you can start to receive members\' feedback~'\
											,reply_markup = Tools.dynamic_keyboard_1(['Start collecting feedback.']),parse_mode = 'HTML')
				elif Main.activity_step == 3:
					await self.sender.sendMessage(f'You can close the activity <b>{Main.activity_name}</b> or just view the feedback from the members.'\
											,reply_markup = Tools.dynamic_keyboard_1(['Close the activity.','View the feedback']),parse_mode = 'HTML')
					self.count = 0

			elif self.stage==make_announcement:
				db = Data(Main.club_name,self.ID)
				id_list = db.read_id('others')
				for item in id_list:
					try:
						await bot.sendMessage(int(item),'<b>ANNOUNCEMENT!!!</b>',parse_mode='HTML')
						await bot.forwardMessage(int(item),self.ID,msg['message_id'])
					except Exception:
						pass
				await self.sender.sendMessage('You have send the announcement to the members.\nSend any message to go back to main menu.')
				self.stage=initial_stage

			# activity setting
			elif self.stage == organize_activity:
				if self.count == 0:
					Main.activity_name=text
					await self.sender.sendMessage(f'The activity name is <b>{text}</b>.',reply_markup = Tools.dynamic_keyboard_1(['Confirm','Reset']),parse_mode = 'HTML')
				elif self.count == 1:
					buff = Tools.msg_processor(text)
					Main.activity_buffer = buff
					text = str(buff)
					item = text.strip("]").replace("[","\n--").replace(",","\n--")
					if len(buff)==1:
						await self.sender.sendMessage(f'The query is <b>{item}</b>.',reply_markup = Tools.dynamic_keyboard_1(['That\'s right.','Reset'])\
											,parse_mode = 'HTML')
					elif len(buff)>1:
						await self.sender.sendMessage(f'The queries are <b>{item}</b>.',reply_markup = Tools.dynamic_keyboard_1(['That\'s right.','Reset'])\
											,parse_mode = 'HTML')
				elif self.count == 2:
					db = Data(Main.club_name,self.ID)
					id_list = db.read_id('others')
					for item in id_list:
						await bot.forwardMessage(int(item),self.ID,msg['message_id'])
					await self.sender.sendMessage('You can continue sending announcements or start providing wiki references by URL.'\
							,reply_markup = Tools.dynamic_keyboard_1(['Start','Activity Setting Completed.']))
				elif self.count == 3:
					try:
						info = wiki(text)
						info_title = wiki_title(str(text))
						db = Data(Main.club_name,self.ID)
						id_list = db.read_id('others')
						for item in id_list:# send the url information to all the members.
							try:
								await bot.sendMessage(int(item),'You may need the following refereces. (Taken from wikipedia)',parse_mode = 'HTML')
								await bot.sendMessage(int(item),"<a href='"+str(text)+"'>"+info_title+"</a>",parse_mode = 'HTML')
								await bot.sendMessage(int(item),f'Here is the brief introduction of <b>{info_title}</b>\n'+info,parse_mode = 'HTML')
							except Exception:
								pass
						await self.sender.sendMessage('You may add more urls.')
						await self.sender.sendMessage('After this step, you may collect the registration stats at certain time.'\
												,reply_markup=Tools.dynamic_keyboard_1(['Activity Setting Completed.']))
					except Exception:
						await self.sender.sendMessage('It is an invalid website. Sorry, but only the wikipedia on PC is allowed for the time being.\n'+\
												'You may try and send a wikipedia URL on your laptop or other devices.'\
												,reply_markup=Tools.dynamic_keyboard_1(['Activity Setting Completed.']))
#########################   EXCOs functions   #########################################
#########################   Group leaders' functions   ################################
		async def _Working_Process_Leaders():# two method are available for group leaders.
			if content_type == 'text':
				text = msg['text']
			if self.stage == initial_stage:
				button = ['View the profile of group members.','send an announcement','Edit profile & Registration']
				await self.sender.sendMessage('Hi! What can I help you with?',reply_markup = Tools.dynamic_keyboard_1(button))
			elif self.stage == make_announcement:
				db = Data(Main.club_name,self.ID)
				gn = tem.dict_reader()['Group_Name']
				name_list = tem.extract_group_member(gn)
				for name in name_list:
					_id = db.dict_reader(name)['ID']
					if int(_id) != self.ID:
						try:
							await bot.sendMessage(int(_id),'<b>ANNOUNCEMENT!!!</b>',parse_mode='HTML')
							await bot.forwardMessage(int(_id),self.ID,msg['message_id'])
						except Exception:
							pass
				await self.sender.sendMessage('You have send the announcement to the group members.\nSend any message to go back to main menu.')
				self.stage=initial_stage
#########################   Group leaders' functions   ################################
#########################   Members' functions   ######################################
		# members' method is available to all
		async def _Working_Process_Members():
			if self.stage == initial_stage:
				db = Data(Main.club_name,self.ID)
				self.Dictprofile = dict(db.dict_reader())
				button = ['Change personal profile']
				position = db.dict_reader()['Hierarchy']
				if position == 'Member':
					button.append('Change group')
				try:
					ac_db = Data(Main.activity_name,self.ID)
					if ac_db.read_id() == '' and Main.activity_step == 1:
						button.append(f'Register the {Main.activity_name}')
				except Exception:
					pass
				if db.read_position() not in Main.Hierarchy_3:
					button.append('Exit "profile editing & registration."')
				await self.sender.sendMessage('HI! What can I help you with?'\
										,reply_markup = Tools.dynamic_keyboard_1(button))
			elif self.stage == edit_info:
				text = msg['text']
				await _Change_Info(text)
			if Main.activity_step == 1:
				text = msg['text']
				if 1<=self.count <= len(Main.activity_buffer):
					await self.sender.sendMessage(f'{self.count}.  {Main.activity_buffer[self.count-1]}')
					if self.count!=1:
						self.query_dict[Main.activity_buffer[self.count-2]] = text
					self.count+=1
				elif self.count == 0:
					pass			
				else:
					if Main.activity_buffer != []:
						self.query_dict[Main.activity_buffer[self.count-2]] = text
						await self.sender.sendMessage('You have answered all the queries.')
					await self.sender.sendMessage('You are to check your own profile.')
					self.count = 0
					time.sleep(2)
					string_profile = Tools.dict_processor(self.Dictprofile)
					for item in string_profile[3:]:
						await self.sender.sendMessage(item)
					await self.sender.sendMessage('Check whether your profile is correct.'\
											,reply_markup = Tools.keyboard(('Yes, the profile is correct.','confirm'),('No, something goes wrong.','wrong')))#

			elif Main.activity_step == 2:
				db = Data(Main.activity_name,self.ID)
				if db.read_id() != '':
					await self.sender.sendMessage(f'Thank you for joining <b>{Main.activity_name}</b>!!! We cannot wait to see you there!!',parse_mode = 'HTML') #
			elif Main.activity_step == 3:
				db = Data(Main.activity_name,self.ID)
				if db.read_id() != '':
					if self.stage != send_feedback:
						fb = db.dict_reader()['Feedback']
						if fb == None:
							await self.sender.sendMessage(f'Hope you have enjoyed <b>{Main.activity_name}</b>!!! Have you sent your feedback?'\
													,reply_markup = Tools.dynamic_keyboard_1(['Send My Feedback Now']),parse_mode='HTML')#
					else:
						text = msg['text']
						dict_buffer = db.dict_reader()
						dict_buffer['Feedback']=text
						db.edit_file(list(dict_buffer.values()))
						await self.sender.sendMessage(f'This is your feedback:\n' + f'{text}.'\
												,reply_markup=Tools.dynamic_keyboard_1(['Confirm', 'Reset']))
#########################   Members' functions   ######################################
#########################   Flow Control  (This bot will not accept information other than text and document)    #########################################
		if self.ID == developer_id: #0#developer tool to restart the bot but keep the data in database.  # my id 439767082
			await self.sender.sendMessage('Developer Tools',reply_markup = Tools.dynamic_keyboard_1(['Retrive Setting files and databases','Deploy Setting files and databases']))
		if content_type=='text' or content_type=='document': # only take these two types of message
			try:# msg['text'] is not always callable. 
				if msg['text']=='/help':
					await self.sender.sendMessage('You can read the document if you are confused.')
					await bot.sendDocument(self.ID,open('Club_Assistant.docx','rb'))
			except Exception:
				pass
			finally:	
				if Main.processing_stage == initial_process:
					await _Initial_Process()
				elif Main.processing_stage == club_setting_process:
					await _Club_Setting_Process()
				elif Main.processing_stage == creator_profile:
					await _Zero_Profile()
				elif Main.processing_stage == working_process or Main.processing_stage == activity_process:
					tem = Data(Main.club_name,self.ID)
					if tem.read_position() in Main.Hierarchy_0+Main.Hierarchy_1:
						if self.info_setting == 0:
							await _Working_Process_Managers()
						else:
							await _Working_Process_Members()
					elif tem.read_position() in Main.Hierarchy_2:
						if self.info_setting == 0:
							await _Working_Process_Leaders()
						else:
							await _Working_Process_Members()
					else:
						if tem.read_id() == '':
							await _Create_Member_Profile()
						else:
							self.Dictprofile = tem.dict_reader()
							await _Working_Process_Members()
		else:
			await self.sender.sendMessage('This approach is not available right now...')
#########################   Flow Control  (This bot will not accept information other than text and document)    #########################################
########################################################################################################################################################################
########################################################################################################################################################################
#########################   Developer TOOLS  ########################################	
	async def on_callback_query(self,msg):
		query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
		if query_data == 'Retrive Setting files and databases':# for program improvement and maintanance
			db = Data('Setting',self.ID)
			db.write_file(['activate'])
			data = \
			Main.club_name,\
			Main.processing_stage ,\
			Main.activity_name ,\
			Main.activity_step ,\
			Main.Dict_group_leaders ,\
			Main.fieldname,\
			Main.Hierarchy_0 ,\
			Main.Hierarchy_1 ,\
			Main.Hierarchy_2 ,\
			Main.Hierarchy_3 ,\
			Main.group_names,\
			Main.activity_buffer ,\
			Main.activity_list
			print(data)
			data = list(data)
			db.write_file(data)
			await bot.sendDocument(self.ID,open('Setting.csv','rb'))
			try:	
				await bot.sendDocument(self.ID,open(Main.club_name+'.csv','rb'))
				for activity in Main.activity_list:
					await bot.sendDocument(self.ID,open(activity+'.csv','rb'))
			except Exception:
				pass
		elif query_data == 'Deploy Setting files and databases':
			try:
				db = Data('Setting',0)
				Main.club_name,\
				Main.processing_stage ,\
				Main.activity_name ,\
				= db.read_file('keys')[:3]
				Main.activity_step = int(db.read_file('keys')[3])
				Main.Dict_group_leaders = ast.literal_eval(db.read_file('keys')[4])
				Main.fieldname = ast.literal_eval(db.read_file('keys')[5])
				Main.Hierarchy_0  = ast.literal_eval(db.read_file('keys')[6])
				Main.Hierarchy_1  = ast.literal_eval(db.read_file('keys')[7])
				Main.Hierarchy_2  = ast.literal_eval(db.read_file('keys')[8])
				Main.Hierarchy_3  = ast.literal_eval(db.read_file('keys')[9])
				Main.group_names = ast.literal_eval(db.read_file('keys')[10])
				Main.activity_buffer  = ast.literal_eval(db.read_file('keys')[11])
				Main.activity_list = ast.literal_eval(db.read_file('keys')[12])
				await self.sender.sendMessage("Restart successfully.")
			except Exception:
				await self.sender.sendMessage("Restart failed.")
		elif query_data == 'Inform the developer to restart.':
			await bot.sendMessage(developer_id,f'0#{self.first_name} requires to restart.')
#########################   Developer TOOLS  ########################################	
#########################   TOOLS #########################################	
		async def _exit_():
			await self.sender.sendMessage('Bye~ Have a nice day.')
			self.stage = 'exit'
		
		# take hierarchy as a parameter
		# if specify the hierarchy the content will be assign to a person
		async def _Confirm_Info(Hierarchy = ''):
			if Hierarchy != '':
				self.Dictprofile['Hierarchy'] = Hierarchy
			found = 0
			profile = []
			for value in self.Dictprofile.values():
				profile.append(value)
			tem = Data(Main.club_name,self.ID)
			if tem.read_id() != '':
				found = 1
			self.database = Data(Main.club_name,str(self.ID))
			if found == 0:
				self.database.append_file(profile)
			else:
				self.database.edit_file(profile)
			print(1)
			self.stage = initial_stage
			self.edit=''

		# set profile accoring to the fieldname specified by the president
		async def _Profile_setting():
			self.count=4
			await bot.answerCallbackQuery(query_id,'Activated.')
			await self.sender.sendMessage(f'Enter your own information into the <b>{Main.club_name}</b> please.',parse_mode = 'HTML')
			await self.sender.sendMessage(f'Let\'s start from... What is your {Main.fieldname[self.count-1]}?')
			self.Dictprofile = {Main.fieldname[0]:str(self.ID),Main.fieldname[1]:'',Main.fieldname[2]:''}

		# the initial stage for all the members
		async def _Create_Member_Profile():
			if self.stage == edit_info:
				self.edit = query_data
				await self.sender.sendMessage(f'What is your <b>{self.edit}</b>',parse_mode = 'HTML')
			if query_data == 'start':
				self.stage = create_member_profile
				await _Profile_setting()
			elif query_data == 'reset':
				self.count-=1
				await self.sender.sendMessage(f'Reenter your {Main.fieldname[self.count-1]}.')
			elif query_data == 'wrong':
				self.stage = edit_info
				await self.sender.sendMessage('Choose the information that you need to change.'\
										,reply_markup = Tools.dynamic_keyboard_2(Main.fieldname[3:]))
			elif query_data == 'confirm':
				await self.sender.sendMessage('Congratulations! Your profile setting is completed.\n'+
								'You will no longer need to resubmit your personal particulars for registration.\n'+
								'You may wait for the EXCOs to organize the next activities to participate in.\n'+
								'You can send your feedback to EXCOs so we will organize better activities for you all.\n'+
								'Thank you for your cooperation. ')
				# await self.sender.sendMessage(f'Hi {self.first_name}, this is the demo version of our bot, you are accessing it as a member. Later, when the developer see your registration, he will change your hierarchy for you!')
				# await self.sender.sendMessage('You may also request the developer to restart the bot from beginning, "the setting up stage for the club".',reply_markup = Tools.dynamic_keyboard_1(['Inform the developer to restart.']))
				await self.sender.sendMessage('Type anything to access the main menu.')
				# await bot.sendMessage(developer_id,f'0#{self.first_name} created his profile.')
				tem = Data(Main.club_name,self.ID)
				line = tem.dict_reader()
				self.count = 0
				self.stage = initial_stage
				await _Confirm_Info(Main.Hierarchy_3[0])
#########################   TOOLS #########################################
#########################   Initial Setting   #########################################
		async def _Initial_Process():
			if query_data=='create' or query_data == 'reset':
				await self.sender.sendMessage('Choose default mode or customized mode.')
				await self.sender.sendMessage('default titles contain: <b>\n{:^s}, {:^s}, {:^s}, {:^s}, {:^s}, {:^s}, {:^s}, {:^s}, {:^s}, {:^s}.\n</b>\
										'.format('Group_name', 'Hierarchy', 'Name','Gender','Phone_number','Matriculation_number','Program','Year',\
										'Email address','Official Email'),reply_markup=Tools.keyboard(('default keywords setting','default')\
																						,('Customize keywords setting','customize'))\
																						,parse_mode = 'HTML')#stage 2 of initialization #
			elif query_data=='reset_0':
				self.count=1
				await bot.answerCallbackQuery(query_id, text='RESETTING...')
			elif query_data=='confirm_0':
				await bot.answerCallbackQuery(query_id, text='Now you may start to create database.')
				await self.sender.sendMessage('You can type anything to activate database settings.\nOr activate later at any time.') #
				self.stage = set_information_database
			elif query_data=='default':
				Main.fieldname = ['ID','Group_Name','Hierarchy','Name','Gender','Phone_Number','Matriculation_Number','Program/Year',
								'Email Address','Official Email']
				self.stage=create_main_database
				await self.sender.sendMessage('Is there any other information you need? Seperate your queries by commas.'\
										,reply_markup=Tools.keyboard(('Reset','reset'),('No need to add more.','complete')))#stage 3 of initialization
			elif query_data == 'customize':
				Main.fieldname = ['ID','Group_Name','Hierarchy','Name','Gender']
				self.stage=create_main_database
				tem = str(Main.fieldname)
				await self.sender.sendMessage('Customized setting still contains criterias for a club database structure.\n'\
										+f'keywords contain \n<b>{tem.strip("[]")}</b> by default.\n'\
										+'You can add more types of information. (seperated by commas)'\
										,reply_markup=Tools.keyboard(('Reset','reset'),('No need to add more.','complete'))\
										,parse_mode = 'HTML')
			elif query_data=='complete':
				tem = str(Main.fieldname)
				await self.sender.sendMessage('Initialized successfully!\nYour keyswords setting includes\n'+\
										f'<b>{tem.strip("[]")}</b>'\
										,reply_markup=Tools.keyboard(('Reset','reset'),('confirm','confirm'))\
										,parse_mode = 'HTML')
			elif query_data == 'confirm':
				self.database = Data(Main.club_name,str(self.ID))
				self.database.write_file(Main.fieldname)
				Main.processing_stage = club_setting_process
				self.stage = initial_stage
				await self.sender.sendMessage(f'You can set up subcommittees and officers for <b>{Main.club_name}</b> now.',reply_markup=Tools.keyboard(('Start Now.','start'),('Exit','exit'))\
										,parse_mode = 'HTML')

		async def _Club_Setting_Process():
			if query_data == 'start':
				await bot.answerCallbackQuery(query_id, text=f'Edit {Main.club_name} information...')
				await self.sender.sendMessage(f'You have already created the database of <b>{Main.club_name}</b>.\n'+
										f'Please indicate all the <b>subgroups</b> in <b>{Main.club_name}</b> and separate them with commas.'\
										,parse_mode = 'HTML')
				await self.sender.sendMessage('eg.Admin & Finance,Outreach,Football team...')
				self.stage = group_name_setting
			elif query_data == 'reset':
				self.count-=1
				await bot.answerCallbackQuery(query_id,'RESETTING...')
			elif query_data == 'exit':
				await self.sender.sendMessage('Bye~ Have a nice day.')
				self.stage = 'exit'
			elif query_data == 'confirm_0':
				await self.sender.sendMessage('Now you can set up the <b>leaders</b> in each subgroup.',parse_mode = 'HTML')
				await self.sender.sendMessage('eg.Vice President, Project director, football team leader')
				await self.sender.sendMessage('Send any message to start.')
				self.count = 0
				self.stage = subcommittee_setting
			elif query_data == 'right' or query_data == 'Reset':
				self.count = 0
				if query_data =='right':
					for item in Main.Dict_group_leaders.values():
						Main.Hierarchy_2.extend(item)
				Main.Hierarchy_2.extend(['Complete'])
				Main.Hierarchy_1=[]
				await self.sender.sendMessage('Click the buttons to assign EXCO who will have access to read the database.'\
										,reply_markup = Tools.dynamic_keyboard_2(Main.Hierarchy_2)) #
				Main.Hierarchy_2.remove('Complete')
				self.stage = maincommittee_setting
			elif query_data =='wrong':
				await self.sender.sendMessage('Send any message to reset.')
				self.count = 0
				Main.Dict_group_leaders=dict()
			elif query_data == 'confirm':
				Main.processing_stage = creator_profile
				self.stage = initial_stage
				await self.sender.sendMessage(f'You can create your own profile now. You will obtain the highest authority in <b>{Main.club_name}</b>'\
										,reply_markup=Tools.keyboard(('Start Now.','start'),('Exit','exit')),parse_mode = 'HTML')
			if self.stage == maincommittee_setting:
				tem = query_data
				if query_data == 'Complete':
					if Main.Hierarchy_1 != []:
						exco = set(Main.Hierarchy_1)
						Main.Hierarchy_1 = list(exco)
						exco = str(exco).strip('{}')
						await self.sender.sendMessage(f'The EXCOs are <b>\'President\',{exco}</b>'\
												,reply_markup = Tools.dynamic_keyboard_1(['Reset','confirm']),parse_mode = 'HTML')
					else:
						await self.sender.sendMessage(f'The EXCO is <b>\'President\'</b>'\
												,reply_markup = Tools.dynamic_keyboard_1(['Reset','confirm']),parse_mode = 'HTML')
				elif query_data in Main.Hierarchy_2:
					Main.Hierarchy_2.remove(tem)
					Main.Hierarchy_1.append(tem)
					await bot.answerCallbackQuery(query_id,f'SET {tem} TO BE THE MANAGER.')

		async def _Zero_Profile():
			if self.stage == edit_info:
				self.edit = query_data
				await self.sender.sendMessage(f'What is your <b>{self.edit}</b>',parse_mode='HTML')
				
			if query_data == 'exit':
				await _exit_()
			elif query_data == 'start':
				self.stage = initial_stage
				await _Profile_setting()
			elif query_data == 'reset':
				self.count-=1
				await self.sender.sendMessage(f'Reenter your {Main.fieldname[self.count-1]}.')
			elif query_data == 'wrong':
				self.stage = edit_info
				await self.sender.sendMessage('Choose the information that you need to change.'\
										,reply_markup = Tools.dynamic_keyboard_2(Main.fieldname[3:]))
			elif query_data == 'confirm':
				await self.sender.sendMessage('Congratulations! All pre-settings are completed.\n'+
										'Now you may instruct the members to add me and create their own profile.\n'+
										'You may also create activities for all members to participate.')
				await self.sender.sendMessage('Type anything to access main menu.')
				print('President profile set')
				self.count = 0
				await _Confirm_Info(Main.Hierarchy_0[0])
				Main.processing_stage = working_process
				self.stage = initial_stage
#########################   Initial Setting   #########################################
#########################   EXCOs functions   #########################################
		async def _Working_Process_Managers():
			if query_data=='Initiate a club activity.':
				Main.processing_stage = activity_process
				await self.sender.sendMessage('Firstly, what\'s the name of the activity?')
				self.stage=organize_activity
				self.count=0
				Main.activity_step = 1
			elif query_data == f'Require {Main.club_name} Database.':
				await self.sender.sendMessage('Do you require to access <b>Main Database</b> or <b>Activity Database</b>?'\
										,reply_markup = Tools.dynamic_keyboard_1([f'Download Main Database of {Main.club_name}','Download Activity Databases'])\
										,parse_mode = 'HTML') #
			elif query_data=='Send an announcement':
				await self.sender.sendMessage('Now you can make your announcement!\nSend documents as references is also available.')
				self.stage=make_announcement
			elif query_data==f'Download Main Database of {Main.club_name}':
				await bot.sendDocument(from_id,open(Main.club_name+'.csv','rb'))
				await self.sender.sendMessage('Here is the maindatabase!\nYou can send any message to go back to main menu.')
				self.stage=initial_stage
			elif query_data=='Download Activity Databases':
				if bool(Main.activity_list)==True:
					await self.sender.sendMessage('Here are the activity databases!',reply_markup=Tools.dynamic_keyboard_1(Main.activity_list))
					await self.sender.sendMessage('You can choose the activity database you need.')
					self.stage=show_activity_database
				else:
					await self.sender.sendMessage('Sorry, you haven\'t organized any activity yet.\nYou can click <b>Initiate a club activity.</b> '+
											'and follow the instructions to organize your first club activity.\n'+\
											'Send any message to return to the main menu!',parse_mode = 'HTML')
					self.stage=initial_stage
			elif query_data==f'Change members\' Hierarchy.':
					db=Data(str(Main.club_name),self.ID)
					tem = Data(Main.club_name,self.ID)
					if tem.read_position() in Main.Hierarchy_0:
						Main.hierarchy_name_list=db.read_name(Main.Hierarchy_0)
					else:
						Main.hierarchy_name_list=db.read_name(Main.Hierarchy_0+Main.Hierarchy_1)
					await self.sender.sendMessage('Whose Hierarchy do you want to change?'\
											,reply_markup=Tools.dynamic_keyboard_2(Main.hierarchy_name_list))
					self.stage=change_hierarchy
			elif query_data == 'Edit profile & Registration':# go to members' method
				self.info_setting = 1
				await self.sender.sendMessage('Send any message to change your profile or register the activity.')
				self.stage = initial_stage
			
			# shared query process
			elif query_data == 'Confirm':
				Main.activity_list.append(Main.activity_name)
				await self.sender.sendMessage('Except the information in the profile, do you have other queries? Seperate them by commas.'\
										,reply_markup = Tools.dynamic_keyboard_1(['No need.']))
				self.count = 1
			elif query_data == 'No need.' or query_data == 'That\'s right.':
				tem = list(Main.fieldname)
				tem.extend(Main.activity_buffer)
				tem.extend(['Feedback'])
				db = Data(Main.activity_name,self.ID)
				db.write_file(list(tem))
				await self.sender.sendMessage('Now you can either copy and paste the email by text.\nOr send specific invitation to the members.\nYou may send documents and files as well.')
				self.count = 2
			elif query_data == 'Reset':
				await bot.answerCallbackQuery(query_id,'RESETTING')
			elif query_data == 'Start':
				self.count = 3
				await bot.answerCallbackQuery(query_id,'Provide the wiki references...')
			elif query_data =='Activity Setting Completed.':
				await self.sender.sendMessage('Activity invitation has been sent to all members!')
				await self.sender.sendMessage('You can send any message to go back to main menu.')
				self.stage = initial_stage
				self.count = 0
			#query at different stages, do not share
			if self.stage==show_activity_database:
				if query_data != 'Download Activity Databases':
					item = query_data
					try:
						await bot.sendDocument(self.ID,open(item+'.csv','rb'))
					except:
						await self.sender.sendMessage('Your query is not passed, something went wrong.') #
					await self.sender.sendMessage('You can send any message to return to the main menu')
					self.stage = initial_stage
			elif self.stage==change_hierarchy:
				if query_data in Main.hierarchy_name_list:
					self.change_name=query_data
					tem = Data(Main.club_name,self.ID)
					position = tem.dict_reader()['Hierarchy']
					await self.sender.sendMessage('Which Hierarchy do you want to assign to him/her?') #
					if position == 'President':
						await self.sender.sendMessage('President: If you want to find someone to replace you.....              '\
												,reply_markup=Tools.dynamic_keyboard_2(Main.Hierarchy_0))
					await self.sender.sendMessage('EXCOs: Who can access the databases and initiate activities.            '\
											,reply_markup=Tools.dynamic_keyboard_2(Main.Hierarchy_1))
					await self.sender.sendMessage('Group Leader: Have access to view members profile and send announcements.'\
											,reply_markup=Tools.dynamic_keyboard_2(Main.Hierarchy_2))#
					await self.sender.sendMessage('Member: The most powerful and important component in a club!!           '\
											,reply_markup=Tools.dynamic_keyboard_2(Main.Hierarchy_3))
				elif query_data == f'Change members\' Hierarchy.':
					pass
				else:
					db=Data(Main.club_name,self.ID)
					alist=db.read_file('values',self.change_name)
					alist[2]=query_data
					for item in Main.Dict_group_leaders.keys():
						if query_data in Main.Dict_group_leaders[item]:
							group = item
							break
						else:
							group = ''
					alist[1] = group
					db.edit_file(alist,object=self.change_name)
					try:
						await bot.sendMessage(int(alist[0]),f'Your Hierarchy has been changed to {query_data}')
					except Exception:
						print('alist[0] = '+alist[0])
						print('unexpected error')
					await bot.answerCallbackQuery(query_id,f'{self.change_name}\'s position changed')
					await self.sender.sendMessage('Send any message to return to the main menu.')
					self.stage=initial_stage
					self.change_name = ''
			#############################   Activity Setting  ############################
			if Main.activity_step == 1 and query_data =='Terminate registration.':
				self.count=0
				self.stage = collect_feedback
				try:
					await bot.sendDocument(self.ID,open(Main.activity_name+'.csv','rb'))
				except Exception:
					pass
				await self.sender.sendMessage('You have terminated the registration, here is the name list of the members who have registered.')
				await self.sender.sendMessage('Send any message to go back to main menu.')
				db1 = Data(Main.club_name,self.ID)
				id_list = db1.read_id('others')
				db2 = Data(Main.activity_name,self.ID)
				ac_list = db2.read_id('others')
				Main.activity_step = 2
				await bot.answerCallbackQuery(query_id,'You have terminated the registration.')
				for item in id_list:
					if item not in ac_list:
						try:
							await bot.sendMessage(int(item),'<b>ANNOUNCEMENT!!!</b>',parse_mode='HTML')
							await bot.sendMessage(int(item),f'Registration is terminated, you will no longer be able to participate in <b>{Main.activity_name}</b>.'+\
													   '\nHave a nice day.',parse_mode='HTML')
						except Exception:
							pass
			elif Main.activity_step == 2 and query_data == 'Start collecting feedback.':
				db = Data(Main.activity_name,self.ID)
				id_list = db.read_id('others')
				for item in id_list:
					try:
						await bot.sendMessage(int(item),'<b>ANNOUNCEMENT!!!</b>',parse_mode='HTML')
						await bot.sendMessage(int(item),f'Did you enjoy the activity? Give us your feedback!'\
												 ,parse_mode='HTML')
					except Exception:
						pass
				await bot.answerCallbackQuery(query_id,'Message Sent.')
				await self.sender.sendMessage('Message has been sent to members, you may send any message to go back to main menu.')
				Main.activity_step = 3
			elif Main.activity_step == 3:
				if query_data == 'Close the activity.':
					await bot.answerCallbackQuery(query_id,'Activity Closed')
					db = Data(Main.activity_name,self.ID)
					id_list = db.read_id('others')
					for item in id_list:
						try:
							await bot.sendMessage(int(item),'<b>ANNOUNCEMENT!!!</b>',parse_mode='HTML')
							await bot.sendMessage(int(item),'The activity is ended. Hope to see you next time!',parse_mode='HTML')
						except Exception:
							pass
						await bot.sendDocument(from_id,open(Main.activity_name+'.csv','rb'))

					await self.sender.sendMessage(f'Here is the database of all the registered member in {Main.activity_name}')
					await self.sender.sendMessage('Send any message to go back to main menu.')
					Main.activity_name = ''
					Main.activity_buffer = []
					db = Data(Main.activity_name,self.ID)
					Main.processing_stage = working_process
					Main.activity_step = 0
				elif query_data == 'View the feedback' or query_data == 'Next':
					db1 = Data(Main.activity_name, self.ID)
					actmember_namelist = db1.read_name()
					try:
						fb = db1.dict_reader(actmember_namelist[self.count])
						if fb['Feedback'] != None:
							await self.sender.sendMessage(f"{fb['Name']}:\n{fb['Feedback']}",reply_markup =Tools.dynamic_keyboard_1(['Next','Close the activity.']))
							self.count += 1
						else:
							self.count+=1
					except Exception:
						await self.sender.sendMessage('All the feedback has been sent'\
														,reply_markup=Tools.dynamic_keyboard_1(['Close the activity.']))
						self.count = 0
			#############################   Activity Setting  ############################
#########################   EXCOs functions   #########################################
#########################   Group leaders' functions   ################################
		async def _Working_Process_Leaders():
			if query_data == 'View the profile of group members.':
				tem = Data(Main.club_name,self.ID)
				gn = tem.dict_reader()['Group_Name']
				try:
					button = tem.extract_group_member(gn)
					await self.sender.sendMessage('Whose profile do you need?',reply_markup = Tools.dynamic_keyboard_2(button))
				except Exception:
					await self.sender.sendMessage('Sorry, there is no one in your group now...')
			elif query_data == 'send an announcement':
				await self.sender.sendMessage('Now you can send your announcement!')
				self.stage=make_announcement
			elif query_data == 'Edit profile & Registration':# go to members' method
				self.info_setting = 1
				await self.sender.sendMessage('Send any message to change self information or register.')
				self.stage = initial_stage
			else:
				try:	
					tem = Data(Main.club_name,self.ID)
					dict_file = dict(tem.dict_reader(query_data))
					string_profile = Tools.dict_processor(dict_file)
					for item in string_profile[1:]:
						await self.sender.sendMessage(item)
				except Exception:
					print('error')
#########################   Group leaders' functions   ################################	
#########################   Members' functions   ######################################
		async def _Working_Process_Members():
			if self.stage == edit_info:
				self.edit = query_data
				await self.sender.sendMessage(f'What is your <b>{self.edit}</b>',parse_mode = 'HTML')
			elif self.stage == change_group:
				db=Data(Main.club_name,self.ID)
				profile=db.dict_reader()
				profile['Group_Name'] = query_data
				tem = []
				for value in profile.values():
					tem.append(value)
				db.edit_file(tem)
				await bot.answerCallbackQuery(query_id,'Your group has changed')
				await self.sender.sendMessage('Send any message to return to the main menu.')
				self.stage = initial_stage
			if query_data == 'wrong' or query_data == 'Change personal profile':
				self.stage = edit_info
				await self.sender.sendMessage('Choose the information that you need to change.',reply_markup = Tools.dynamic_keyboard_2(Main.fieldname[3:]))
			elif query_data == 'confirm':
				if Main.activity_step == 0:
					await self.sender.sendMessage('Your profile setting has been changed. You can send any message to go back to main menu.')
				self.count = 0
				self.stage = initial_stage
				await _Confirm_Info()
			elif query_data == 'Exit "profile editing & registration."':
				self.info_setting = 0
				await bot.answerCallbackQuery(query_id,'Back to main menu.')
				self.stage = initial_stage
			elif query_data == 'Change group':
				db = Data(Main.club_name,self.ID)
				gn = db.dict_reader()['Group_Name']
				if gn == '':
					await self.sender.sendMessage('You have not joined a group yet')
				else:
					await self.sender.sendMessage(f'You are currently in the group of {gn}.')
				await self.sender.sendMessage('If you want to change your group, which group would you like to join?'\
										,reply_markup = Tools.dynamic_keyboard_2(Main.group_names))
				self.stage = change_group
			if Main.activity_step==1:
				if query_data==f'Register the {Main.activity_name}':
					if Main.activity_buffer != []:
						await self.sender.sendMessage('You are required to answer the following questions. Send any message to start.')
					else:
						await self.sender.sendMessage('No other queries are needed. Send any message to continue.')
					self.count=1
					self.stage = query_stage
				if query_data == 'confirm':
					db1 = Data(Main.club_name,self.ID)
					me = db1.read_file('personal value')
					for value in self.query_dict.values():
						me.append(value)
					db2 = Data(Main.activity_name,self.ID)
					db2.append_file(me)
					await self.sender.sendMessage('Your registration has been saved successfully! See you then!!!')
					await self.sender.sendMessage('Now you can send any message to go back to main menu.')
			if Main.activity_step == 3:
				if query_data == 'Send My Feedback Now':
					await bot.answerCallbackQuery(query_id,'Send the message when you are ready.')
					self.stage = send_feedback
				elif query_data == 'Confirm':
					await self.sender.sendMessage('Your feedback has been saved successfully! Hope to see you in the next activity!')
					self.stage = initial_stage
					self.feedback = 1
				elif query_data == 'Reset':
					self.stage = send_feedback
					await self.sender.sendMessage('You can send your feedback again.')
#########################   Members' functions   ######################################
#########################   Flow Control      #########################################
		if Main.processing_stage == initial_process:
			await _Initial_Process()
		elif Main.processing_stage == club_setting_process:
			await _Club_Setting_Process()
		elif Main.processing_stage == creator_profile:
			await _Zero_Profile()
		elif Main.processing_stage == working_process or Main.processing_stage == activity_process:
			tem = Data(Main.club_name,self.ID)
			if tem.read_position() in Main.Hierarchy_0+Main.Hierarchy_1:
				if self.info_setting == 0:
					await _Working_Process_Managers()
				else:
					await _Working_Process_Members()
			elif tem.read_position() in Main.Hierarchy_2:
				if self.info_setting == 0:
					await _Working_Process_Leaders()
				else:
					await _Working_Process_Members()
			else:
				if tem.read_id() == '':
					await _Create_Member_Profile()
				else:
					await _Working_Process_Members()
#########################   Flow Control      #########################################

	async def on__idle(self,event):# restart of the program, avoid on_close function.
		print("idle called")

#########################   Main Function     #########################################
developer_id = 0#439767082
TOKEN = '392540312:AAERhaHdBOZtBLtpwFplIAZthtu-KpJRs04'
bot = telepot.aio.DelegatorBot(TOKEN, [
	include_callback_query_chat_id(pave_event_space())
	(per_chat_id(types = 'private'), create_open, Main,timeout=60*60*2)])# 1. this bot is not meant for group or channel 2. bot stage will return back to initial stage if no request for two hours.
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('bot is waiting for instruction')
loop.run_forever()
#########################   Main Function     #########################################
