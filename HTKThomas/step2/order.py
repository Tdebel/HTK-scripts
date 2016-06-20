#!/usr/bin/env python

fname = "ROGER_dictionary.txt"

with open(fname, "r") as f:
	content = f.readlines()
	content = list(set(content))
	content.sort()
	file = open("ordered_dict.txt", "w")
	for line in content:
		file.write(line)
	file.close()
