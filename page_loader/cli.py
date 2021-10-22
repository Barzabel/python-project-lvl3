import argparse
import os

def parser_argument():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output',
                        type=str,
                        default=os.getcwd(),
                        help='output dir (default: current directory)')
    args = parser.parse_args()
    return args
