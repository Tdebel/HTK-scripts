import sys
import os

class GrammerCreator:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_path = self.local_folder
    self.transcriptions = []

  def get_files(self):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return files
  
  def transcribe(self,files):
    for f in files:
      if f.endswith('.wav'):
	words = f.split("_")
	for word in words:
	  if word.endswith('.wav'):
	    transcription = word[:-4]
	    self.transcriptions.append(transcription)
    
  def change_dir(self,folders):
    path = "%s/"%(self.local_folder)
    for folder in folders:
      path = "%s%s/"%(path,folder)
    os.chdir(path)
    self.current_path = path
    
  def make_grammer(self,filename):
    grammer_file = open(filename,'w')
    line1 = "$word = "
    for transcription in self.transcriptions:
      line1 = "%s%s | "%(line1,transcription) #.upper())
    line1 = "%s;"%(line1[:-3])
    line2 = "( SENT-START ( [silence] $word [silence] ) SENT-END )"
    grammer_file.write("%s\n"%(line1))
    grammer_file.write(line2)
    grammer_file.close()
    
  #def create(self):
    #print(self.current_path)
    #print("creating new file")
    #name=raw_input ("enter the name of file:")
    ##extension=raw_input ("enter extension of file:")
    #try:
        ##name=name+"."+extension
        #file=open(name,'a')
	#self.make_grammer(name)
        #file.close()
    #except:
            #print("error occured")
            #sys.exit(0)
    
  def execute(self,wav_file_folder):
    self.change_dir([wav_file_folder])
    files = self.get_files()
    self.transcribe(files)
    for transcription in self.transcriptions:
      print(transcription)
    self.change_dir([])
    #self.create()
    self.make_grammer("gram")
	
#gc = GrammerCreator()
#gc.execute("segmentations")
