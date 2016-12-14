linenum = 0
newlines=[]
id=""
text=""
space=""
sentiment = 0
with open("output.txt") as combine:
	#print combine[3]
	for line in combine:
		linenum=linenum + 1
		if linenum % 3 == 1:
			filename = line.split(".txt")
			id = filename[0]
			
		if linenum % 3 == 2:
			text = line
			text = text.rstrip()
		if linenum % 3 == 0:
			textvalue = id.split("_")
			sentiment = int(textvalue[1])
			if sentiment <5: sentiment = 0
			if sentiment >6: sentiment = 1
			newlines.append("\"" + id + "\"" + "\t" + str(sentiment) + "\t" + "\"" + text + "\"")
	combine.close()

with open("testoutput.tsv","w") as output:
		output.write("document_id\tsentiment\treview\n")
		for lines in newlines:
			output.write(lines + "\n")
		output.close()
