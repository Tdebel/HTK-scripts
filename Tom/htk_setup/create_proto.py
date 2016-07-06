import sys
import re
import os

class ProtoCreator:
  
  def __init__(self):
    self.local_folder = os.path.dirname(os.path.abspath(__file__))
     
  def repeat_to_length(self,sentence, amount):
    altered_sentence = sentence * amount
    return altered_sentence

  def execute(self,vec_length,targetkind):
    proto_file = open("proto", "w")
    proto_file.write("~o <VecSize> %s <%s>\n"%(vec_length,targetkind))
    proto_file.write("~h \"proto\"\n")
    proto_file.write("<BeginHMM>\n")
    proto_file.write("\t<NumStates> 5\n")
    proto_file.write("\t<State> 2\n")
    proto_file.write("\t\t<Mean> %s\n"%(vec_length))
    proto_file.write("\t\t\t%s\n"%(self.repeat_to_length("0.0 ",vec_length)))
    proto_file.write("\t\t<Variance> %s\n"%(vec_length))
    proto_file.write("\t\t\t%s\n"%(self.repeat_to_length("1.0 ",vec_length)))
    proto_file.write("\t<State> 3\n")
    proto_file.write("\t\t<Mean> %s\n"%(vec_length))
    proto_file.write("\t\t\t%s\n"%(self.repeat_to_length("0.0 ",vec_length)))
    proto_file.write("\t\t<Variance> %s\n"%(vec_length))
    proto_file.write("\t\t\t%s\n"%(self.repeat_to_length("1.0 ",vec_length)))
    proto_file.write("\t<State> 4\n")
    proto_file.write("\t\t<Mean> %s\n"%(vec_length))
    proto_file.write("\t\t\t%s\n"%(self.repeat_to_length("0.0 ",vec_length)))
    proto_file.write("\t\t<Variance> %s\n"%(vec_length))
    proto_file.write("\t\t\t%s\n"%(self.repeat_to_length("1.0 ",vec_length)))
    proto_file.write("\t<TransP> 5\n")
    proto_file.write("\t\t0.0 1.0 0.0 0.0 0.0\n")
    proto_file.write("\t\t0.0 0.6 0.4 0.0 0.0\n")
    proto_file.write("\t\t0.0 0.0 0.6 0.4 0.0\n")
    proto_file.write("\t\t0.0 0.0 0.0 0.7 0.3\n")
    proto_file.write("\t\t0.0 0.0 0.0 0.0 0.0\n")
    proto_file.write("<EndHMM>\n")
    proto_file.close()

#execute(39,"MFCC_0_D_A")