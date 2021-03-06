'''
initial version of webcrawler
The first version plans to do below things:
1. extract urls from seed page within specific depth
2. index urls to its content
3. simple query
4. rank pages

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
	return url, end_quote

def validURL(url):
	import re
	prog = re.compile(r'^http')
	return prog.match(url)

def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)

		if not url:
			break

		if validURL(url):
			links.append(url)

		page = page[endpos:]

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
		return "exception in get_page" 


def crawl_web(seed, max_depth):
	tocrawl = [seed]
	crawled = []
	index = {}
	graph = {}
	next_depth = []
	cur_depth = 0

	while tocrawl and cur_depth <= max_depth:
		page = tocrawl.pop()

		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			graph[page] = outlinks
			#union(tocrawl, outlinks)
			union(next_depth, outlinks)
			crawled.append(page)

		if not tocrawl:
			tocrawl,next_depth = next_depth,[]
			cur_depth += 1

	return index,graph 


def record_user_click(index, keyword, url):
	urls = lookup(index, keyword)

	if urls:
		for link in urls:
			if url == link[0]:
				link[1] += 1


def add_to_index(index, keyword, url):
	if keyword in index:
		if url in index[keyword]:
			return 
		else:
			index[keyword].append([url,0])

	else:
		index[keyword] = [[url, 0]]


def add_page_to_index(index, url, content):
	splitted_content = content.split(' ')

	for element in splitted_content:
		add_to_index(index, element, url)


def lookup(index, keyword):
	if keyword in index:
		return index[keyword]

	return None


#recursively check the cycling reference
def is_reciprocal(graph, source, dest, k):
	if k == 0:
		if source == dest:
			return True
		return False

	if source in graph[dest]:
		return True

	for page in graph[dest]:
		if is_reciprocal(graph, source, page, k - 1):
			return True

	return False

#pageRank
def compute_ranks(graph, k):
	dfactor = 0.8	#damping factor
	numloops = 10

	ranks = {}
	numPages = len(graph)

	#init each page with equal weights
	for page in graph:
		ranks[page] = 1.0/numPages

	for index in range(numloops):
		newranks = {}

		'''
		rank(page, t) = (1 - d)/npages 
			+ sum(d*rank(p,t-1)/number of outlinks from p) 
			over all pages p that link to this page
		'''
		for page in graph:
			newrank = (1.0 - dfactor)/numPages

			for node in graph:
				if page in graph[node]:

					#ignore pages that involved in cycling reference within k depth
					if not is_reciprocal(graph, node, page, k):		
						newrank += dfactor * (ranks[node]/len(graph[node]))

			newranks[page] = newrank

		ranks = newranks

	return ranks


def search_optimal(index, ranks, keyword):

	pages = lookup(index, keyword)

	if not pages:
		return None

	bestURL = pages[0] 

	for page in pages:
		if ranks[page] > ranks[bestURL]:
			bestURL = page

	return bestURL


def quicksort(pages, ranks):
	if not pages or len(pages) <= 1:
		return pages

	pivot = pages[0]
	less = []
	more = []

	for page in pages[1:]:
		if ranks[page] <= ranks[pivot]:
			less.append(page)
		else:
			more.append(page)

	return quicksort(more, ranks) + [pivot] + quicksort(less,ranks)


def ordered_search(index, ranks, keyword):
	pages = lookup(index, keyword)
	return quicksort(pages, ranks)


if __name__ == '__main__':
	index, graph = crawl_web('http://www.baidu.com', 0)
