#!/usr/bin/python3
'''
This program is for smallFile, parses the output and puts important numbers in a
csv file.

usage: parse.py [-h] [-i INPUT] [-o OUTPUT]

SmallFile Parser

optional arguments:
  -h, --help                 :  show this help message and exit
  -i INPUT, --input INPUT    :  smallfile output [path] file name
  -o OUTPUT, --output OUTPUT :  export parsed result in a file (csv) of the name
'''
import re
import argparse
import csv
import os.path

def shred_digit(line):
    '''
    This function fetches numbers from a line
    '''
    return re.findall(r'\d+.\d+', line)

def find_pattern(file_name):
    '''
    This function is to get numbers by filtering pattern
    '''
    attr = []
    with open(file_name) as fobj:
        data_file = fobj.read().split("\n")
        for line in data_file:
            if re.match('^total data', line):
                attr.append(shred_digit(line)[0])

            elif re.match('^files/sec', line):
                attr.append(shred_digit(line)[0])

            elif re.match('^IOPS', line):
                attr.append(shred_digit(line)[0])

            elif re.match('^MiB/sec', line):
                attr.append(shred_digit(line)[0])
    return attr
def write_to_csv(numbers, fname):
    '''
    this function writes a given list in csv file
    '''
    fname = fname + ".csv"
    with open(fname, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(numbers)

def main():
    '''
    Main function that checks the argument and performs accordingly
    '''
    input_help = 'smallfile output file name'
    output_help = 'export parsed result in a file (csv) of this name.'

    header = ['Total Data', 'Files/sec', 'IOPS', 'MiB/sec']

    parser = argparse.ArgumentParser(description='SmallFile Parser')
    parser.add_argument('-i', '--input', type=str, help=input_help)
    parser.add_argument('-o', '--output', type=str, help=output_help)
    args = parser.parse_args()

    if args.input and os.path.isfile(args.input):
        result = find_pattern(args.input)
        print(result)
        if args.output:
            if os.path.isfile(args.output+".csv"):
                write_to_csv(result, args.output)
            else:
                write_to_csv(header, args.output)
                write_to_csv(result, args.output)
        else:
            print(result)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
