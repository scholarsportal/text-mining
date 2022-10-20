import requests
import math
import re
import pandas as pd

#####################################################

# USER DEFINED VARIABLES:

# You can construct your boolean logic on the search form and copy the query string from the results page (English only for now).
query = '(TITLE:(water) AND (testing) AND (ontario))'	
pageLength = 20		# The larger the results per page the slower the response. 

#dataType = 'id' 	# Returns URIs only. This is very fast you should be able to grab thousands at a time. 
dataType = 'bib' 	# Results include bibliographic data like titles and authors.
#dataType = 'full'	# Results include everything including abstracts, snippets and keywords.

######################################################

base = 'https://journals.scholarsportal.info/search?q='
page = 1 
dataArray = []

def get_results(page):
	url = base+query+'&page='+str(page)+'&page_length='+str(pageLength)+'&data='+dataType+'&format=json'
	results = requests.get(url).json()
	return results['response']

# this cleans leading and trailing whitespaces
def ws(string):
	clean = re.sub("^\s+|\s+$", "", string)
	return clean

def make_row(data):
	rowArray = []

	if 'uri' in data:
		rowArray.append(data['url'])
	else: rowArray.append('')

	if 'uri' in data:
		rowArray.append(data['uri'])
	else: rowArray.append('')

	if 'title' in data:
		rowArray.append(ws(data['title']))
		print(data['title'])
	else: rowArray.append('')

	if 'author' in data['authors'][0]:
		authors = data['authors'][0]['author']
		authorsArray = []
		for i in authors:
			authorsArray.append(ws(i['surname'])+', '+ws(i['given-names']))
		rowArray.append('; '.join(authorsArray))
	else: rowArray.append('')

	if 'journal-title' in data['source']:
		rowArray.append(data['source']['journal-title'])
	else: rowArray.append('')

	if 'pub-date' in data['source']:
		rowArray.append(data['source']['pub-date'])
	else: rowArray.append('')

	if 'volume' in data['source']:
		rowArray.append(data['source']['volume'])
	else: rowArray.append('')

	if 'issue' in data['source']:
		rowArray.append(data['source']['issue'])
	else: rowArray.append('')

	if 'doi' in data['source']:
		rowArray.append(data['source']['doi'])
	else: rowArray.append('')

	return rowArray

results = get_results(page)

total = int(results['total'])
pages = math.ceil(total/pageLength)

for i in results['results']['result']:
	rowArray = make_row(i)
	dataArray.append(rowArray)

# get subsequent pages
for p in range(2, pages+1):
	results = get_results(p)
	for i in results['results']['result']:
		rowArray = make_row(i)	
		dataArray.append(rowArray)

df = pd.DataFrame(dataArray,columns=[
	'url',
	'uri',
	'title',
	'author',
	'journal',
	'date',
	'volume',
	'issue',
	'doi'
	])

df.to_csv('corpus.csv', index=False)