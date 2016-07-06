import os
import argparse
import subprocess

# write a hcopy config file to filename based on args
def macro(args):
    vfloors = open(args.protodir + "/vFloors", 'r')
    proto = open(args.protodir + "/proto", 'r')
    macros = open(args.outdir + "/macros", 'w')
    proto_global = proto.read().splitlines()[:3]
    macros.write("\n".join(proto_global))
    macros.write("\n" + vfloors.read())

def hmmdefs(args):
    hmmdefs = open(args.outdir + "/hmmdefs", 'w')
    monophones = open(args.monophones, 'r')
    proto = open(args.protodir + "/proto", 'r')
    
    mono_list = monophones.read().splitlines()
    proto_temp = proto.read().splitlines()[4:]
    
    for phone in mono_list:
        hmmdefs.write("~h \"" + phone + "\"\n")
	hmmdefs.write("\n".join(proto_temp) + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('outdir', help='Dir to write HMMdefs and macro', nargs='?', default="hmm0")
    parser.add_argument('monophones', help='file with the list of monophones', nargs='?',default="monophones")
    parser.add_argument('protodir', help='Dir to the proto and vfloors files', nargs='?', default="hmmdef0")
    args = parser.parse_args()
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    hmmdefs(args)
    macro(args)
