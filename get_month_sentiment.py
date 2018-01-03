import csv
import pandas as pd
import datetime
import numpy as np 
import matplotlib.pyplot as plt
from tqdm import tqdm



class Sentiment_Analyzer():
	def __init__(self, sentiment_generator, keywords):
		self._sentiment_generator = sentiment_generator
		self._keywords = sorted(keywords) 
		self._months = 	["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", 
			"Aug", "Sep", "Oct", "Nov", "Dec"]
		self._possible_sentiments = ["G", "B", "N"]
		self.build()
		self.get_range()
	def build(self):
		self.freq_dic = {}

		for year, month, word, compound_score in self._sentiment_generator:
			month = index(self._months)+1


			if year not in self.freq_dic: self.freq_dic[year] ={}
			if month not in self.freq_dic[year]: self.freq_dic[year][month] ={}
			if word not in self.freq_dic[year][month]: 
				self.freq_dic[year][month][word] = {"G":0, "B":0, "N": 0, "T":0}

			self.freq_dic[year][month][word][sentiment_type] += 1
			self.freq_dic[year][month][word]["T"] += 1

	def get_sentiment_type(compound_score):
		sep_point = 0.5

		if compound_score > sep_point: return "G"
		elif compound_score < -sep_point: return "B"
		else: return "N"
		
	def get_range():
		self.start_year = min(self.freq_dic.keys())
		self.start_month = min(self.freq_dic[self.start_year].keys())

		self.end_year = max(self.freq_dic.keys())
		self.end_month = max(self.freq_dic[self.end_year].keys())

	def plot(keyword, sentiment, display_type="ratio"):
		x, y = [], []
		for year in self.freq_dic:
			for month in self.freq_dic[year]:
				x.append(datetime.datetime(year, month))
				if word not in freq_dic:
					y.append(0)
				else:
					frequencies = freq_dic[year][month][keyword]
					if display_type=="ratio":
						y.append(frequencies[sentiment])
					elif display_type:"total":
						y.append(frequencies[sentiment])
					else:
						raise AssertionError("Not valid display type. Enter ratio or total")
		x, y = np.array(x), np.array(y)
		plt.plot(x, y)
		plt.show()

		for i in range((self.end-year-self.start_year))



'''




def get_freq_dic():
	sentiment_generator = generate_sentiment_concurrency.get_sentiments()
	year_month_dic[year] = year_month_dic.get(year, {})
	year_month_dic[year][month] = year_month_dic[year].get(month, {})
	year_month_dic[year][month][domain] = year_month_dic[year][month].get(domain, 0)+1
		#print(year_month_dic[year][month][domain])

def main():



	domain_order = sorted(list(generate_sentiment_concurrency.get_doma))

	year_month_tup = [] 
	for year in year_month_dic:
		for month in year_month_dic[year]:
			year_month_tup.append((year, month))

	year_month_tup.sort(key=lambda x: month_order.index(x[1]))
	year_month_tup.sort(key=lambda x: x[0])

	with open("parent_freq.tsv", "w") as outfile:
		csvwriter = csv.writer(outfile, delimiter="\t")
		csvwriter.writerow(["Year", "Month"]+domain_order)
		for year, month in year_month_tup:
			domain_freqs = []
			for domain in domain_order:
				freq = year_month_dic[year][month].get(domain, 0)
				#print(year_month_dic[year][month])
				domain_freqs.append(freq)
				#print(freq)
			csvwriter.writerow([year, month]+domain_freqs)
'''