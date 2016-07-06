import sys
import re
import os

class MfcScpCreator:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_path = self.local_folder
    
  def change_dir(self,folders):
    path = "%s/"%(self.local_folder)
    for folder in folders:
      path = "%s%s/"%(path,folder)
    os.chdir(path)
    self.current_path = path
    
  def get_files(self):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return files
  
  def execute(self):
    training_files = {}
    self.change_dir(["training","k"])
    files = self.get_files()
    for f in files:
      if f.endswith('.wav'):
	training_files[f] = f[:-4]
    self.change_dir([])
    with open("train.scp","w") as scp_file:
      for key, value in training_files.items():
	line = "./mfc/%s.mfc\n"%(value)
	scp_file.write(line)
    
  
