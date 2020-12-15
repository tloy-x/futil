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
parser.add_argument('-a', "--aa", action="store_true") #monolithic help

rename_parser = subparsers.add_parser("rename", help="rename files", usage="futil.py [-d] rename filetype newname [-p]")
rename_parser.add_argument("filetype", type=str)
rename_parser.add_argument("newname", type=str)
rename_parser.add_argument("-p", "--placeholder", type=int, metavar="<int>", help='number of placeholder digits. default is 4, maximum is 10')

create_parser = subparsers.add_parser("create", help="create files", usage="futil.py [-d] create [-t] filetype name amount")
create_parser.add_argument("filetype", type=str)
create_parser.add_argument("name", type=str)
create_parser.add_argument("amount", type=int, help='number of files to create')
create_parser.add_argument("-p", "--placeholder", type=int, metavar="<int>", help='number of placeholder digits. default is 4, maximum is 10')
create_parser.add_argument("-t", "--template", action="store_true", help="define a template file")

remove_parser = subparsers.add_parser("remove", help="remove files", usage="futil.py [-d] remove filetype")
remove_parser.add_argument("filetype", type=str)

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    exit(0)

args = parser.parse_args()

if args.aa:
    parser.print_help(sys.stdout)
    subparsers_actions = [
        action for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)]

    for subparsers_action in subparsers_actions:
        for choice, subparser in subparsers_action.choices.items():
            print('{}'.format(choice))
            print(subparser.format_help())
    exit(1)

if args.filetype[0] == '.' and args.filetype is not None:
    args.filetype = args.filetype[1:]

if args.directory is not None:
    if not os.path.exists(args.directory):
        parser.error(f"Path {args.directory} does not exist.")
    else:
        os.chdir(args.directory)
else:
    args.directory = os.getcwd()
    os.chdir(os.getcwd())

if args.command == 'rename' or args.command == 'create':
    if args.placeholder is None:
        args.placeholder = 4
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
    for x in range(args.amount):
        filenum = str(x).zfill(args.placeholder)
        file = args.name + str(filenum) + '.' + args.filetype
        f = open(file, "w")
        f.close()
        if args.verbose:
            print(f'Creating {file}...')
    print("Done.")

if args.command == 'remove':
    for file in files:
        os.remove(file)
        if args.verbose:
            print(f"Removing {file}...")
    print("Done.")