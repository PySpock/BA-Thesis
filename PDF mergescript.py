from PyPDF2 import PdfFileMerger
import os

def getPDFs():
	dircontent = os.listdir(os.getcwd())
	pdflist = []
	for item in dircontent:
		if item[-4:] == '.pdf':
			pdflist.append(item)
	return pdflist


pdfs = getPDFs()

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(open(pdf, 'rb'))

with open('result.pdf', 'wb') as fout:
    merger.write(fout)
