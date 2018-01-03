import csv
from tqdm import tqdm 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#from nltk.sentiment.sentiment_analyzer import SentimentAnalyzer



def main():
	analyzer = SentimentIntensityAnalyzer()
	with open("formatted_tweets.txt") as infile:
		with open("sentiment_analyzed_tweets.txt", "w") as outfile:
			csvreader = csv.reader(infile, delimiter="\t")
			csvwriter = csv.writer(outfile, delimiter="\t")
			for line in tqdm(csvreader, total=15000000):
				text = line[3]
				line += [analyzer.polarity_scores(text)["compound"]]
				csvwriter.writerow(line)
		

main()

#def get_sentiment(string, )