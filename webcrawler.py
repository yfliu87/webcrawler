'''
initial version of webcrawler
The first version plans to do below things:
1. extract urls from seed page within specific depth
2. index urls to its content
3. simple query

Future work:
performance improvement
'''

def find_url(page):
	start_link = page.find('<a href=')
	start_quote = page.find('"', start_link + 1)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote : end_quote]
	print url