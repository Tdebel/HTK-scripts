import os
import sys
import random
import shutil

class Sorter:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_path = self.local_folder
    self.training_folder = "%s/training/"%(self.local_folder)
    self.testing_folder = "%s/testing/"%(self.local_folder)
    
  '''
  method change_dir will change the current directory
  :param: [string] folders contains the name of the folders
  in order to build the path
  '''
  def change_dir(self,folders):
    path = "%s/"%(self.local_folder)
    for folder in folders:
      path = "%s%s/"%(path,folder)
    os.chdir(path)
    self.current_path = path

  '''
  method get_files will return all files in the current directory
  '''
  def get_files(self):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return files
    
  '''
  method move_file will move a file to another directory
  :param: string file_name holds the name of the file to be moved
  :param: string new_path holds the path name of the new directory
  '''
  def move_file(self,file_name,new_path):
    os.rename(self.current_path + file_name, new_path + file_name)
    
  def execute(self,percentage,k):
    self.change_dir(["segmentations"])
    files = self.get_files()
    nr_elements = len(files)
    trainingset = random.sample(files,int(percentage*nr_elements))
    nr_training_samples = len(trainingset)
    print(nr_training_samples)
    
    testset = [x for x in files if x not in trainingset]
    nr_test_samples = len(testset)
    print(nr_test_samples)
    
    progress = nr_training_samples
    
    for tf in trainingset:
      if tf.endswith('.wav'):
	shutil.copy2("%s%s"%(self.current_path,tf),self.training_folder)
	progress = progress - 1
	print(progress)
    print("_____________\n")
    
    k_trainingset = random.sample(trainingset,int(k*nr_training_samples))
    nr_ktraining_samples = len(k_trainingset)
    progress = nr_ktraining_samples
    for k_tf in k_trainingset:
      if k_tf.endswith('.wav'):
	shutil.copy2("%s%s"%(self.current_path,k_tf),"%sk/"%(self.training_folder))
	#self.move_file(k_tf,"%s%s"%(self.training_folder,"k/"))
	progress = progress - 1
	print(progress)
    
    print("_____________\n")
    progress = nr_test_samples
    for tf in testset:
      if tf.endswith('.wav'):
	shutil.copy2("%s%s"%(self.current_path,tf),self.testing_folder)
	progress = progress - 1
	print(progress)
	
    self.change_dir([])