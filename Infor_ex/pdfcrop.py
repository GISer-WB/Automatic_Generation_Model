from PyPDF2 import PdfFileWriter, PdfFileReader

def  pdfCrop(path,start_page,save_path):
    """
    从pdf文件中截取几页，并保存在对应pdf文件中
    """
    # 开始页
    start_page = start_page - 1
    # 截止页
    end_page = start_page +  1 # 这里设定截取3页
    output = PdfFileWriter()
    pdf_file = PdfFileReader(path)
    pdf_pages_len = pdf_file.getNumPages()
    for i  in  range(start_page, end_page):
        output.addPage(pdf_file.getPage(i)) # 在输出流中添加页
    outputStream =  open(save_path, "wb")
    output.write(outputStream)

if __name__ == '__main__':
   inputfile = r"D:\code\bp\pmt\dem\infor_extract\infor_ex\input.pdf"
   outputfile = r"D:\code\bp\pmt\dem\infor_extract\infor_ex\output.pdf"    
   pdfCrop(inputfile,5,outputfile)
