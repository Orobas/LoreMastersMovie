import time, os
dict = dict()
scoredict = {}
neglist = []
with open("SelfTrainingWords.tsv") as train:
	next(train)
	for lines in train:
		line = lines.split("\t")
		dict[line[0]] = line[1]

with open("negative.tsv") as negative:
	next(negative)
	for lines in negative:
		neglist.append(lines)
		
with open("TestDataset.tsv") as f:
	next(f)
	for lines in f:
		line = lines.split("\t",1)
		score=0
		words = line[1].split()
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
				#print dict[word]
				wordscore = int(dict[word])
				if wordscore==0: wordscore=-1
				if neg == True:
					wordscore = -wordscore
					neg = False
				if wordscore < 0:
					#print("minus")
					#if wordscore<-10000:
					#	score = score - 1
					#if wordscore<-1000:
					#	score = score -1
					#if wordscore<-100:
					#	score = score - 1
					#if wordscore<-10:
					#	score = score - 1
					score = score - 1
				else:
					#print("plus")
					#if wordscore>10000:
					#	score = score + 1
					#if wordscore>1000:
					#	score = score + 1
					#if wordscore>100:
					#	score = score + 1
					#if wordscore>10:
					#	score = score + 1
					score = score + 1
				#time.sleep(.5)
		#print score
		#time.sleep(.5)
		if score < 0: 	
			scoredict[line[0]] = 0
		else:
			scoredict[line[0]] = 1
try:
	os.remove("SubmissionData.csv")
except OSError:
	pass

with open("SubmissionData.csv","w") as write:
	write.write("document_id,sentiment\n")
	for key in scoredict:
		word = key.translate(None, '\"')
		write.write(word+","+str(scoredict[key])+"\n")