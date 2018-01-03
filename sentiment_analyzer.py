import csv
import pandas as pd
import datetime
import numpy as np 
import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle 



class Sentiment_Analyzer():
	def __init__(self, sentiment_generator, keywords, load=False):
		self._sentiment_generator = sentiment_generator
		self._keywords = sorted(keywords) 
		self._months = 	["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", 
			"Aug", "Sep", "Oct", "Nov", "Dec"]
		self._possible_sentiments = ["G", "B", "N"]
		if load:
			self.freq_dic = pickle.load(open("freq_dic.pkl", "rb"))
		else:
			self.build()
			self.save()
		self.get_range()
		self.get_pos_var()
		self.get_neg_var()
		self.get_all_entropy()

	def build(self):
		self.freq_dic = {}

		for year, month, word, compound_score in self._sentiment_generator:
			month = self._months.index(month)+1
			sentiment_type = self.get_sentiment_type(compound_score)

			if year not in self.freq_dic: self.freq_dic[year] ={}
			if month not in self.freq_dic[year]: self.freq_dic[year][month] ={}
			if word not in self.freq_dic[year][month]: 
				self.freq_dic[year][month][word] = {"G":0, "B":0, "N": 0, "T":0}

			self.freq_dic[year][month][word][sentiment_type] += 1
			self.freq_dic[year][month][word]["T"] += 1

	def get_sentiment_type(self, compound_score):
		sep_point = 0.8

		if compound_score > sep_point: return "G"
		elif compound_score < -sep_point: return "B"
		else: return "N"

	def get_range(self):
		self.start_year = min(self.freq_dic.keys())
		self.start_month = min(self.freq_dic[self.start_year].keys())

		self.end_year = max(self.freq_dic.keys())
		self.end_month = max(self.freq_dic[self.end_year].keys())

	def get_var(self, sentiment_type):
		var_dic = {}
		for word in self._keywords:
			sentiment_freq = []
			for year in self.freq_dic.values():
				for month in year.values():
					if word in month:
						if month[word]["T"] > 1000:
							sentiment_freq.append(month[word][sentiment_type]/month[word]["T"])
			if len(sentiment_freq) > 5:
				var_dic[word] = np.std(sentiment_freq)
		return var_dic

	def get_pos_var(self):
		self.pos_var = self.get_var("G")
	
	def get_neg_var(self):
		self.neg_var = self.get_var("B")



	def get_all_entropy(self):
		self.entropy_dic = {}
		for word in self._keywords:
			entropy_dist = [] 
			for year in self.freq_dic.values():
				for month in year.values():
					if word in month:
						entropy_dist.append(self.get_entropy(month[word]))
			self.entropy_dic[word] = entropy_dist


	def get_entropy(self, dist):
		if dist["G"] > 50 and dist["B"] >50:
			total = (dist["G"]+dist["B"])
			pos_freq = dist["G"]/total
			neg_freq = dist["B"]/total
			#neu_freq = (dist["T"]-dist["G"]-dist["B"])/dist["T"]

			entropy =0 
			for event in [pos_freq, neg_freq]:
				if event:
					entropy-= event*np.log(event)
			return entropy
		else:
			return 0

	def print_top_ten_entropy(self):
		top_ten = sorted(self.entropy_dic.items(), key=lambda x: self.modified_max(x[1]), reverse=True)[:100]
		for word, entropies in top_ten:
			print("Word: "+word+ " Entropy: "+str(self.modified_max(entropies)))


	def modified_max(self, array):
		if len(array) != 0:
			return max(array)
		else:
			return 0


	def print_top_ten(self,sentiment_type):
		if sentiment_type == "G":
			var_dic = self.pos_var
		else:
			var_dic = self.neg_var

		top_ten = sorted(var_dic.items(), key=lambda x: x[1], reverse=True)[:10]
		for word, var in top_ten:
			print("Word: "+word+ " var: "+str(var))


	def plot(self,keyword, full=True):
		x, good, bad, total = [], [], [] , []
		for year in self.freq_dic:
			for month in self.freq_dic[year]:
				#print(datetime.datetime(year, month, 15))
				x.append(datetime.datetime(year, month, 15))
				if keyword not in self.freq_dic[year][month]:
					good.append(0)
					bad.append(0)
					total.append(0)
				else:
					frequencies = self.freq_dic[year][month][keyword]
					good.append(frequencies["G"])
					bad.append(frequencies["B"])
					total.append(frequencies["T"])
		#print(x[0])
		x_y_tuple = list(zip(x, good, bad, total))
		x_y_tuple = sorted(x_y_tuple, key=lambda time_tuple: time_tuple[0])
		x, good, bad, total = list(zip(*x_y_tuple))
		x, good, bad, total= map(np.array, [x, good, bad, total])
		print(x[np.argmax(bad)])
		plt.plot(x, good)
		plt.plot(x, bad)
		if full:
			plt.plot(x, total)
		plt.legend(['Good', 'Bad', 'Total'], loc='upper left')
		plt.show()

	def get_order(self, time_freq):
		return 0
		time_tuple = time_freq[0].timetuple()
		return time_tuple[0]*12+time_tuple[1]

	def save(self):
		with open("freq_dic.pkl", "wb") as outfile:
			pickle.dump(self.freq_dic, outfile)



'''

	def plot(self,keyword, sentiment, display_type="ratio"):
		x, y = [], []
		for year in self.freq_dic:
			for month in self.freq_dic[year]:
				print(datetime.datetime(year, month, 15))
				x.append(datetime.datetime(year, month, 15))
				if keyword not in self.freq_dic[year][month]:
					y.append(0)
				else:
					frequencies = self.freq_dic[year][month][keyword]
					if display_type=="ratio":
						y.append(frequencies[sentiment]/frequencies["T"])
					elif display_type=="total":
						y.append(frequencies[sentiment])
					else:
						raise AssertionError("Not valid display type. Enter ratio or total")
		
		x_y_tuple = [(x[i], y[i]) for i in range(len(x))]
		print(x_y_tuple[0])
		x_y_tuple = sorted(x_y_tuple, key=lambda time_tuple: time_tuple[0])
		x = [x_y_tuple[i][0] for i in range(len(x))]
		y = [x_y_tuple[i][1] for i in range(len(x))]
		x, y = np.array(x), np.array(y)
		plt.plot(x, y)
		plt.show()
'''

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