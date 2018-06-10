from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
from fuzzywuzzy import fuzz
import nltk
from nltk import *
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
import unirest
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string

from uclassify import uclassify
from django.views.decorators.csrf import csrf_exempt
import json

import logging



def general_coversational_bot(question):
	bot=ChatBot('Bot')
	bot.set_trainer(ListTrainer)

	# for _file in os.listdir('/home/pavan/Desktop/Chatbot/Chatbot/Web_Chatbot/templates/Conversation'):
	#	data=open('/home/pavan/Desktop/Chatbot/Chatbot/Web_Chatbot/templates/Conversation/' + _file,'r').readlines()
	#	bot.train(data)

	if question.strip() != 'Bye':
			reply = bot.get_response(question)
	if question.strip() == 'Bye':
			reply = 'Bye'
	return reply

def paragraph_devide_and_compare(question_keywords, answer):
	ans = answer.split(".")
	return compare_sentences(question_keywords, ans)


def answer_summerizer(answer):
	response = unirest.post("https://textanalysis-text-summarization.p.mashape.com/text-summarizer-text",
		headers={
			"X-Mashape-Key": "QtN3LJIP6lmsh5BbW50SZIiKAfVTp1FkomLjsnJvKRw0dRVhuE",
			"Content-Type": "application/x-www-form-urlencoded",
			"Accept": "application/json"
			},
		params={
			"sentnum": 3,
			"text": answer
			}
	)
	try:
		output = response.body['sentences'][0] + response.body['sentences'][1] + response.body['sentences'][2]
	except:
		output = "I dont know"
	return output

def compare_sentences(question_keywords, file_content):
	res = 0
	answer = ""
	for line in file_content:
		ans = keyword_extractor(line)
		# toks = nltk.regexp_tokenize(line, sentence_re)
		# postoks = nltk.tag.pos_tag(toks)
		# new_tree = chunker.parse(postoks)
		# new_terms = get_terms(new_tree)
		# ans = ""
		# for new_term in new_terms:
		# 	for word in new_term:
		# 		ans = ans + " " + word

		stopword = nltk.corpus.stopwords.words('english')
		stopword.extend(string.punctuation)
		stopword.append('')

			# Create tokenizer and stemmer
		tokenizer = nltk.tokenize.punkt.PunktWordTokenizer()
			


		tokens_a = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(ans) \
						if token.lower().strip(string.punctuation) not in stopword]
		tokens_b = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(question_keywords) \
						if token.lower().strip(string.punctuation) not in stopword]

					# Calculate Jaccard similarity
		ratio = len(set(tokens_a).intersection(tokens_b)) / float(len(set(tokens_a).union(tokens_b)))
		


	
		if (ratio>res):
			res = ratio
			answer = line
	return answer
	

def legal_conversational_bot(question_keywords):
	print question_keywords
	file = open("C:\\Users\\Rahul\\Desktop\\input.txt","r")
	file_content = file.read()
	file_content = file_content.split("\n")
	answer = compare_sentences(question_keywords, file_content)
	
	#reply = answer_summerizer(answer)
	reply = paragraph_devide_and_compare(question_keywords, answer)	
	file.close()
	return reply

def keyword_extractor(content):
	sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
	lemmatizer = nltk.WordNetLemmatizer()
	stemmer = PorterStemmer()

	grammar = r"""
		NBAR:
		# Nouns and Adjectives, terminated with Nouns
		{<NN.*|JJ>*<NN.*>}

		NP:
		{<NBAR>}
		# Above, connected with in/of/etc...
		{<NBAR><IN><NBAR>}
	"""
	chunker = nltk.RegexpParser(grammar)
	toks = nltk.regexp_tokenize(content, sentence_re)
	postoks = nltk.tag.pos_tag(toks)
	tree = chunker.parse(postoks)
	stopword = stopwords.words('english')
	stopwords1 = [".",",",";","'s","-"]




	def leaves(tree):
		"""Finds NP (nounphrase) leaf nodes of a chunk tree."""
		for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
			yield subtree.leaves()


	def normalise(word):
		"""Normalises words to lowercase and stems and lemmatizes it."""
		word = word.lower()
		word = stemmer.stem(word)
		word = lemmatizer.lemmatize(word)
		return word

	def acceptable_word(word):
		"""Checks conditions for acceptable word: length, stopword."""
		accepted = bool(2 <= len(word) <= 40
			and word.lower() not in stopword and word.lower() not in stopwords1)
		return accepted

	def get_terms(tree):
		for leaf in leaves(tree):
			term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
			yield term


	terms = get_terms(tree)
	keywords = ""
	for term in terms:
		for word in term:
			keywords = keywords + " " + word

	return keywords




def classify(keywords):
	
	# file = open('/home/pavan/Desktop/py/english/greetings.yml')
	# lines = file.readlines()
	# lineList = []
	# for line in lines:
	# 	temp = line.rstrip("\n")
	# 	lineList.append(temp.lstrip("- "))


	# fileLegal = open("/home/pavan/Desktop/py/law_words","r")
	# linesLegal = fileLegal.readlines()
	# lineLegalList = []
	# for line in linesLegal:
	# 	lineLegalList.append(line.rstrip("\n"))

	keyword_classifier = uclassify()
	keyword_classifier.setWriteApiKey("DDmXKJDNomia")
	keyword_classifier.setReadApiKey("xFA156CyIuFl")

	# keyword_classifier.create("GeneralorLegal2") 
	# keyword_classifier.addClass(["General","Legal"],"GeneralorLegal2") 

	# keyword_classifier.train(lineList,"General","GeneralorLegal2")
	# keyword_classifier.train(lineLegalList,"Legal","GeneralorLegal2")
	legal_or_general = (keyword_classifier.classify([keywords],"GeneralorLegal2"))[0][2]
	if legal_or_general[0][1] >= legal_or_general[1][1]:
		return "genaral"
	else:
		return "legal"

@csrf_exempt
def response(request):
	postData = request.POST
	message = postData.get('data[msg]')
	keywords = keyword_extractor(message)
	print "keyword " + keywords
	logger = logging.getLogger('testlogger')
	logger.info('This is a simple log message')

	if classify(keywords) == "genaral":
		reply = general_coversational_bot(message)
	else :
		reply = legal_conversational_bot(keywords)
	reply = str(reply)
	data = json.dumps({"reply": reply })
	return HttpResponse(data,  content_type='application/json')
