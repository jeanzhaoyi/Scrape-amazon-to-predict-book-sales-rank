exec(open('fun_ParseReviews.py').read())

# load saved links
text_file = open('unique_biography_review_links.txt','r')
review_links = text_file.read().split('\n')

#os.chdir('biogrphies/' )


for i in review_links[1:]:
	temp_data = ParseReviews(i) #review_links[i]
	file_path = re.sub(' ', '_', temp_data['name'])
	file_path = re.sub(r'\W', '', file_path)+ '.json'
	with open( file_path,'w') as outfile:
		json.dump(temp_data, outfile)
