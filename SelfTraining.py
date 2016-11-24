from __future__ import division
import time, os

dict = dict()
scoredict = {}
nomatchdict = {}
neglist = []
true = 0
false = 0
nomatch = 0
with open("SelfTrainingWords.tsv") as train:
	next(train)
	for lines in train:
		line = lines.split("\t")
		dict[line[0]] = line[1]

with open("negative.tsv") as negative:
	next(negative)
	for lines in negative:
		neglist.append(lines)
		
with open("TrainDataset.tsv") as f:
	next(f)
	for lines in f:
		line = lines.split("\t",2)
		score=0
		match=False
		words = line[2].split()
		neg = False
		for word in words:
			wordsplit=word.split(".?!;")
			if len(wordsplit) > 1:
				word=wordsplit[0]
			word = word.translate(None, '\".!></()?@,\\\';:+-*#$`')
			word = word.lower()
			if word in neglist:
				neg = True
				continue
			if word in dict:
				match=True
				#print dict[word]
				wordscore = int(dict[word])
				#print(wordscore)
				if wordscore==0: wordscore=-1
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
					score = score - 1
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
					score = score + 1
				#time.sleep(.5)
		#print score
		#time.sleep(.5)
		if match==False:
			#print("No match")
			nomatchdict[nomatch] = line[1],line[2]
			nomatch = nomatch + 1
			continue
		if score < 0: 	
			scoredict[line[0]] = 0
		else:
			scoredict[line[0]] = 1
		if scoredict[line[0]]==int(line[1]):
			true = true + 1
		else:
			false = false + 1
			#print("Score: " + str(score))
			#print(line[2])

print("Correct classifications: " + str(true))
print("False classifications: " + str(false))
print("No match: " + str(nomatch))
print("Percentage: {0:.0f}%".format(true/25000*100))		
try:
	os.remove("UnmatchedData.tsv")
except OSError:
	pass

with open("UnmatchedData.tsv","w") as write:
		write.write("sentiment\twords\n")
		for key in nomatchdict:
			write.write(nomatchdict[key][0] + "\t" + nomatchdict[key][1])
			
			
			
			
			
			
#with open("SubmissionData.csv","w") as write:
	#write.write("document_id,sentiment\n")
	#for key in scoredict:
		#word = key.translate(None, '\"')
		#write.write(word+","+str(scoredict[key])+"\n")