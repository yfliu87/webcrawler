'''
helper file for replacing list with hashtabel for webpage indexing
'''

def hash_string(keyword, buckets):
	ret = 0

	for char in keyword:
		ret += ord(char)

	return ret%buckets