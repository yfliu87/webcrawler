'''
initial version of webcrawler
The first version plans to do below things:
1. extract urls from seed page within specific depth
2. index urls to its content
3. simple query

Future work:
performance improvement
'''

def get_next_target(page):
	start_link = page.find('<a href=')

	if start_link == -1:
		return None, 0

	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote+1 : end_quote]
	print url, end_quote

def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)

		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break

	return links

def craw_web(seed):
	tocrawl = [seed]
	crawled = []

	while tocrawl:
		page = tocrawl.pop()

		if page not in crawled:
			links = get_all_links(page)
			#union links with tocrawl
			crawled.append(page)

	return crawled