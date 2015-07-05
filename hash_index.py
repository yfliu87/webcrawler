'''
helper file for replacing list with hashtabel for webpage indexing
'''

def hash_string(keyword, buckets):
	ret = 0

	for char in keyword:
		ret += ord(char)

	return ret%buckets


def make_hashtable(bucketsize):
	htable = []

	for index in bucketsize:
		htable.append([])

	return htable


def hashtable_get_bucket(htable, keyword):
	return htable[hash_string(keyword, len(htable))]


def hashtable_add(htable, key, value):
	hashtable_get_bucket(htable, keyword).append([key, value])


def find_bucket(bucket, key):
	for entry in bucket:
		if entry[0] == key:
			return entry[1]

	return None


def hashtable_lookup(htable, key):
	entry = find_bucket(hashtable_get_bucket(htable, key))

	if entry:
		return entry[1]
	else:
		return None


def hashtable_update(htable, key, value):
	bucket = hashtable_get_bucket(htable, key)
	entry = find_bucket(bucket, key)

	if entry:
		entry[1] = value
	else:
		bucket.append([key, value])
