'''
initial version of webcrawler
The first version plans to do below things:
1. extract urls from seed page within specific depth
2. index urls to its content
3. simple query

Future work:
performance improvement
'''

index = []

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


def union(p, q):
	for element in q:
		if element not in p:
			p.append(element)


def split_string(source, splitlist):
	result = []
	isAtSplitor = True

	for char in source:
		if char in splitlist:
			isAtSplitor = True
		else:
			if isAtSplitor:
				result.append(char)
				isAtSplitor = False
			else:
				result[-1] = result[-1] + char

	return result


def get_page(url):
	try:
		import urllib
		return urllib.urlopen(url).read()
	except:
		return "" 


def crawl_web(seed):
	tocrawl = [seed]
	crawled = []
	index = []

	while tocrawl:
		page = tocrawl.pop()

		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			union(tocrawl, get_all_links(page))
			crawled.append(page)

	return index 


def add_to_index(index, keyword, url):
	for idx in index:
		if idx[0] == keyword and url not in idx[1]:
			idx[1].append(url)
			return

	index.append([keyword, [url]])


def add_page_to_index(index, url, content):
	splitted_content = content.split(' ')

	for element in splitted_content:
		add_to_index(index, element, url)


def lookup(index, keyword):
	for entry in index:
		if entry[0] == keyword:
			return entry[1]

	return []