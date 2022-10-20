import requests
import math
import jsonlines
import re
import pandas as pd

base = 'https://journals.scholarsportal.info/data'

df = pd.read_csv('corpus.csv',usecols=['uri'])
uris = df['uri'].to_list()
dataArray = []

for i in uris:
	rowArray = []
	data = requests.get(base+i).json()
	rowArray.append(data['uri'])
	if data['is_entitled'] == True:
		if data['pdf'] == '' and data['xml_available'] == False:
			rowArray.append('NO FULLTEXT')
			print('NO FULLTEXT: '+data['uri'])
		else: 
			article = requests.get(data['json']).json()
			with jsonlines.open('harvest.jsonl', mode='a') as writer:
				writer.write(article)
			rowArray.append('SUCCESS')
			print('SUCCESS: '+data['uri'])
	else:
		rowArray.append('NOT ENTITLED')
		print('NOT ENTITLED: '+data['uri'])
	dataArray.append(rowArray)

lf = pd.DataFrame(dataArray,columns=[
	'uri',
	'status'
	])

lf.to_csv('log.csv', index=False)