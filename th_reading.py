#-*- coding: utf-8 -*-
import threading
import markovify
import time
import uuid
import os
import telepot
import requests


lang_model_q = None
lang_model_b = None

path = '/Users/macbookpro/questions/'

def generate_models():
	global lang_model_b
	global lang_model_q
	temp = []
	with open(
		'/Users/macbookpro/PycharmProjects/untitled/questions.txt', 'r'
	) as quests:
		questions = quests.read()
	with open(
		'/Users/macbookpro/PycharmProjects/untitled/bodies.txt', 'r'
	) as bods:
		bodies = bods.read()

	lang_model_q = markovify.Text(questions)
	lang_model_b = markovify.Text(bodies)

def question():
	return (
		lang_model_b.make_sentence() + ' ' + lang_model_q.make_sentence() + '\n'
	)

def generate_n_questions(n):
	for _ in range(n):
		name = 'questions/' + str(uuid.uuid4()) + '.txt'
		with open(name, 'w') as f:
			f.write(question())

def checker():
	filelist = os.listdir(path)
	if len(filelist) >= 100:
		pass
	else:
		num = 100 - len(filelist) 
		generate_n_questions(num)

def bgthread():
	while True:
		checker()
		time.sleep(60)

def thr():
	generate_models()
	t = threading.Thread(target = bgthread)
	t.start()

def picker():
	filelist = os.listdir(path)
	with open(path + filelist[0], 'r') as firstfile:
		f = firstfile.read()
	os.remove(path + filelist[0])
	return f

token = '788912243:AAHoqgcjX8Oqz04Z1ndGAl3JPBZl7ePKgFc'
print('Start')

bot = telepot.Bot(token)

def reply(text, chat_id):
	if '/question' in text:
		bot.sendMessage(chat_id, picker())
	else:
		bot.sendMessage(chat_id, '¯\_(ツ)_/¯')

print('Bot is ready')

update_id = 0

thr()

while True:
	updates = bot.getUpdates(offset = update_id + 1)
	for update in updates:
		if update['update_id'] > update_id:
			update_id = update['update_id']
			reply(update['message']['text'], update['message']['chat']['id'])