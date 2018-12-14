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
	for_springer = open('statistics.txt').read()
	d_springer = json.loads(for_springer)

except:
	d_springer = requests.get(base_url_springer + springer_keyword
								,params=url_params_springer).json()

	print "\n=== See the result of Springer Metadata API in your directory. ===\n"

	fr_springer = open("statistics.txt","w")
	fr_springer.write(json.dumps(d_springer))
	fr_springer.close()

class Springer_Article():
    def __init__(self, facets={}):
        self.facets = facets

    def count(self):
        count_lst = [i['count'].encode('utf-8') for i in self.facets['values']]
        # combine_name = ', '.join(count_lst)
        return count_lst
        # return combine_name

    def value(self):
        value_lst = [i['value'].encode('utf-8') for i in self.facets['values']]
        # combine_name = ', '.join(value_lst)
        return value_lst
        # return combine_name


facet_cat_insts = [Springer_Article(facets) for facets in d_springer['facets']] # 6 items, means 6 attributes in "facets".

count = 0

for facets in facet_cat_insts:
    count = count + 1 # is 6

countlst = [i.count() for i in facet_cat_insts]
countlst_subject = countlst[0]
countlst_keyword = countlst[1]
countlst_pub = countlst[2]
countlst_year = countlst[3]
countlst_country = countlst[4]
countlst_type = countlst[5]
valuelst = [i.value() for i in facet_cat_insts]
valuelst_subject = valuelst[0]
valuelst_keyword = valuelst[1]
valuelst_pub = valuelst[2]
valuelst_year = valuelst[3]
valuelst_country = valuelst[4]
valuelst_type = valuelst[5]

file0=open('statistics_subject.csv','wb')
writer=csv.writer(file0)

writer.writerow(['count','value'])
writer.writerows(zip(countlst_subject, valuelst_subject))

print '-------- Created dataset file "statistics_subject.csv" -----------'

# ---

file1=open('statistics_keyword.csv','wb')
writer=csv.writer(file1)

writer.writerow(['count','value'])
writer.writerows(zip(countlst_keyword, valuelst_keyword))

print '-------- Created dataset file "statistics_keyword.csv" -----------'

# ---

file2=open('statistics_pub.csv','wb')
writer=csv.writer(file2)

writer.writerow(['count','value'])
writer.writerows(zip(countlst_pub, valuelst_pub))

print '-------- Created dataset file "statistics_pub.csv"     -----------'

# ---

file3=open('statistics_year.csv','wb')
writer=csv.writer(file3)

writer.writerow(['count','value'])
writer.writerows(zip(countlst_year, valuelst_year))

print '-------- Created dataset file "statistics_year.csv"    -----------'

# ---

file4=open('statistics_country.csv','wb')
writer=csv.writer(file4)

writer.writerow(['count','value'])
writer.writerows(zip(countlst_country, valuelst_country))

print '-------- Created dataset file "statistics_country.csv" -----------'

# ---

file5=open('statistics_type.csv','wb')
writer=csv.writer(file5)

writer.writerow(['count','value'])
writer.writerows(zip(countlst_type, valuelst_type))

print '-------- Created dataset file "statistics_type.csv"    -----------\n'

### For test purpose.
# print subject_count
# print count
# print countlst_year
