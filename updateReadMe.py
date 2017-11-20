"""
Script updates the readMe when new papers are added
"""
import os

linkPath="https://github.com/ZigaSajovic/Readings/tree/master/"

valid_files=["pdf","txt"]
forbiden=[".git","./"]
silent=[".silent"]
ignore=[".ignoreIt"]

def directoryDescent(pwd="./",depth=0):
  pdfNum=0
  dir__=next(os.walk(pwd))
  dirs=[dir_ for dir_ in dir__[1] if dir_ not in forbiden]
  dirs=sorted(dirs)
  link_=lambda pre, s1, s2:pre+" ["+s1+"]("+linkPath+s2+")"
  if dir__[0] not in forbiden:
    this_dir=dir__[0].split("/")[-1]
    url_dir="/".join(dir__[0].split("/")[1:])
    toBeIgnored=any(map(lambda x:x in ignore,dir__[2]))
    if toBeIgnored:
      return 0
    isSilent=any(map(lambda x:x in silent,dir__[2]))
    if isSilent:
    	subsection=link_(("\t"*max(depth-2,0))+"*", "__"+this_dir.replace("_", " ")+"__",url_dir)
    else:
	    subsection=link_(("\t"*(depth-1))+"#"*(depth+1), this_dir.replace("_", " "),url_dir)
    print(subsection,file=f)
    fs_=[d for d in dir__[2] if d.split(".")[-1] in valid_files]
    pdfNum+=len(fs_)
    for f_ in sorted(fs_):
      pdf=f_
      if " " in pdf:
        pdf=pdf.replace(" ","_")
        os.rename(os.path.join(dir__[0],f_),os.path.join(dir__[0],pdf))
        print(dir__[0]+": Renamed "+f_+" -> "+pdf)
      if not pdf[0].isupper():
        pdfCap=pdf.capitalize()
        os.rename(os.path.join(dir__[0],pdf),os.path.join(dir__[0],pdfCap))
        print(dir__[0]+": Renamed "+pdf+" -> "+pdfCap)
        pdf=pdfCap
      if not isSilent:
      	listElement=link_(("\t"*(depth-1))+"*",pdf.replace(".pdf","").replace("_"," "),os.path.join(url_dir,pdf))
      	print(listElement, file=f)
  for d in dirs:
    pdfNum+=directoryDescent(os.path.join(pwd,d), depth=depth+1)
  return pdfNum

with open("README.md", "w") as f:
  with open("READMEtemplate.md", "r") as f2:
    for line in f2:
      print(line, file=f)
  print("",file=f)
  pdfNum=directoryDescent()
  print("ReadMe has been updated. Contains %d papers."%pdfNum)
