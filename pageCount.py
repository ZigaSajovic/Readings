import os
import pyPdf
dirs=[dir_ for dir_ in os.walk("./") if "./.git" not in dir_[0] and dir_[0]!="./"]
sum=0
for d in dirs:
 if "Compilers" in d[0]:
  continue
 for f in d[2]:
  p=d[0]+"/"+f
  if f[-3:]=="pdf":
   pdf=pyPdf.PdfFileReader(open(p,'rb'))
   sum+=pdf.getNumPages()
print("Directory contains %d pages of pdf documents"%sum)
