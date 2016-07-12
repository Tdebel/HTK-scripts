class LatConverter:
  
  def __init__(self,htk_l,fst_l):
    self.htklattice = open(htk_l,"r")
    self.fstlattice = open(fst_l,"w")
    self.isyms = open("isyms.txt","w")
    self.osyms = open("osyms.txt","w")
    self.nodes = []
    self.arcs = {}
    self.labels = {}
    self.weights = {}
    self.input_symbols = []
    self.output_symbols = []
    
  def execute(self):
    self.isyms.write("<eps> 0\n")
    self.osyms.write("<eps> 0\n")
    startnode_counter = 0
    endnode_counter = 0
    for line in self.htklattice:
      if line.startswith("I"):
	content = line.split()
	node = content[0]
	label = content[2]
	self.nodes.append(node[2:])
	self.labels[node[2:]] = label[2:]
      if line.startswith("J"):
	content = line.split()
	arcnumber = content[0][2:]
	startnode = content[1][2:]
	endnode = content[2][2:]
	weight = content[3][2:]
	self.arcs[arcnumber] = (startnode,endnode)
	self.weights[arcnumber] = weight
      for key,value in self.arcs.items():
	startnode = value[0]
	endnode = value[1]
	label1 = self.labels[startnode]
	label2 = self.labels[endnode]
	if label1 not in self.input_symbols:
	  self.input_symbols.append(label1)
	if label2 not in self.output_symbols:
	  self.output_symbols.append(label2)
	weight = self.weights[key]
	line = "%s %s %s %s %s\n"%(startnode,endnode,label1,label2,weight)
	self.fstlattice.write(line)
	#line2 = "%s %s\n"%(label1,int(key)+1)
	#line3 = "%s %s\n"%(label2,int(key)+1)
	#self.isyms.write(line2)
	#self.osyms.write(line3)
    for x in range(0,len(self.input_symbols)):
      line2 = "%s %s\n"%(self.input_symbols[x],x+1)
      self.isyms.write(line2)
    for x in range(0,len(self.output_symbols)):
      line3 = "%s %s\n"%(self.output_symbols[x],x+1)
      self.osyms.write(line3)
    self.htklattice.close()
    self.fstlattice.close()
    self.isyms.close()
    self.osyms.close()
    
lc = LatConverter("cut_0_12715_minced.ext","fst_lattice.txt")
lc.execute()
