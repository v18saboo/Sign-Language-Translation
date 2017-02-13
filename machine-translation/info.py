import csv
import gensim
def print_count():
	d={}
	with open("translations.csv","r") as fp:
		reader = csv.reader(fp,delimiter=";")
		for row in reader:
			lhs = len(row[0].split())
			rhs = len(row[1].strip().split())
			d[lhs]=d.get(lhs,0)+1
	print d

def get_data():
	gloss=[]
	eng=[]
	with open("translations.csv","r") as fp:
		reader = csv.reader(fp,delimiter=";")
		for row in reader:
			gloss=row[0]
			eng=row[1].strip()
	return gloss,eng
			
def main():
	gloss,eng=get_data()
	

if(__name__=="__main__"):
	main()