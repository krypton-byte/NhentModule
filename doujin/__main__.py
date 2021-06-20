import sys
from .Dwrapper import nhentai
import os
import argparse
name=os.path.dirname(__file__).split('/')[-1]
parser=argparse.ArgumentParser(prog=f"python -m {name}", description="doujin wrapper")
parser.add_argument("--nuklir", help="Nhentai Code")
parser.add_argument("--output", help="File")
args=parser.parse_args()
if args.nuklir:
    try:
        d=nhentai(args.nuklir).doujin
        print(f"title: {d.title}")
        print(f"number of sheets: {d.images.__len__()} sheet")
        sys.stdout.write("\rstatus: Dowloading ...")
        d.save_to_file(args.output if args.output else d.title)
        filename = args.output or d.title
        sys.stdout.flush()
        sys.stdout.write("\rstatus: Dowloaded      \n")
        sys.stdout.flush()
        print(f"Save as {filename}{'' if filename[-4:]=='.pdf' else '.pdf'}")
    except Exception:
        print("Invalid Code")
else:
    print(f"Try `python -m {name} -h' for more information.")
