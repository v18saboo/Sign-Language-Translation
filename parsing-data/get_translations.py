import os
import pickle

def main():
	for path, subdirs, files in os.walk("parsed/"):
		for name in files:
			fname = os.path.join(path, name)
			if(fname.find("ncslgr-1")==-1 and fname.find("ncslgr-2")==-1):
				continue
			with open(fname,"r") as fp:
				sentences = pickle.load(fp)
			for i in range(len(sentences)):
				print " ".join(sentences[i]["Words"]).lower(),";",sentences[i]["English"].lower()


if(__name__=="__main__"):
	main()