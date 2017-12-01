"""
Script updates the readMe when new papers are added
"""
import os

linkPath="https://github.com/ZigaSajovic/Readings/tree/master/"

valid_files=["pdf","txt","ipynb"]
forbiden=[".git","./",".ipynb_checkpoints"]
silent=[".silent",".asFile",".noExpand"]
asFile=[".asFile"]
noExpand_=[".noExpand"]

def directoryDescent(pwd="./",depth=0, noExpand=False):
  pdfNum=0
  dir__=next(os.walk(pwd))
  dirs=[dir_ for dir_ in dir__[1] if dir_ not in forbiden]
  dirs=sorted(dirs)
  noExpand=noExpand or any(map(lambda x:x in noExpand_,dir__[2]))
  isSilent=any(map(lambda x:x in silent,dir__[2]))
  link_=lambda pre, s1, s2:pre+" ["+s1+"]("+linkPath+s2+")"
  if dir__[0] not in forbiden:
    this_dir=dir__[0].split("/")[-1]
    url_dir="/".join(dir__[0].split("/")[1:])
    as_file=any(map(lambda x:x in asFile,dir__[2]))
    if depth>1:
      subsection=link_(("\t"*max(depth-2,0))+"*", ("__" if not as_file else "")+this_dir.replace("_", " ")+("__" if not as_file else ""),url_dir)
    else:
      subsection=link_(("\t"*(depth-1))+"#"*(depth+1), this_dir.replace("_", " "),url_dir)
    if not noExpand:
      print(subsection,file=f)
    fs_=[d for d in dir__[2] if d.split(".")[-1] in valid_files]
    pdfNum+=len(fs_)
    for f_ in sorted(fs_):
      pdf=f_
      pdfCap="_".join(map(lambda x:x[0:1].capitalize()+x[1:],("_".join(map(lambda x:x[0:1].capitalize()+x[1:] ,pdf.lower().replace(" ","_").split("_")))).split("-")))
      pdfCap=pdfCap[0:1].capitalize()+pdfCap[1:]
      if pdfCap!=pdf:
        os.rename(os.path.join(dir__[0],pdf),os.path.join(dir__[0],pdfCap))
        print(dir__[0]+": Renamed "+pdf+" -> "+pdfCap)
        pdf=pdfCap
      if not isSilent:
        listElement=link_(("\t"*(depth-1))+"*",pdf.replace(".pdf","").replace("_"," "),os.path.join(url_dir,pdf))
        print(listElement, file=f)
  for d in dirs:
    pdfNum+=directoryDescent(os.path.join(pwd,d), depth=depth+1, noExpand=noExpand)
  return pdfNum

with open("README.md", "w") as f:
  with open("READMEtemplate.md", "r") as f2:
    for line in f2:
      print(line, file=f)
  print("",file=f)
  pdfNum=directoryDescent()
  print("ReadMe has been updated. Contains %d papers."%pdfNum)