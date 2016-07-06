import sys
import os
import subprocess
from re_estimating import *
from silence_model import *
from coding_data import *
from evaluate import *
sys.path.append('/home/tomjan/WORK/STUDENTASSISTENTEN_CLSM/TOM/HTK_lesson_(English_AM)/option1/hmm0/')
sys.path.append('/home/tomjan/WORK/STUDENTASSISTENTEN_CLSM/TOM/HTK_lesson_(English_AM)/initial_setup/testing/')
from make_hmmdefs import *
from make_macros import *
#from prompt2testmlf import *
from prompt2mlf import *

class MonophoneCreator:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
    self.current_folder = self.local_folder
    
  def change_dir(self,folders):
    path = "%s/"%(self.local_folder)
    for folder in folders:
      path = "%s%s/"%(path,folder)
    os.chdir(path)
    self.current_path = path
    
  def execute(self):
    self.change_dir(["hmm0"])
    hc = HmmdefsCreator()
    hc.execute()
    mc = MacrosCreator()
    mc.execute()
    self.change_dir([])
    re = ReEstimator()
    re.execute(1,3)
    sl = Silencer()
    sl.execute(4)
    re.execute(6,7)
    tdc = TestDataCoder()
    tdc.execute()
    mf = Mlfifier()
    mf.prompt2mlf("testref.mlf","testing")
    #tmc = TestMlfCreator()
    #tmc.prompt2mlf("testref.mlf")
    ev = Evaluator()
    ev.execute(7)
    
mc = MonophoneCreator()
mc.execute()