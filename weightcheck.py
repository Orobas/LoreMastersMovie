from __future__ import division
import time, os, re, sys


#IDEAS:
#Get list of all words from unmatched words, count them and show positive/negative count and overall score count
#Get score count of all words from unmatched words
#Get accuracy count of all words that are matched, check score of hits, misses and total number of times that words show update





dict = dict()
scoredict = {}
nomatchdict = {}
phraselist = {}
neglist = []
mismatchwords = []
linesmissed = []
poswords = {}
negwords = {}
totalwords = {}
totaluse = {}
true = 0
linescore = 0
false = 0
nomatch = 0
linenum = -1
printout=False
if len(sys.argv)==2:
	printout=True
#with open("SelfTrainingWords.tsv") as train:
with open("SelfTrainingWordsWeighted.tsv") as train:
	next(train)
	for lines in train:
		line = lines.split("\t")
		dict[line[0]] = line[1]

with open("negative.tsv") as negative:
	next(negative)
	for lines in negative:
		lines = lines.split("\n")
		neglist.append(lines[0])

with open("phrases.tsv") as phrases:
	next(phrases)
	for lines in phrases:
		line = lines.split("\t")
		phrase = line[1].split(' ')
		keyword = phrase[0]
		phraselist[keyword]=""
		for word in phrase[1:]:
			word = word.translate(None, "\n")
			phraselist[keyword] = phraselist[keyword] + word + " "
		phraselist[keyword] = phraselist[keyword] + line[0]	
	#print(phraselist)
		
def clean( word ):
	wordsplit = re.split(r'[.?!,;]+', word)
	if len(wordsplit) > 1:
		word=wordsplit[0]
		end = True
	word = word.translate(None, '\".!></()?@,\\\';:+-*#$`')
	word = word.lower()
	return word
		
with open("TrainDataset.tsv") as f:
#with open("specifictraindata.tsv") as f:
	next(f)
	curskip = 0
	skiptil = 0
	for lines in f:
		line = lines.split("\t",2)
		linescore = int(line[1])
		if linescore==0: linescore=-1
		score=0
		match=False
		words = line[2].split()
		neg = False
		end = False
		phrasebool = False
		matches = []		
		for index, word in enumerate(words):
			linenum=linenum+1;
			#print index
			if skiptil > 0:
				if curskip < skiptil:
					curskip = curskip + 1
					continue
				else:
					skiptil = 0
					continue
			wordsplit = re.split(r'[.?!,;]+', word)
			#wordsplit=word.split('.|?|!|/;')
			phrasebool = False
			if len(wordsplit) > 1:
				word=wordsplit[0]
				end = True
			word = word.translate(None, '\".!></()?@,\\\';:+-*#$`')
			word = word.lower()
			
			#print word + "~"
			#we have word now
			if word in dict:
				if linescore==1:
					if word in poswords:
						poswords[word]=poswords[word] + 1
					else:
						poswords[word]=1
				else:
					if word in negwords:
						negwords[word]=negwords[word] + 1
					else:
						negwords[word]=1
				if word in totalwords:
					totalwords[word]=totalwords[word] + linescore
				else:
					totalwords[word]=linescore
				if word in totaluse:
					totaluse[word]=totaluse[word] + 1
				else:
					totaluse[word]=1
	for key in totalwords:
		if key not in poswords:
			poswords[key]=0
		if key not in negwords:
			negwords[key]=0
#	os.remove("UnmatchedData.tsv")
#except OSError:
#	pass

with open("WeightedAverageWords.tsv","w") as write:
		write.write("word\tvalue\n")
		for key in totalwords:
			avg = 0
			if totalwords[key]>0:
				weight = 1
				avg = poswords[key]/totaluse[key]*100
				if avg >= 50: weight = 2
				if avg >= 60: weight = 3
				if avg >= 70: weight = 4
				if avg >= 80: weight = 5
				if avg >= 90: weight = 6
				write.write(key + "\t" + str(weight) + "\t" + str(avg) + "\n")
			else:
				weight = -1
				avg = negwords[key]/totaluse[key]*100
				if avg >= 50: weight = -2
				if avg >= 40: weight = -3
				if avg >= 60: weight = -4
				if avg >= 80: weight = -5
				if avg >= 90: weight = -6
				write.write(key + "\t" + str(weight) + "\t" + str(avg) + "\n")
		write.close()

#with open("LeftoverWords.tsv") as read:
	#next(read)
	#for lines in read:
		
		
#with open("SubmissionData.csv","w") as write:
	#write.write("document_id,sentiment\n")
	#for key in scoredict:
		#word = key.translate(None, '\"')
		#write.write(word+","+str(scoredict[key])+"\n")