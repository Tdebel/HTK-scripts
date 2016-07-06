import os
import sys
import subprocess

class ReEstimator:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_path = self.local_folder
    self.config = "config2"
    self.phonesmlf = "phones0.mlf"
    self.trainscript = "train.scp"
    self.monophones0 = "monophones0"
    self.monophones1 = "monophones1"
    
  def new_folder(self,name,path):
    new_path = path + name
    if not os.path.exists(new_path):
      os.makedirs(new_path)
    
  def herest(self,index):
    if index < 4:
      params = "HERest -C %s -I %s -t 250.0 150.0 1000.0 -S %s -H hmm%s/macros -H hmm%s/hmmdefs -M hmm%s %s"%(self.config,self.phonesmlf,self.trainscript,index-1,index-1,index,self.monophones0)
      subprocess.call(params,shell=True)
    else:
      params = "HERest -C %s -I %s -t 250.0 150.0 1000.0 -S %s -H hmm%s/macros -H hmm%s/hmmdefs -M hmm%s %s"%(self.config,self.phonesmlf,self.trainscript,index-1,index-1,index,self.monophones1)
      subprocess.call(params,shell=True)
    
  def execute(self,start,end):
    for index in range(start,end+1):
      self.new_folder("/hmm%s"%(index),self.local_folder)
    for index in range(start,end+1):
      self.herest(index)
  
#re = ReEstimator()
#re.execute(6,7)
