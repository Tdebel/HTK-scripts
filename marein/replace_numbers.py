import sys

with open(sys.argv[1]) as f:
    text = f.read()
    for i,c in zip(range(10),'abcdefghij'):
        text = text.replace(str(i),'n{}'.format(c))

with open(sys.argv[1],'w') as f:
    f.write(text)
