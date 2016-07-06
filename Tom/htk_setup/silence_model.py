import os
import sys
import subprocess
import shutil

class Silencer:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_path = self.local_folder
    self.silhed = "sil.hed"
    self.monophones = "monophones1"
    
  def change_dir(self,folders):
    path = "%s/"%(self.local_folder)
    for folder in folders:
      path = "%s%s/"%(path,folder)
    os.chdir(path)
    self.current_path = path
  
  def get_files(self):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return files
    
  def move_file(self,file_name,new_path):
    os.rename(self.current_path + file_name, new_path + "old_%s"%(file_name))
    
  def new_folder(self,name,path):
    new_path = path + name
    if not os.path.exists(new_path):
      os.makedirs(new_path)
    return new_path
  
  def hhed(self,index):
    params = "HHEd -H hmm%s/macros -H hmm%s/hmmdefs -M hmm%s %s %s"%(index-1,index-1,index,self.silhed,self.monophones)
    print(params)
    subprocess.call(params,shell=True)
  
  def execute(self,index):
    new_path = self.new_folder("/hmm%s"%(index),self.local_folder)
    self.change_dir(["hmm%s"%(index-1)])
    files = self.get_files()
    for f in files:
      if f.startswith('hmmdefs'):
	shutil.copy2('%s/hmm%s/%s'%(self.local_folder,index-1,f),'%s/hmm%s/old_hmmdefs'%(self.local_folder,index))
      elif f.startswith('macros'):
	shutil.copy2('%s/hmm%s/%s'%(self.local_folder,index-1,f),'%s/hmm%s'%(self.local_folder,index))
    
    self.change_dir(["hmm%s"%(index)])
    searchquery = "~h \"sil\""
    searchqueryindex = 0
    sp_model = []
    sil_model = []
    with open("old_hmmdefs","r") as f1:
      with open("hmmdefs","w") as f2:
	lines = f1.readlines()
	for i, line in enumerate(lines):
	  if line.startswith(searchquery):
	    searchqueryindex = i
	for i, line in enumerate(lines):
	  if line.startswith(searchquery):
	    sil_model = lines[i:i+28]
	    sil_text = "".join(sil_model)
	    sp_model.append("~h \"sp\"\n")
	    sp_model.append(lines[i + 1])
	    sp_model.append("<NUMSTATES> 3\n")
	    sp_model.append("<STATE> 2\n")
	    sp_model.append(lines[i + 10])
	    sp_model.append(lines[i + 11])
	    sp_model.append(lines[i + 12])
	    sp_model.append(lines[i + 13])
	    sp_model.append(lines[i + 14])
	    sp_model.append("<TRANSP> 3\n")
	    sp_model.append(" 0.0 1.0 0.0\n 0.0 0.9 0.1\n 0.0 0.0 0.0\n")
	    sp_model.append(lines[i + 27])
	    sp_text = "".join(sp_model)
	    f2.write(sil_text)
	    f2.write(sp_text)
	  elif i not in range(searchqueryindex,searchqueryindex+28):
	    f2.write(line)
    os.remove("old_hmmdefs")
    
    self.change_dir([])
    with open("sil.hed","w") as f3:
      f3.write("AT 2 4 0.2 {sil.transp}\nAT 4 2 0.2 {sil.transP}\nAT 1 3 0.3 {sp.transP}\nTI silst {sil.state[3],sp.state[2]}\n")
    
    #with open("monophones1","w") as f4:
      #with open("monophones0","r") as f5:
	#lines = f5.readlines()
	#lines.append("sp\n")
	#lines = sorted(lines)
	#for line in lines:
	  #f4.write(line)
    new_path2 = self.new_folder("/hmm%s"%(index+1),self.local_folder)
    self.hhed(index+1)
	  
#sl = Silencer()
#sl.execute(4)
