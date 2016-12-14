from __future__ import division
import time, os, re, sys


#IDEAS:
#Get list of all words from unmatched words, count them and show positive/negative count and overall score count
#Get score count of all words from unmatched words
#Get accuracy count of all words that are matched, check score of hits, misses and total number of times that words show update
#Try with a list of stop words, get from online?




dict = dict()
scoredict = {}
nomatchdict = {}
phraselist = {}
neglist = []
mismatchwords = []
linesmissed = []
true = 0
false = 0
nomatch = 0
linenum = -1
printout=False
if len(sys.argv)==2:
	printout=True
#with open("SelfTrainingWords.tsv") as train:
#with open("SelfTrainingWordsWeighted.tsv") as train:
with open("WeightedAverageWords.tsv") as train:
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
			if word in phraselist:
				wordsinphrase = phraselist[word].split()
				for x in xrange(0,len(wordsinphrase)):
					neg = False
					try:
						nextword = clean(words[index+x+1])
					except:
						break
					if x == len(wordsinphrase)-1:
						wordscore = int(wordsinphrase[len(wordsinphrase)-1])
						skiptil = len(wordsinphrase)-1
						curskip = 1
						phrasebool = True
						matches.append("Phrase: " + word + " " + str(wordscore))
						break
					if nextword != wordsinphrase[x]: break
					
			if word in neglist and phrasebool == False:
				neg = True
				#print "NEG FOUND!"
				continue
			if word in dict or phrasebool == True:
				match=True
				#print dict[word]
				if phrasebool == False:
					wordscore = int(dict[word])
					if neg == True:
						matches.append("Neg " + word + " " + str(wordscore))
						#print("Neg " + word + " " + str(wordscore))
					else:
						matches.append(word + " " + str(wordscore))
						#print(word + " " + str(wordscore))
				#print(wordscore)
				if neg == True: 
					wordscore = -wordscore
					neg = False
				if wordscore < 0:
					#print("minus")
					#if wordscore<-10000:
					#	score = score - 1
					#if wordscore<-1000:
						#score = score -1
					#if wordscore<-100:
						#score = score - 1
					#if wordscore<-10:
						#score = score - 1
					score = score + wordscore
				else:
					#print("plus")
					#if wordscore>10000:
						#score = score + 1
					#if wordscore>1000:
						#score = score + 1
					#if wordscore>100:
						#score = score + 1
					#if wordscore>10:
						#score = score + 1
					score = score + wordscore
				#time.sleep(.5)
			if end == True: 
				neg = False	
				end = False
		#print score
		#time.sleep(.5)
		if match==False:
			#print("No match")
			linesmissed.append(linenum);
			nomatchdict[nomatch] = line[0],line[1],line[2]
			nomatch = nomatch + 1
			#continue
		if score < 0: 	
			scoredict[line[0]] = 0
		else:
			scoredict[line[0]] = 1
		if int(line[1])==1:
			if scoredict[line[0]]==1:
				true = true + 1
			else:
				false = false + 1
				for word in matches:
					word = word.split()
					if int(word[len(word)-1]) < 0:
						mismatchwords.append(word[0])
				if printout==True:
					print(line[2])
					raw_input("Continue...")
		else:
			if scoredict[line[0]]==0:
				true = true + 1
			else:
				false = false + 1
				for word in matches:
					word = word.split()
					if int(word[len(word)-1]) > 0:
						mismatchwords.append(word[0])
				if printout==True:
					print(line[2])
					raw_input("Continue...")
		#if scoredict[line[0]]==int(line[1]):
			#true = true + 1
		#else:
			#false = false + 1
			#if printout==True: 
				#print("Score: " + str(score))
				#print("Words: ")
			#for word in matches:
				#word = word.split()
				#mismatchwords.append(word[0])
				#if printout == True:	print word
			#if printout==True:
				#print(line[2])
				#raw_input("Continue...")

print("Correct classifications: " + str(true))
print("False classifications: " + str(false))
print("No match: " + str(nomatch))
print("Percentage: {0:.0f}%".format(true/25000*100))		
#try:
#	os.remove("UnmatchedData.tsv")
#except OSError:
#	pass

with open("UnmatchedData.tsv","w") as write:
		write.write("id\tsentiment\twords\n")
		for key in nomatchdict:
			write.write(nomatchdict[key][0] + "\t" + nomatchdict[key][1] + "\t" + nomatchdict[key][2])
			
#with open("CorrectWords.tsv","w") as write:
		#write.write("words")
		#for words in dict:
			#print words
			#if words in mismatchwords:
				#print "incorrect word: " + words
				#continue
			#else:
				#write.write(words)
				
with open("SubmissionData.csv","w") as write:
	write.write("document_id,sentiment\n")
	for key in scoredict:
		word = key.translate(None, '\"')
		write.write(word+","+str(scoredict[key])+"\n")			
			
			
#with open("SubmissionData.csv","w") as write:
	#write.write("document_id,sentiment\n")
	#for key in scoredict:
		#word = key.translate(None, '\"')
		#write.write(word+","+str(scoredict[key])+"\n")