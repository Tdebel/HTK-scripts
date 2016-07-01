import os
import argparse
import subprocess

def hcompv(args):
    config_file = 'hcopy_temp.config'
    subprocess.call('HCompV', '-C', config_file, '-f', args.floor, '-m', '-S', args.script, '-H', args.outdir, args.proto)
    os.remove(config_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('proto', help='The initial prototype file.')
    parser.add_argument('script', help='Script file (.scp).')
    parser.add_argument('outdir', help='Dir to write HMM macro files.')
    parser.add_argument('-k', '--targetkind', nargs='?', default='MFCC_0_D', type=str)
    parser.add_argument('-r', '--targetrate', nargs='?', default=100000.0, type=float)
    parser.add_argument('-c', '--compressed', nargs='?', default='T', choices=['T','F'])
    parser.add_argument('-f', '--floor', nargs='?', default=0.01, type=float)
    parser.add_argument('-m', '--means', default=True, action='store_true')
    args = parser.parse_args()
    hcompv(args)
