import os
import sys
import subprocess

class Evaluator:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.testscript = "test.scp"
    self.outputfile = "recout.mlf"
    self.wdnet = "wdnet"
    self.dic = "dict_fixed"
    self.monophones = "monophones1"
    self.testrefmlf = "testref.mlf"
    
  def hvite(self,index):
    params = "HVite -H hmm%s/macros -H hmm%s/hmmdefs -S %s -l '*' -i %s -w %s -p 0.0 -s 5.0 %s %s"%(index,index,self.testscript, self.outputfile, self.wdnet, self.dic, self.monophones)
    print(params)
    subprocess.call(params,shell=True)
  
  def hresults(self):
    params = "HResults -I %s %s %s"%(self.testrefmlf,self.monophones,self.outputfile)
    subprocess.call(params,shell=True)

  def execute(self,index):
    self.hvite(index)
    self.hresults()
    
#ev = Evaluator()
#ev.execute(7)