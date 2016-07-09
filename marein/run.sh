# example of running prepare, train and test in sequence

python prepare.py ../../material/segmentations mfc "cut_\d*_\d*_(\w*).wav" input/config input/current_wordlist.txt
python train.py htk scp ordered_dict input/proto words.mlf monophones input/config
python test.py htk/htk5 wdnet dict monophones scp2 phones.mlf
