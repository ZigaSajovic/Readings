import os
from argparse import ArgumentParser

parser = ArgumentParser(description="This script updates the README.md file and corrects file names.")
parser.add_argument("-g","--git",const=True, default=False,metavar="COMMIT_MSG",\
    nargs="?",help="If used, the script will add and commit to git, if README is changed.")
args = parser.parse_args()

linkPath="https://github.com/ZigaSajovic/Readings/tree/master/"

valid_files=["pdf","txt","ipynb", "djvu"]
forbiden=[".git","./",".ipynb_checkpoints"]
silent=[".silent",".asFile",".noExpand"]
asFile=[".asFile"]
noExpand_=[".noExpand"]

file_list=".fileList"
readMe="README.md"

commit_msg=args.git if isinstance(args.git,str) else "Automated commit."


def fix_git(new_name, old_name, new_=True, old_=True, force=False, make_note=True):
  if make_note:
    print(new_name, file=f2)
  change=old_name not in files or new_!=old_
  if old_name not in files or force:
    git_commands["add"].append(new_name)
  elif new_!=old_:
    git_commands["rm"].append(old_name)
    git_commands["add"].append(new_name)
  if old_name in files:
    files.remove(old_name)
  return change


def directoryDescent(pwd="./",depths=[0], noExpand=False):
  pdfNum=0
  change=False
  dir__=next(os.walk(pwd))
  dirs=sorted([dir_ for dir_ in dir__[1] if dir_ not in forbiden])
  noExpand=noExpand or any(map(lambda x:x in noExpand_,dir__[2]))
  isSilent=any(map(lambda x:x in silent,dir__[2]))
  link_=lambda pre, s1, s2:pre+" ["+s1+"]("+linkPath+s2+")"
  readMe_path_=os.path.join(pwd,readMe)
  create_readme= (not noExpand) and dir__[0] not in forbiden
  if create_readme:
    # print(dir__[0].split(os.sep)[-1], readMe_path_)
    _files.append(open(readMe_path_,"w"))

  if dir__[0] not in forbiden:
    dirs=sorted(dirs)
    this_dir=dir__[0].split(os.sep)[-1]
    url_dir=os.sep.join(dir__[0].split(os.sep)[1:])
    as_file=any(map(lambda x:x in asFile,dir__[2]))
    if not noExpand:
      for _f,depth in zip(_files,depths):
        sbs=link_(("\t"*max(depth-2,0))+"*", ("__" if not as_file else "")+this_dir.replace("_", " ")\
                                    +("__" if not as_file else ""),url_dir) if depth >1 else\
                                    link_(("\t"*(depth-1))+"#"*(depth+1), this_dir.replace("_", " "),url_dir)
        print(sbs, file=_f)

    fs_=[d for d in dir__[2] if d.split(".")[-1] in valid_files]
    pdfNum+=len(fs_)
    for f_ in sorted(fs_):
      pdf=f_
      pdfCap="-".join(map(lambda x:x[0:1].capitalize()+x[1:],("_".join(map(lambda x:x[0:1].capitalize()+x[1:] ,"_".join(pdf.lower().split()).split("_")))).split("-")))
      pdfCap=pdfCap[0:1].capitalize()+pdfCap[1:]
      if pdfCap!=pdf:
        os.rename(os.path.join(dir__[0],pdf),os.path.join(dir__[0],pdfCap))
        print(dir__[0]+": Renamed "+pdf+" -> "+pdfCap)
      if not isSilent:
        for _f,depth in zip(_files,depths):
          listElement=link_(("\t"*(depth-1))+"*",pdfCap.replace(".pdf","").replace("_"," "),os.path.join(url_dir,pdfCap))
          print(listElement, file=_f)
      #print(this_dir, not noExpand, 1 if args.git else 2, "AAA")
      if args.git and not noExpand:
        change= fix_git(os.path.join(dir__[0],pdfCap),os.path.join(dir__[0],pdf),pdfCap,pdf) or change
  for d in dirs:
    try:
      pdfNum_, change_=directoryDescent(os.path.join(pwd,d), depths=list(map(lambda x:x+1,depths))+[1], noExpand=noExpand)
      change=change or change_
      pdfNum+=pdfNum_
    finally:
      pass      
  if create_readme:
    if change:
      fix_git(readMe_path_, readMe_path_, force=True, make_note=False)
    _files.pop().close()
  return pdfNum, change

try:
  with open(file_list,"r") as f:
    files=set(line.strip() for line in f)
except FileNotFoundError:
  files=set()

git_commands={"rm":[],"add":[]}

readMe_files=[readMe]

f = open("README.md", "w")
_files=[f]
with open("READMEtemplate.md", "r") as f2:
  for line in f2:
    print(line, file=f)
print("",file=f)
if args.git:
  f2=open(file_list, "w")
  try:
    pdfNum, change=directoryDescent()
  finally:
    f2.close()
else:
  pdfNum, change =directoryDescent()

_files.pop().close()

assert not len(_files), "Error: some files still open"

if change:
  git_commands["add"].append(readMe)

if args.git:
  for file in files:
    git_commands["rm"].append(file)
  import subprocess as sp
  for command in git_commands:
    for file in git_commands[command]:
      sp.call(["git", command, file])
  if change:
    sp.call(["git", "commit", "-m", commit_msg])
    print("Changes have been committed, ReadMe has been updated. Contains %d papers."%pdfNum)
  else:
    print("No changes to commit. Contains %d papers."%pdfNum)
else:
  print("ReadMe updated. Contains %d papers."%pdfNum)