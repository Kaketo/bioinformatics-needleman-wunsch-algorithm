from src.needleman_wunch import needleman_wunch_alghoritm
from src.files_handling import *
import argparse
parser = argparse.ArgumentParser(description='Needleman Wunch Alghoritm Program')
parser.add_argument('-a', '--a_sequence', help='First sequence in FASTA format')
parser.add_argument('-b', '--b_sequence', help='Second sequence in FASTA format')
parser.add_argument('-c', '--config', help='File with configuration', default='config.txt')
parser.add_argument('-o', '--output', help='File to save results', default='output.txt')

args = parser.parse_args()

# Read sequences and config
config = read_config(args.config)
A = read_sequence(args.a_sequence, config['MAX_SEQ_LEN'])
B = read_sequence(args.b_sequence, config['MAX_SEQ_LEN'])


# Get Needleman-Wunch alghoritm results
score, paths = needleman_wunch_alghoritm(A,B,
        max_number_paths = config['MAX_NUMBER_PATHS'], 
        match_score = config['SAME'], 
        miss_score = config['DIFF'], 
        gap_penalty = config['GAP_PENALTY'])

# Write results to output file
f = open(args.output,"w+")
f.write('SCORE = ' + '%1.0f' % score + '\n\n')
for path in paths:
     f.write(str(path[0]) + '\n' + str(path[1]) + '\n\n')
f.close()