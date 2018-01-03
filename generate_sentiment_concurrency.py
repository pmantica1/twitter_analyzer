import csv 
import re
import pickle
from cucco import Cucco
from tqdm import tqdm 
from sentiment_analyzer import Sentiment_Analyzer
from string import ascii_letters



def main():
	analyzer = Sentiment_Analyzer(get_sentiments(), get_domains(), load=True)
	#analyzer.print_top_ten_entropy()
	analyzer.plot("bubble", True)
	#analyzer.plot("bitcoin", "G")
	#sample("bubble", 2015, "Apr")

S
def sample(word, sample_year, sample_month):
	csvreader = csv.reader(open("sentiment_analyzed_tweets.txt"), delimiter="\t")
	cucco = Cucco() 
	sep_point = 0.5
	for line in tqdm(csvreader, total=20000000):
		text = line[3]
		time = line[2]
		month = time.split()[1] 
		year = int(time.split()[-1])
		sentiment = float(line[4])
		if year == sample_year:
			if month == sample_month:
				if word in normalize_lines(text, cucco):
					print(text)
					#if sentiment < -sep_point:
					



def get_sentiments():
	industry_keywords = get_domains()
	csvreader = csv.reader(open("sentiment_analyzed_tweets.txt"), delimiter="\t")
	cucco = Cucco()
	tot_count = 0
	written_count = 0 
	sep_point = 0.5
	for line in tqdm(csvreader, total=15000000):
		tot_count+=1
		text = line[3]
		time = line[2]
		month = time.split()[1] 
		year = int(time.split()[-1])
		sentiment = float(line[4])
		intersection = normalize_lines(text, cucco).intersection(industry_keywords)
	
		if len(intersection) > 0:
			written_count+=1
			for word in intersection:
				yield year, month, word, sentiment






def get_domains(): 
	industry_keywords = set(['new', 'president', 'time', 'people', 'made', 'news', 'national', 'business', 'make', 'political', 'house', 'market', 'work', 'financial', 'life', 'set', 'police', 'less', 'military', 'men', 'go', 'small', 'help', 'south', 'reviews', 'money', 'health', 'television', 'best', 'future', 'real', 'congress', 'family', 'find', 'past', 'program', 'security', 'children', 'local', 'senate', 'led', 'campaign', 'bush', 'music', 'sales', 'university', 'service', 'oil', 'play', 'open', 'social', 'exchange', 'industrial', 'human', 'system', 'art', 'game', 'pay', 'europe', 'book', 'credit', 'college', 'others', 'china', 'face', 'cause', 'building', 'history', 'force', 'free', 'defense', 'efforts', 'research', 'german', 'middle', 'vice', 'deep', 'food', 'medical', 'r.', 'certain', 'germany', 'baseball', 'turn', 'corporation', 'nuclear', 'investors', 'investment', 'study', 'students', 'markets', 'offer', 'film', 'heart', 'france', 'community', 'jersey', 'legal', 'leader', 'america', 'development', 'trading', 'job', 'energy', 'love', 'football', 'share', 'brooklyn', 'education', 'justice', 'peace', 'weather', 'form', 'san', 'vote', 'editorial', 'israel', 'japanese', 'services', 'article', 'safety', 'press', 'london', 'stocks', 'space', 'countries', 'buy', 'debate', 'reason', 'friends', 'management', 'russian', 'beyond', 'insurance', 'commercial', 'fire', 'russia', 'events', 'chicago', 'sell', 'performance', 'books', 'global', 'worth', 'sports', 'moving', 'water', 'movie', 'red', 'computer', 'car', 'commerce', 'english', 'basketball', 'word', 'radio', 'rest', 'spring', 'mexico', 'advertising', 'environmental', 'natural', 'proposal', 'currency', 'offers', 'body', 'square', 'middle east', 'search', 'construction', 'crime', 'banking', 'daily', 'author', 'due', 'movement', 'experience', 'technology', 'politics', 'sale', 'words', 'gold', 'iran', 'new jersey', 'test', 'stories', 'boston', 'finance', 'telephone', 'jobs', 'england', 'range', 'games', 'original', 'survey', 'writing', 'drive', 'doctors', 'inside', 'gas', 'hands', 'data', 'science', 'newspaper', 'post', 'character', 'al', 'blue', 'tv', 'steel', 'families', 'express', 'culture', 'progress', 'media', 'vietnam', 'airlines', 'video', 'connecticut', 'debt', 'india', 'paris', 'expect', 'cash', 'village', 'transportation', 'africa', 'characters', 'none', 'send', 'style', 'garden', 'travel', 'paper', 'florida', 'message', 'rock', 'opens', 'green', 'event', 'canada', 'mean', 'class', 'movies', 'calling', 'web', 'moral', 'views', 'details', 'training', 'manufacturing', 'design', 'agencies', 'challenge', 'happy', 'fashion', 'property', 'player', 'sex', 'carry', 'protection', 'wave', 'artist', 'convention', 'la', 'vast', 'cancer', 'forward', 'policies', 'cars', 'language', 'strength', 'communications', 'regional', 'moscow', 'trust', 'comedy', 'exhibition', 'discussion', 'internet', 'flight', 'marriage', 'films', 'bonds', 'access', 'retail', 'leads', 'electronic', 'latin', 'agents', 'blood', 'strategy', 'benefits', 'accounting', 'assembly', 'entertainment', 'academy', 'pop', 'ideas', 'claim', 'push', 'organizations', 'box', 'loans', 'host', 'fuel', 'spanish', 'pieces', 'unit', 'marketing', 'foundation', 'houston', 'brother', 'governments', 'singer', 'systems', 'brian', 'auto', 'net', 'jackson', 'makers', 'match', 'native', 'quick', 'teachers', 'projects', 'ties', 'crowd', 'consumers', 'reputation', 'spain', 'cable', 'basis', 'writers', 'sugar', 'studio', 'touch', '*', 'color', 'knowledge', 'investor', 'promises', 'outlook', 'online', 'payments', 'actions', 'technical', 'magazine', 'golf', 'voting', 'regulators', 'tennis', 'seat', 'earth', 'maker', 'teacher', 'corruption', 'request', 'automobile', 'morgan', 'tickets', 'creative', 'interviews', 'futures', 'retailers', 'wedding', 'agriculture', 'rally', 'girls', 'hero', 'brazil', 'poland', 'premiere', 'glass', 'detroit', 'motor', 'asia', 'shopping', 'founder', 'europe.', 'advice', 'broadcast', 'radical', 'apparel', 'hospitals', 'eve', 'identity', 'deals', 'beauty', 'mortgage', 'photography', 'immigration', 'elderly', 'exercise', 'cool', 'taste', 'wind', 'composer', 'spot', 'restaurant', 'musicians', 'challenges', 'pages', '500', 'retirement', 'alice', 'metal', 'mention', 'miami', 'facts', 'storm', 'solid', 'consulting', 'religion', 'learning', 'legacy', 'teaching', 'hits', 'publishing', 'engagement', 'indeed', 'restaurants', 'healthy', 'ensemble', 'fun', 'reporting', 'capacity', 'researchers', 'lowest', 'software', 'ireland', 'contest', 'acute', 'constant', 'marine', 'turkey', 'adult', 'kids', 'mets', 'wood', 'employment', 'surface', 'symphony', 'shop', 'testing', 'jason', 'object', 'engineering', 'ticket', 'doctor', 'disney', 'proper', 'speaker', 'motion', 'pakistan', 'medicine', 'themes', 'core', 'magic', 'shipping', 'summit', 'chronicle', 'swing', 'utility', 'flow', 'privacy', 'mail', 'outlets', 'memories', 'designer', 'journal', 'racing', 'brand', 'concerts', 'motors', 'guitar', 'statistics', 'goals', 'tracks', 'atlanta', 'electronics', 'passion', 'equity', 'confident', 'argentina', 'publication', 'arm', 'apple', 'forth', 'walking', 'brain', 'imagine', 'poetry', 'doors', 'tens', 'julia', 'coffee', 'principle', 'pension', 'dallas', 'relationships', 'options', 'camera', 'clothing', 'secure', 'installation', 'pure', 'roots', 'economics', 'awards', 'code', 'computers', 'asterisk', 'analyst', 'phil', 'parking', 'communities', 'atomic', 'sculpture', 'drivers', 'furniture', 'wholesale', 'c', 'gifts', 'journalists', 'boom', 'windows', 'tobacco', 'mortgages', 'resume', 'wine', 'aeronautics', 'surgery', 'michigan', 'distribution', 'broadcasting', 'noise', 'conversation', 'aviation', 'monthly', 'truck', 'mothers', 'gambling', 'auction', 'maria', 'charging', 'virus', 'document', 'sessions', 'injury', 'device', 'passenger', 'payment'])
	industry_keywords = set(["bitcoin"])
	with open("pkl_input/primary_domains.pkl", "rb") as infile:
		tags = pickle.load(infile)

	industry_keywords = []
	for tag, domains in tags.items():
		if len(domains) ==1:
			if all(c in ascii_letters+'-' for c in tag):
				industry_keywords.append(tag.lower())

	industry_keywords = ["bubble"]
	return set(industry_keywords)



def replace_char(char):
	chars_to_be_replaced ="|\\,/!?.-"
	if char in chars_to_be_replaced:
		return " " 
	else:
		return char



def normalize_lines(string, cucco):
	#print(string)
	first_norm = re.sub(r"http\S+", "", string)
	#print(first_norm)
	chars_to_be_deleted = "@#$%^&*()_={}[]:;\"<>'"
	second_norm = "".join([char for char in first_norm if not char in chars_to_be_deleted])  
	#print(second_norm)
	third_norm = "".join([replace_char(char) for char in second_norm])
	#print(third_norm)

	return set(third_norm.lower().split())

main()





