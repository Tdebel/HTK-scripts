#!/usr/bin/env python
outdir = "/home/thomas/Documents/HTKGit/HTKThomas/step6/hmm0"
monodir = "monophones0"


file = open(outdir+"/hmmdefs", "w")

monophones = open(monodir, "r")
mono_list = monophones.read().splitlines()
proto = open("hmm0/proto", "r");
proto_text = proto.read().splitlines()[4:]
proto_text = "\n".join(proto_text)



for m in mono_list:
	file.write("~h \"" + m + "\"\n")
	file.write(proto_text + "\n")

file.close()
monophones.close()
