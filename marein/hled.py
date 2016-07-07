import os, re
import argparse
import subprocess

def make_led(fn,s):
    with open(fn,'w') as f:
        f.write('EX\n')
        if not s:
            f.write('IS sil sil\n')
            f.write('DE sp\n')

def hled(outfile,dictfile,wordsfile,s):
    ledfile = 'hled_temp.led'
    make_led(ledfile,s)
    subprocess.call(['HLEd', '-l', '*', '-d', dictfile, '-i', outfile, ledfile, wordsfile])
    os.remove(ledfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the required mlf edits.')
    parser.add_argument('outfile', type=str)
    parser.add_argument('dict', type=str)
    parser.add_argument('words', type=str)
    parser.add_argument('-s', type=bool,help='Do not execute the sil and sp edits - only expand the words into phonemes.')
    args = parser.parse_args()
    hled(args.outfile,args.dict,args.words,args.s)
