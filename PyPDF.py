from PyPDF2 import PdfFileMerger

# pdfs = ['Letter of motivation.pdf', 'Table of modules.pdf', 'Module.pdf', 'Teilmodule.pdf']

pdfs = ['1.pdf', '2.pdf', '3.pdf', '4.pdf', '5.pdf']

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(open(pdf, 'rb'))

with open('result.pdf', 'wb') as fout:
    merger.write(fout)
