#-*- coding: utf-8 -*-
import telepot
import requests
import markovify
import threading

def question():
	with open('/Users/macbookpro/PycharmProjects/untitled/questions.txt', 'r') as quests:
		questions = quests.read()
	with open('/Users/macbookpro/PycharmProjects/untitled/bodies.txt', 'r') as bods:
		bodies = bods.read()

	lang_model_q = markovify.Text(questions)
	lang_model_b = markovify.Text(bodies)

	rez = lang_model_b.make_sentence()
	rez_2 = lang_model_q.make_sentence()
	rez_3 = rez + rez_2

	return lang_model_b.make_sentence()

def writer(x, event_queue, event_set):
	for i in range(10):
		event_queue.wait()
		event_queue.clear()
		print(x)
		event_set.set()

token = '788912243:AAHoqgcjX8Oqz04Z1ndGAl3JPBZl7ePKgFc'
print('Start')

bot = telepot.Bot(token)

def reply(text, chat_id):
	if '/question' in text:
		bot.sendMessage(chat_id, question())
	else:
		bot.sendMessage(chat_id, '¯\_(ツ)_/¯')

print('Bot is ready')

update_id = 0

while True:
	updates = bot.getUpdates(offset = update_id + 1)
	for update in updates:
		if update['update_id'] > update_id:
			update_id = update['update_id']
			reply(update['message']['text'], update['message']['chat']['id'])