import os
dict = dict()
num =0;
with open("TrainDataset.tsv") as f:
	next(f)
	for lines in f:
		num = num + 1
		line = lines.split("\t", 2)
		#print "."+line[1]+"."
		review = int(line[1])
		if review==0: review=-1
		#if line[1] is 0:
			#review=-1
			#print review
		#else:
			#review=1
			#print review
		#print review
		#print(line)
		words = line[2].split()
		for word in words:
			word = word.translate(None, '\".!></()?@,\\\';:+-*#$`')
			word = word.lower()
			#print("."+word+".")
			if word in dict:
				#print "Before: " + str(dict[word]) + " Review: " + str(review)
				dict[word] = [dict[word][0] + review,dict[word][1] + 1]
				#print "After" + str(dict[word])
			else:
				dict[word] = [review,1]
			#input("continue")

try:
	os.remove("TrainWords")
except OSError:
	pass
			
with open ("TrainWords", "a") as f:
	f.write("Word\tValue\n")
	for key in dict:
		#print(key + str(dict[key]))
				f.write(key+"\t"+str(dict[key][0])+"\n")
		#f.write("{}\t{}\n".format(key,str(value)))
		#print(key + str(value))
		
			