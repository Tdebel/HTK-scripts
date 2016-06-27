import glob
import re

promptwavs = glob.glob('../segmentations/*')
file = open('words.mlf','w')
file.write("#!MLF!#\n")
for name in promptwavs:
	name = name.replace('../segmentations','*')
	file.write("\"" + name + "\"\n")
	prompt = re.search('_([a-zA-Z].+)\.', name)
	file.write(prompt.group(1) + "\n.\n")
