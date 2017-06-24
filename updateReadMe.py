"""
Script updates the readMe when new papers are added
"""
import os

linkPath="https://github.com/ZigaSajovic/Readings/tree/master/"

with open("README.md", "w") as f:
	with open("READMEtemplate.md", "r") as f2:
		for line in f2:
			print(line, file=f)
	print("",file=f)
	dirs=[dir_ for dir_ in os.walk("./") if "./.git" not in dir_[0] and dir_[0]!="./"]
	dirs.sort(key=lambda x: x[0][2:])
	link_=lambda pre, s1, s2:pre+" ["+s1+"]("+linkPath+s2+")"
	pdfNum=0
	for dir_ in dirs:
		dir=dir_[0][2:]
		subsection=link_("##", dir.replace("_", " "),dir)
		print(subsection+"\n", file=f)
		pdfNum+=len(dir_[2])
		for pdf_ in sorted(dir_[2]):
			pdf=pdf_
			if " " in pdf:
				pdf=pdf.replace(" ","_")
				os.rename(dir+"/"+pdf_,dir+"/"+pdf)
				print(dir+": Renamed "+pdf_+" -> "+pdf)
			if not pdf[0].isupper():
				pdfCap=pdf.capitalize()
				os.rename(dir+"/"+pdf,dir+"/"+pdfCap)
				print(dir+": Renamed "+pdf+" -> "+pdfCap)
				pdf=pdfCap
			listElement=link_("*",pdf.replace(".pdf","").replace("_"," "),dir+"/"+pdf)
			print(listElement, file=f)
		print("\n",file=f)
	print("ReadMe has been updated. Contains %d papers."%pdfNum)
