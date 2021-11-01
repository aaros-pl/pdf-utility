import os
import sys
from PIL import Image
from tempfile import TemporaryDirectory
from tools import pdf_split
from pdf2image import convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('Running in a PyInstaller bundle')
    # basedir = os.path.dirname(sys.argv[0])
    # basedir = os.path.dirname(sys.executable)
    # input_dir = os.path.join(basedir, "input")
    # if not os.path.exists(input_dir):
    #     print("Katalog wejściowy nie istnieje\n")
    # print(input_dir)
    # output_dir = os.path.join(basedir, "output")
    # if not os.path.exists(output_dir):
    #     os.mkdir(output_dir)
    # print(output_dir)
else:
    print('Running in a normal Python process')
    # input_dir = os.path.join(os.getcwd(), "input")
    # if not os.path.exists(input_dir):
        # print("Katalog wejściowy nie istnieje\n")
    # print(input_dir)
    # output_dir = os.path.join(os.getcwd(), "output")
    # if not os.path.exists(output_dir):
        # os.mkdir(output_dir)
    # print(output_dir)


def process_pdf(basedir=str, size=1.0):
    input_dir = os.path.join(basedir)
    if not os.path.exists(input_dir):
        print("Katalog wejściowy nie istnieje\n")
        return
    output_dir = os.path.join(basedir, "..", "output")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for file in os.listdir(input_dir):
        _, ext = os.path.splitext(file)
        # print(ext)
        # print(os.cpu_count())
        input_file=os.path.join(input_dir, file)
        if ext == ".pdf":
            with TemporaryDirectory() as path:
                with open(input_file, "rb") as pdf_file:
                    images_from_bytes = convert_from_bytes(
                        pdf_file.read(),
                        # fmt="jpg", jpegopt={'quality': 40},
                        # fmt="jpg", jpegopt={'quality': 40, 'optimize': True, 'progressive': True},
                        fmt="jpg", jpegopt={'quality': 30, 'optimize': True},
                        dpi=120, thread_count=os.cpu_count(),
                        grayscale=True,
                        # use_pdftocairo=True,
                        hide_annotations=True,
                        output_folder=path
                    )
                images_from_bytes[0].save(os.path.join(output_dir, file), save_all=True, append_images=images_from_bytes[1:])
                [im.close() for im in images_from_bytes]
        pdf_split.main_split(os.path.join(output_dir, file), size)
        os.remove(os.path.join(output_dir, file))
                
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Compress and split PDFs.')
    # parser.add_argument('--input', metavar='path', type=str, nargs='?', help='Path to input dir.')
    parser.add_argument("-i", "--input", metavar='path', required=True, default=None, type=str, help="Path to input dir with pdfs.")
    # parser.add_argument("-s", "--size", dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
    parser.add_argument("-s", "--size", metavar='size', required=False, default=1.0, type=float, help="Max size in MB of one PDF file.")
    args = parser.parse_args()
    process_pdf(args.input, args.size)
    print("Done")

# process_pdf()
# input("Press Enter to continue...")
