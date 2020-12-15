#/usr/bin/python3
#futil v1.0

import os
import glob
import sys
import argparse

parser = argparse.ArgumentParser(usage="futil.py [-h] [-d] {rename, create, remove} ...")
subparsers = parser.add_subparsers(help="functions", dest="command")

parser.add_argument('-d','--directory', type=str, metavar='<directory>', help='specify a directory. Default is current working directory')
parser.add_argument('-v', '--verbose', action='store_true', help='toggle verbose output')
parser.add_argument('-V', '--version', action='version', version='%(prog)s 1.0', help='show program\'s version number and exit')

rename_parser = subparsers.add_parser("rename", help="rename files", usage="futil.py [-d] rename [-h] filetype newname [-p]")
rename_parser.add_argument("filetype", type=str, help="filetype of file(s) to rename")
rename_parser.add_argument("newname", type=str, help="new name of file(s) to rename")
rename_parser.add_argument("-p", "--placeholder", type=int, metavar="<int>", help='number of placeholder digits. default is 4, maximum is 10')

create_parser = subparsers.add_parser("create", help="create files", usage="futil.py [-d] create [-h] [-t] filetype name amount")
create_parser.add_argument("filetype", type=str)
create_parser.add_argument("name", type=str, help="name of file(s)")
create_parser.add_argument("amount", type=int, help='number of files to create')
create_parser.add_argument("-p", "--placeholder", type=int, metavar="<int>", help='number of placeholder digits. default is 4, maximum is 10')
create_parser.add_argument("-t", "--template", type=str, metavar="<template file>", help="define a template file")

remove_parser = subparsers.add_parser("remove", help="remove files", usage="futil.py [-d] remove [-h]  filetype")
remove_parser.add_argument("filetype", type=str, help="filetype of files to remove")

if len(sys.argv) == 1: #if no args, print help message
    parser.print_help(sys.stderr)
    exit(0) #exit with code 0

args = parser.parse_args() #parse arguments into ns args

if args.filetype[0] == '.' and args.filetype is not None: #parsing for filetype. if "." in filetype, remove.
    args.filetype = args.filetype[1:]

if args.directory is not None: #check if path exists
    if not os.path.exists(args.directory):
        parser.error(f"Path {args.directory} does not exist.")
    else:
        os.chdir(args.directory)
else:
    args.directory = os.getcwd()
    os.chdir(os.getcwd())

#if args.command == 'rename' or args.command == 'create' or args.command == 'remove' and len(sys.argv == 2):
#    parser.print_help(sys.stderr)
#    exit(0)

if args.command == 'rename' or args.command == 'create': #range checking
    if args.placeholder is None:
        args.placeholder = 4 #default is 4
    elif args.placeholder > 10:
        parser.error("Placeholder must be less than 10.")
        exit(2)
    elif args.placeholder < 0:
        parser.error("Placeholder must be less than 10.")
        exit(2)

files = []
count = 0

for a in glob.glob('*.' + args.filetype):
    files.append(a)  

if args.command == 'rename':
    if files:
        for i in files:
            file2 = args.newname + str(count).zfill(args.placeholder) + '.' + args.filetype
            os.rename(i, file2)
            if args.verbose:
                print(f"Renaming {i} to {file2}...")
            count += 1
        print("Done.")
    else:
        parser.error("No files found")   
        exit(1)

if args.command == 'create':
    if args.template: 
        if not os.path.exists(args.template): #catch for template file not existing
            parser.error("Template file does not exist.")
            exit(1)
        with open(args.template) as t:
            for x in range(args.amount):
                filenum = str(x).zfill(args.placeholder)
                if args.placeholder == 0 and args.amount == 1: #catch for single file 
                    file = args.name + '.' + args.filetype
                else:
                    file = args.name + str(filenum) + '.' + args.filetype
                f = open(file, "w")
                for line in t:
                    f.write(line)
                f.close()
                if args.verbose:
                    print(f"Creating {file} from template {t}...")
            print("Done.")
        t.close()
    else:
        for x in range(args.amount):
            filenum = str(x).zfill(args.placeholder)
            if args.placeholder == 0:
                file = args.name + '.' + args.filetype
            else:
                file = args.name + str(filenum) + '.' + args.filetype
            f = open(file, "w")
            f.close()
            if args.verbose:
                print(f'Creating {file}...')
            print("Done.")

        f.close()

if args.command == 'remove':
    for file in files:
        os.remove(file)
        if args.verbose:
            print(f"Removing {file}...")
    print("Done.")