import os

from fpdf import FPDF
from PIL import Image
from PyPDF2 import PdfFileMerger

DEBUG=False

def get_files(input_folders):
    # 获取所有图片文件的路径
    image_files = []
    for input_folder in input_folders:
        inner_dirs = os.listdir(input_folder)
        inner_dirs.sort()
        for inner_dir in inner_dirs:
            files = os.listdir(os.path.join(input_folder,inner_dir))
            files.sort()
            for file in files:
                filepath = os.path.join(input_folder,inner_dir,file)
                if DEBUG:
                    print(filepath)
                image_files.append(filepath)
    return image_files

def convert_images_to_pdf(input_folders, output_pdf):
    # 获取所有图片文件的路径
    image_files = get_files(input_folders)

    # 创建一个PDF文件
    pdf = FPDF()
    for image_file in image_files:
        pdf.add_page()
        img = Image.open(image_file)
        if DEBUG:
            print(img.size)
        if img.size[0]>img.size[1]:
            img = img.transpose(Image.ROTATE_270)
            if DEBUG:
                print(img.size)
            img.save(image_file)
        if DEBUG:
            print(image_file)
        
        # A4: 210x297 wxh ==> h/w < 297/210
        w, h = img.size[0], img.size[1]
        if h/w < 297/210:
            pdf.image(image_file, pdf.w*0.05, pdf.h*0.05, pdf.w*0.9)
        else:
            rate = 0.9/((h/w)/(297/210))
            pdf.image(image_file, pdf.w*0.05, pdf.h*0.05, pdf.w*rate)
            # break

    # 将PDF文件保存到输出路径
    pdf.output(output_pdf)

if __name__ == "__main__":
    DEBUG=True
    input_folder1 = "2021/"
    input_folder2 = "2022/"
    output_pdf = "output.pdf"

    convert_images_to_pdf([input_folder1,input_folder2], output_pdf)
