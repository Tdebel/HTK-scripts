import sys
import re
import os
import subprocess

class TestDataCoder:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_path = self.local_folder
    self.config = "config3"
    self.codetst = "codetst.scp"
    self.testscp = "test.scp"
    
  def change_dir(self,folders):
    path = "%s/"%(self.local_folder)
    for folder in folders:
      path = "%s%s/"%(path,folder)
    os.chdir(path)
    self.current_path = path
    
  def get_files(self):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return files
    
  def hcopy(self):
    params = "HCopy -T 1 -C %s -S %s"%(self.config,self.codetst)
    subprocess.call(params,shell=True)

  def execute(self):
    test_files = {}
    self.change_dir(["testing"])
    files = self.get_files()
    for f in files:
      if f.endswith('.wav'):
	test_files[f] = f[:-4]
    self.change_dir([])
    with open("codetst.scp","w") as scp_file:
      for key, value in test_files.items():
	line = "./testing/%s\t./mfcc/%s.mfc\n"%(key,value)
	scp_file.write(line)
    self.hcopy()
    with open("test.scp","w") as testscp_file:
      for key, value in test_files.items():
	line = "./mfcc/%s.mfc\n"%(value)
	testscp_file.write(line)
    
#tdc = TestDataCoder()
#tdc.execute()