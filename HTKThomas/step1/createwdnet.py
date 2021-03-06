#!/usr/bin/env python

import glob
import re

prompts = glob.glob('../testing/mfc/*')
file = open('gram', 'w')
file.write('$word = ')

for word in prompts:
	word = word.replace('mfc/', '')
	prompt = re.search('_([a-zA-Z].+)\.', word)
	file.write(prompt.group(1) + " | ")
file.write('( silence $word silence )')



#import glob
#import re

#promptwavs = glob.glob('../segmentations/*')
#file = open('words.mlf','w')
#file.write("#!MLF!#\n")
#for name in promptwavs:
#	name = name.replace('../segmentations','*')
#	file.write("\"" + name + "\"\n")
#	prompt = re.search('_([a-zA-Z].+)\.', name)
#	file.write(prompt.group(1) + "\n.\n")

#$digit = ONE | TWO | THREE | FOUR | FIVE |
#SIX | SEVEN | EIGHT | NINE | OH | ZERO;
#$name = [ STEVE ] YOUNG;
#( SENT-START ( DIAL <$digit> | (PHONE|CALL) $name) SENT-END )

