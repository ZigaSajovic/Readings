import os

linkPath="https://github.com/ZigaSajovic/Readings/tree/master/"

with open("README.md", "w") as f:
	with open("READMEtemplate.md", "r") as f2:
		for line in f2:
			print(line, file=f)
	print("",file=f)
	dirs=[dir_ for dir_ in os.walk("./") if "./.git" not in dir_[0] and dir_[0]!="./"]
	link_=lambda pre, s1, s2:pre+" ["+s1+"]("+linkPath+s2+")"
	for dir_ in dirs:
		dir=dir_[0][2:]
		subsection=link_("##", dir,dir)
		print(subsection+"\n", file=f)
		for pdf_ in dir_[2]:
			pdf=pdf_
			if " " in pdf:
				pdf=pdf.replace(" ","_")
				os.rename(dir+"/"+pdf_,dir+"/"+pdf)
				print(dir+": Renamed "+pdf_+" -> "+pdf)
			listElement=link_("*",pdf.replace(".pdf","").replace("_"," "),dir+"/"+pdf)
			print(listElement, file=f)
		print("\n",file=f)