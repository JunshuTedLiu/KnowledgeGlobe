# Big thanks to Lanfei Liu, who built a tool in Python using Springer Metadata API and other APIs in order to generate literature review data.
# Lanfei's code: github.com/lanfeiliu/SpringerAPI-ElsevierAPI_LiteratureReviewTable

# By learning her code, I figured out how to gather data from the Springer metadata JSON output using Python with filters (query), manage these data, and create & write CSV files by columns.

# I rewrote mostly everything for our own research for the Knowledge Globe project, while I kept her part of the code for querying, which is filtering by topic and year by user input. Once I figured out how she implements the query, I could add a new feature that could allow the user to filter the data by other conditions.

# In the JSON metadata, "records" and "facets" has the same structure. Lanfei's code helped me to understand how to gather and organize the data. However, I rewrote these part of the code because we need to use the "facets" data for statistics ("counts"), instead of "records" that she was using.
# The method of getting these data is the same as Lanfei's, but since we are making completely different things, I made some changes in the Springer_Article class - I made several lists directly for the columns in all datasets, instead of combining data in a string.

### KNOWLEDGE GLOBE

# KnowledgeGlobe.py
# Junshu Liu

import unittest
import requests
import json
import csv
import os

print "\nKNOWLEDGE GLOBE\n===============\nSee how researchers around the world leading the evolution of knowledge. No matter when and where.\n"

keyword = raw_input("Say a topic. Could be a single word or phase.\nTOPIC: ")

date_int = int(raw_input("\nWhat range of time would you like to see? Name that year.\nYEAR: "))

springer_keyword = "?q=("+ "%22" + keyword.replace(" ", "%20") + "%22" + "%20AND%20year:" + str(date_int) + ")"


springer_api_key = raw_input("\nEnter your Springer API key.\nNeed help? Visit https://dev.springernature.com/ for more details.\nAPI key: ")

base_url_springer = 'http://api.springer.com/metadata/json'

url_params_springer = {}
url_params_springer["api_key"] = springer_api_key
url_params_springer["p"] = 300   # If put 200: 10 results will be returned. This doesn't affect for counts. I've tested this line of code and changed this value to 300 and 400, and the outputs are the same.

try:
	for_springer = open('raw_JSON_%s_%i.txt' % (keyword,int(date_int))).read()
	d_springer = json.loads(for_springer)

except:
	d_springer = requests.get(base_url_springer + springer_keyword
								,params=url_params_springer).json()

	print "\n=== See the result of Springer Metadata API in your directory. ===\n"

	fr_springer = open('raw_JSON_%s_%i.txt' % (keyword,int(date_int)),"w")
	fr_springer.write(json.dumps(d_springer))
	fr_springer.close()

class Springer_Article():
    def __init__(self, records={}):
		self.records = records
		self.title = records['title'].encode('utf-8')
		self.abstract = records['abstract'].encode('utf-8')[8:]# get rid of the word "Abstract"

# facet_cat_insts = [Springer_Article(facets) for facets in d_springer['facets']] # 6 items, means 6 attributes in "facets".

article_insts = [Springer_Article(records) for records in d_springer['records']]

# for i in article_insts:
# 	if i.title in titlelst:
# 		article_insts.remove(i)

# count = 0
#
# for records in article_insts:
# 	count = count + 1

# #Create Springer csv file
titlelst = [i.title for i in article_insts]
abstractlst = [i.abstract for i in article_insts]

# file1=open('abstract_full.csv','wb')
# writer=csv.writer(file1)
#
# writer.writerow(['title','abstract'])
# writer.writerow(zip(titlelst,abstractlst))



alllistwithtuples = zip(titlelst,abstractlst)

allinonestring = ' '.join([i for sub in alllistwithtuples for i in sub])

titlestr = "".join(allinonestring)

# print zip(titlelst,abstractlst)

# print titlestr

file1=open('abstract_e_%s_%i.txt' % (keyword,int(date_int)),'wb')
file1.write(titlestr)

print '--------Created text file "abstract_e_%s_%i.txt"-----------' % (keyword,int(date_int))
