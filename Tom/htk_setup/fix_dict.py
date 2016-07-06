class DictFixer:
  
  def __init__(self):
    self.fixedlines = []
    self.worddict = {}
    self.outputsym = {}
    self.length_longest_word = 0
    
  def fixdic(self):
    dictfixed = open("dict_fixed","w")
    with open("dict","r") as file:
      for line in file:
	content = line.split()
	word = content[0]
	phones = content[1:]
	combined_phones = " ".join(phones)
	self.worddict[word] = combined_phones
	self.outputsym[word] = ""
    self.worddict["silence"] = "sil"
    self.outputsym["silence"] = ""
    self.worddict["SENT-END"] = "sil"
    self.outputsym["SENT-END"] = "[]"
    self.worddict["SENT-START"] = "sil"
    self.outputsym["SENT-START"] = "[]"
    longest_word = ""
    for key in self.worddict.keys():
      if len(key) > self.length_longest_word:
	self.length_longest_word = len(key)
	longest_word = key
	
    for key,value in sorted(self.worddict.items()):
      #n = (length_longest_word-len(key))
      if 8 <= len(key) < 16:
	dictfixed.write("%s\t%s\t%s\n"%(key,self.outputsym[key],value))
      elif 0 < len(key) < 8:
	dictfixed.write("%s\t\t%s\t%s\n"%(key,self.outputsym[key],value))
    
    dictfixed.close()