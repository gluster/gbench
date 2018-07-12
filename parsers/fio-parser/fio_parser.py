'''
Fio commands

Large file, sequential I/O workloads
====================================

* fio --name=writetest --ioengine=sync --rw=write --direct=0 --create_on_open=1
--fsync_on_close=1 --bs=128k --directory=<test-dir-gluster>
--filesize=16g --size=16g --numjobs=4 --minimal > outputFioSeqWrite.csv

* sync; echo 3 > /proc/sys/vm/drop_caches # on clients, then on servers

* fio --name=readtest --ioengine=sync --rw=read --direct=0 --bs=128k
--directory=<test-dir-gluster> --filesize=16g --size=16g --numjobs=4 --minimal
> outputFioSeqRead.csv


Important data
==============

5	Total I/O (KB)
6	bandwidth (KB/s)
7	IOPS
8	runtime (ms)
44      Completion latency mean
Bandwidth mean
read_data = [6, 7, 8, 9, 16, 45], columns from csv

46	Total I/O (KB)
47	bandwidth (KB/s)
48	IOPS
46	runtime (ms)
57      Completion latency mean
85      Bandwidth mean
write_data = [47, 48, 49, 50, 57, 86], columns from csv

Code variable explanation
=========================

job_name = cells[2], column from csv
data = {jobName:[write_row_numbers], jobname:[read_row_numbers]}
example:
data = {'readtest': [108676, 17992, 140, 58277, 7102.775, 17748, 613505]
'''
import argparse
import csv

def get_data(file_path):
    '''
    accepts columns that are to be extracted from the given csv file and
    returns the dictionary with job name as key and important data (included
    columns) as value
    '''
    included_cols_read = [5, 6, 7, 8, 15, 44]
    included_cols_write = [46, 47, 48, 49, 56, 85]
    inventory = dict()
    data = list()
    counter = '0'
    try:
        with open(file_path, "r") as file_object:
            file_reader = csv.reader(file_object, delimiter=';')
            for row in file_reader:
                if row[5] != '0':
                    for each_column in included_cols_read:
                        data.append(row[each_column])
                    counter = str(int(counter)+1)
                    inventory[row[2]+counter] = data
                if row[46] != '0':
                    for each_column in included_cols_write:
                        data.append(row[each_column])
                    counter = str(int(counter)+1)
                    inventory[row[2]+counter] = data
                data = []
        return inventory
    except IOError:
        print("File not found")

def write_file(inventory, filename):
    '''
    takes dictionary as input and writes it in a csv file of given name
    '''
    with open(filename, 'w+') as csv_file:
        for key in inventory:
            row = key+',' + ','.join(inventory[key])+'\n'
            csv_file.write(row)


def main():
    '''
    * takes file name as an argument
    * passes included columns with other parameters
    * prints data
    '''
    input_help = 'fio output dump file'
    output_help = 'parse and store data in this file name'

    parser = argparse.ArgumentParser(description='fio Parser(--minimal or --output-format = terse)')
    parser.add_argument('-i', '--input', type=str, help=input_help)
    parser.add_argument('-o', '--output', type=str, help=output_help)
    args = parser.parse_args()
    result = get_data(args.input)
    if result and args.output:
        write_file(result, args.output)
    elif result:
        print(result)

if __name__ == '__main__':
    main()
