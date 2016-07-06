#!/usr/bin/python
# Convert the prompts file of voxforge to a .mlf file

import sys
import re
import os

class Mlfifier:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_path = self.local_folder
    self.training_folder = "training"
    self.testing_folder = "testing"

  def change_dir(self,folders):
    path = "%s/"%(self.local_folder)
    for folder in folders:
      path = "%s%s/"%(path,folder)
    os.chdir(path)
    self.current_path = path

  def get_files(self):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return files
  
  def prompt2mlf(self,mlf,datatype):
    mlf_file = open(mlf,"w")
    file_names = {}
    if datatype == "training":
      self.change_dir([self.training_folder,"k"])
    elif datatype == "testing":
      self.change_dir([self.testing_folder])
    files = self.get_files()
    self.change_dir([])
    for f in files:
      if f.endswith('.wav'):
	f_info = f.split("_")
	f_name = f_info[3][:-4]
	file_names[f[:-4]] = f_name
  
    mlf_file.write("#!MLF!#\n")
    for key,value in file_names.items():
      mlf_file.write('\"*/{0}.lab\"\n'.format(key))
      mlf_file.write("%s\n"%(value))
      mlf_file.write(".\n")

#mf = Mlfifier()
#mf.prompt2mlf("words.mlf","training")