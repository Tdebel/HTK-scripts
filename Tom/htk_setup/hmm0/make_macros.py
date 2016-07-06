import sys
import re
import os

class MacrosCreator():
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_folder = self.local_folder

  def execute(self):
    macros_file = open("macros","w")
    vFloors_file = open("vFloors","r")
    proto_file = open("proto","r")
    
    for line in proto_file:
      if line.startswith('~o') or line.startswith('<STREAMINFO>') or line.startswith('<VECSIZE>'):
	macros_file.write(line)
    
    for line in vFloors_file:
      macros_file.write(line)
      
    macros_file.close()
    vFloors_file.close()
    proto_file.close()
  
