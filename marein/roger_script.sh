INFILES=../../material/segmentations
WORDS=data/words.txt
DICT=data/current_wordlist.txt
python gram.py gram --folder $INFILES --regex "cut_\d*_\d*_(\w*).wav"
HParse gram wdnet
cat $WORDS | LC_ALL=C sort | uniq > wlist
cat $DICT | LC_ALL=C sort | uniq | sed -e 's/\t/\t1\t/' > ordered_dict
HDMan -m -w wlist -n monophones -i dict ordered_dict
python mlf.py mlf --folder $INFILES --regex "cut_\d*_\d*_(\w*).wav"
python hcopy.py $INFILES mfc
python proto.py proto
cat hcopy_temp.scp | cut -d " " -f 2 > hcompv_temp.scp
python hcompv.py proto hcompv_temp.scp hmmdef0
python hled.py phones.mlf ordered_dict mlf
