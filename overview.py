import os
import PyPDF2 as pyPdf
dirs=[dir_ for dir_ in os.walk("./") if "./.git" not in dir_[0] and dir_[0]!="./"]
sum=0
for d in dirs:
  if "Compilers" in d[0]:
    continue
  fls=0
  pgs=0
  for f in d[2]:
    p=d[0]+"/"+f
    if f[-3:]=="pdf":
      pdf=pyPdf.PdfFileReader(open(p,'rb'))
      pgs+=pdf.getNumPages()
      fls+=1
  sum+=pgs
  print("%s:\n%d papers, %d pages\n---"%(d[0].split("/")[-1].replace("_", " "),fls,pgs))
print("Total count: Directory contains %d pages of pdf documents"%sum)
