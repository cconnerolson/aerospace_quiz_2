"""ME 4267 Take-home Quiz 2:

Usage:
	cli.py -f FILE

Options:
	-h, --help       Show this screen.
	-v --version     Show version.
	-f FILE, --inputfile FILE  Specify custom filename for input file. [default: input.file]
 
"""
from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__, version='Quiz 2 0.1.1')
	