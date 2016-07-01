### hcopy.py (step 5)

Given input and output directories, convert the input to .mfc files based on
the arguments.

usage: hcopy.py [-h] [-k [TARGETKIND]] [-r [TARGETRATE]] [-c [{T,F}]]
                indir outdir

### proto.py (step 6)

Create a HTK prototype file based on parameters.

usage: proto.py [-h] [-n [NAME]] [-k [TARGETKIND]] [-v [VECSIZE]]
                [-s [STATES]] [-t [TRANSKERNEL [TRANSKERNEL ...]]]
                outfile

### hcompv.py (step 6)

Given input prototype and an output directory, create an output protoype and floored variance file.

usage: hcompv.py [-h] [-k [TARGETKIND]] [-r [TARGETRATE]] [-c [{T,F}]]
                 [-f [FLOOR]] [-m]
                 proto script outdir

