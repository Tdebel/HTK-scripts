import glob
import re

promptwavs = glob.glob('../segmentations/*')
outdir = "/home/thomas/Documents/HTKGit/HTKThomas/step5/mfc/"

file = open("codetr.scp", "w")

for name in promptwavs:
	sub = name.replace('../segmentations/','')
	sub2 = sub.replace('wav', 'mfc')
	str = name + " " + outdir + sub2 + "\n"
	file.write("%s"%(str))
file.close()
	 
	


