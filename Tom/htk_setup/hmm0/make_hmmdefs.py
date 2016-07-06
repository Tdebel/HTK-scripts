import sys
import re
import os

class HmmdefsCreator():
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_folder = self.local_folder

  def execute(self):
    hmmdefs_file = open("hmmdefs","w")
    monophones_file = open("monophones0","r")
    proto_file = open("proto","r")
    phones = []
    hmm_section = ""
    for line in monophones_file:
      phone = line.rstrip('\n')
      phones.append(phone)
    for line in proto_file:
      if not line.startswith('~o') and not line.startswith('~h') and not line.startswith('<STREAMINFO>') and not line.startswith('<VECSIZE>'):
	hmm_section = hmm_section + line
  
    for phone in phones:
      line1 = "~h \"%s\"\n"%(phone)
      hmmdefs_file.write(line1)
      hmmdefs_file.write(hmm_section)
  
    hmmdefs_file.close()
    monophones_file.close()
    proto_file.close()
  
