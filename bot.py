import urllib.request
import requests
import vk_api
import re
import datetime
from random import randint
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


settings = open("bot_settings.txt", "r", encoding="UTF-8").read()
token = re.findall(r"token *= *([a-zA-Z0-9]*)[ ,\t]*[\n,#]", settings)[0]
public_id = int(re.findall(r"public_id *= *([0-9]*)[ ,\t]*[\n,#]", settings)[0])
MODERS_CHAT_ID = int(re.findall(r"moderators_chat_id *= *([0-9]*)[ ,\t]*[\n,#]", settings)[0])
DB_NAME = re.findall(r"database_file *= *([a-zA-Z0-9._-]*)[ ,\t]*[\n,#]", settings)[0]
ACCEPT_LEVEL = float(re.findall(r"accept_level *= *([0-9.,]*)[ ,\t]*[\n,#]", settings)[0])



DATABASE = 0

CONTEXT = {}
UNANSWERED = {}



def makeLog(error):
    log = open("errors.log", "a", encoding="UTF-8")
    log.write("(" + str(datetime.datetime.now()) + ") Error occured: " + str(error) + "\n")
    log.close()



def writeMsg(peer_id, message, keyboard = "", keyboard_prepared = False):
    try:
        if message != "" and keyboard == "":
            answ = vk_api.messages.send(peer_id=peer_id, message=message, random_id=randint(0, 999999999))
        if message != "" and keyboard != "":
        	if not keyboard_prepared:
        		answ = vk_api.messages.send(peer_id=peer_id, message=message, keyboard=open(keyboard, "r", encoding="UTF-8").read(), random_id=randint(0, 999999999))
        	else:
        		answ = vk_api.messages.send(peer_id=peer_id, message=message, keyboard=keyboard, random_id=randint(0, 999999999))
        else:
        	answ = -2
        return answ
    except:
        makeLog("failed sending \"" + message + "\" to " + str(peer_id))
        return -1




def readDatabase(filename):
	global DATABASE
	db_file = open(filename, "r", encoding = "UTF-8")
	DATABASE = db_file.read()
	DATABASE = re.findall(r"Q: (.*)\nA: (.*)\n", DATABASE)
	
	
	
def writeDatabase(filename):
	db_file = open(filename, "w", encoding = "UTF-8")
	for couple in DATABASE:
		db_file.write("Q: " + couple[0].capitalize() + "\n")
		db_file.write("A: " + couple[1].capitalize() + "\n\n")
	db_file.close()
	
	

def callModers(text, peer_id):
	UNANSWERED[text] = peer_id
	writeMsg(2000000000 + MODERS_CHAT_ID, "⚠ Вопрос от абитуриента " + whoIs(peer_id) + ":\n" + text)



def makeResponce(peer_id, text, event):
	global DATABASE
	
	answer = ""
	keyboard = ""

	if peer_id < 2000000000:
		if peer_id in CONTEXT:
			if text.lower() == "да":
				answer = "Отлично, можете задать еще вопросы"
				CONTEXT.pop(peer_id)
			elif text.lower() == "нет":
				answer = "Хорошо, я переслал вопрос модераторам и они ответят в ближайшее время.\nА пока вы можете задать еще вопросы или узнать интересные факты о факультете."
				callModers(CONTEXT[peer_id], peer_id)
				CONTEXT.pop(peer_id)
			else:
				CONTEXT.pop(peer_id)
				makeResponce(peer_id, text, event)
				
		else:
			CONTEXT[peer_id] = text
			
			for question in DATABASE:
				if compare(question[0], text) > ACCEPT_LEVEL:
					answer += "В: " + question[0] + "\nO: " + question[1] + "\n\n"
					
			if len(answer) != 0:
				answer = "Схожие вопросы:\n\n" + answer + "Вам помогла данная информация?"
				keyboard = "sucess_answer.json"
			else:
				answer = "Похоже, в базе данных нет ответа на этот вопрос, я переадресую его модераторам и они ответят вам в ближайшее время"
				callModers(text, peer_id)
				
	else:
		if "reply_message" in event.object.message:
			reply_to = event.object.message["reply_message"]
			if reply_to["from_id"] == -public_id:
				if text.lower() in ["\ignore", "игнор", "ignore"]:
					writeMsg(UNANSWERED[(reply_to["text"]).split("\n")[1]], "⚠ Модератор счел вопрос неуместным и/или не относящимся к факультету")
					UNANSWERED.pop((reply_to["text"]).split("\n")[1])
					answer = "Вопрос проигнорирован."
				
				else:
					writeMsg(UNANSWERED[(reply_to["text"]).split("\n")[1]], "⚠ Ответ модератора " + whoIs(event.object.message["from_id"]) + ":\n" + text)
					DATABASE += [((reply_to["text"]).split("\n")[1], text)]
					writeDatabase(DB_NAME)
					UNANSWERED.pop((reply_to["text"]).split("\n")[1])
					answer = "Ответ на вопрос выслан абитуриенту и занесен в базу."
			
	writeMsg(peer_id, answer, keyboard)
	
			
			
def compare(template, message):
	template_sep = template.split()
	message_sep = message.split()
	message_len = 0
	coincidence_len = 0
	for word in message_sep:
		message_len += len(word)
		if word.lower() in template.lower():
			coincidence_len += len(word)
			
	answer1 = coincidence_len/message_len
	
	template_len = 0
	coincidence_len = 0
	for word in template_sep:
		template_len += len(word)
		if word.lower() in message.lower():
			coincidence_len += len(word)
			
	answer2 = coincidence_len/template_len
	
	return max(answer1, answer2)



def whoIs(user_id, sex = False):
    user = (vk_session.method('users.get', {'user_ids':user_id, 'fields':['sex']}))[0]
    if sex: return ["@id" + str(user_id) + " (" + user['first_name'] + " " + user['last_name'] + ")", user['sex'] - 1]
    else: return "@id" + str(user_id) + " (" + user['first_name'] + " " + user['last_name'] + ")"



if __name__ == '__main__':

	readDatabase(DB_NAME)

	vk_session = vk_api.VkApi(token = token)
	vk_session._auth_token()
	vk_api = vk_session.get_api()
	while(True):
		try:
			longpoll = VkBotLongPoll(vk_session, public_id)
			for event in longpoll.listen():
				if event.type == VkBotEventType.MESSAGE_NEW:
					text = event.object.message["text"]
					peer_id = event.object.message["peer_id"]
					makeResponce(peer_id, text, event)
		except Exception as error:
			makeLog(error)
			continue
