import re
import pickle
import sys
import shlex

'''
To execute : 
python parse.py <Path to annotated text file>


'''

def newSplit(value):
    lex = shlex.shlex(value)
    lex.quotes = '"'
    lex.whitespace_split = True
    lex.commenters = ''
    return list(lex)

def getVideoName(sublist):
	for item in sublist:
		if(item.find("Video NCSLGR")!=-1 and item.find("master")!=-1):
			k = item.rfind(":")
			return item[k+1:]

def getStartFrame(sublist):
	for item in sublist:
		if(item.find("Start frame:")!=-1):
			k = item.rfind(":")
			return item[k+1:].strip()

def getEndFrame(sublist):
	for item in sublist:
		if(item.find("End frame:")!=-1):
				k = item.rfind(":")
				return item[k+1:].strip()

def getWords(sublist):
	for item in sublist:
		if(item.find("main gloss")!=-1):
			k = item[len("main gloss")+1:]
			print k
			try:
				gloss = shlex.split(k)
			except ValueError:
				gloss = newSplit(k)	
			wordList = []
			annotatedWordList = []
			j=0
			print gloss
			while(j<len(gloss)):
				if(gloss[j]=="|>"):
					annotatedWordList.append(["punct",gloss[j+1]])
					wordList.append("punct")
					j+=2
				else:	
					annotatedWordList.append([gloss[j],gloss[j+1],gloss[j+2]])
					wordList.append(gloss[j])
					j+=3
			return annotatedWordList,wordList

def getTranslation(sublist):
	for item in sublist:
		if(item.find("English translation")!=-1):
			return item[len("English translation")+1:].strip()

def main(fname):
	sentence = {}
	count=0
	with open(fname) as fp:
		lines = fp.readlines()
		alltext = "".join(lines)
	l = len(lines)
	'''
	s = "Number of utterances:"
	for i in range(l):
		lines[i] = re.sub("\n","",lines[i])
		if(lines[i].find(s) != -1):
			num_sent = lines[i][len(s)+1:]
	'''
	sample = alltext.split("Utterance ID:\t")
	#print len(sample)
	for i in range(1,len(sample)):
		sample[i] = re.sub("\t"," ",sample[i])
		sublist = sample[i].split("\n")
		mov_name = getVideoName(sublist)
		s_frame = getStartFrame(sublist)
		e_frame = getEndFrame(sublist)
		annotated,wordList = getWords(sublist)
		translated = getTranslation(sublist)
		if(translated == ""):
			continue
		sentence[count]={}
		sentence[count]["Video"] = mov_name
		sentence[count]["StartFrame"] = s_frame
		sentence[count]["EndFrame"] = e_frame
		sentence[count]["Annotated"] = annotated
		sentence[count]["Words"] = wordList
		sentence[count]["English"] = translated
		#print sentence[count].values()
		count+=1
	return sentence	

def save(fname,data):
	with open(fname+".pkl","w") as fp:
		pickle.dump(data,fp)
		

if(__name__=="__main__"):
	source = sys.argv[1]
	output = re.search("data/(.*)?[.]",source).group(1)
	sentences = main(source)
	save("parsed/"+output,sentences)
	vocab = []
	for key,values in sentences.items():
		vocab.extend(values["Words"])
	vocab = set(vocab)
	if("punct" in vocab):
		vocab.remove("punct")
	save("vocab/"+output,list(vocab))