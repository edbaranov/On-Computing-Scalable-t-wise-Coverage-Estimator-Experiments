import os
import sys
import argparse

def convert_sa(filename, outfilename):
    with open(filename)  as f:
        lines = f.readlines()
        newlines  = []
        for i in range(min(len(lines),1000)):
            els = lines[i].strip().split(' ')
            j=1
            nl = str(i+1) + ', '
            for el in els:
                if el =='0':
                    nl += str(-j) + ' '
                else:
                    nl += str(j) + ' '
                j+=1
            newlines.append(nl + '\n')
        with open(outfilename, 'w+') as fi:
            for line in newlines:
                fi.write(line)

def convert_cmsgen(filename, outfilename):
    with open(filename)  as f:
        lines = f.readlines()
        newlines  = []
        for i in range(len(lines)):
            newlines.append(str(i) + ', ' + lines[i][:-3] + '\n')
        with open(outfilename, 'w+') as fi:
            for line in newlines:
               fi.write(line)
                

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--tool", type=str, default="SamplingCA", help="Tool, accepted inputs samplingca, ls-sampling, cmsgen", dest='tool')
    parser.add_argument("--outputfile", type=str, default="", help="output file, default <inputfile>.samples", dest='outputfile')
    parser.add_argument('inputfile', type=str, help='input file to convert')
    args = parser.parse_args()
    if args.tool not in ["samplingca", "ls-sampling", "cmsgen"]:
        print("Tool must be one of the following list: samplingca, ls-sampling, cmsgen")
        sys.exit(1)
    outfile = args.outputfile if args.outputfile else args.inputfile + ".samples"
    if args.tool == "samplingca":
        convert_sa(args.inputfile, outfile)
    elif args.tool == "ls-sampling":
        convert_sa(args.inputfile, outfile)
    else:
        convert_cmsgen(args.inputfile, outfile)

if __name__== "__main__":
    main()
