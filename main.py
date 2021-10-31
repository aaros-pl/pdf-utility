import tempfile
import os
import sys
import shutil
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

input_dir = os.path.join(os.getcwd(), "input")

# tmpdir = os.path.join(os.getcwd(), "temp")

# print(tmpdir, '\n')
# images = convert_from_bytes(open(r'input\10840.pdf', 'rb').read(), dpi=96, thread_count=4, jpegopt='optimize', grayscale=True, output_folder=path)
# images_from_path = convert_from_path("input\\10840.pdf", dpi=96, thread_count=4, fmt='ppm', jpegopt='optimize', grayscale=True, output_folder=path)
# if not os.path.exists(tmpdir):
#     os.mkdir(tmpdir)
# images_from_path = convert_from_path(r"input\10840.pdf",
#     output_folder=tmpdir,
#     fmt="jpg", #jpegopt={'quality': 75, 'optimize': True, 'progressive': True},
#     dpi=120, thread_count=4, grayscale=True, use_pdftocairo=True)
# print(images_from_path, '\n')
# images_from_path[0].save(r"output\out.pdf", save_all=True, append_images=images_from_path[1:])

def process_pdf():
    for file in os.listdir(input_dir):
        filename, ext = os.path.splitext(file)
        #print(ext)
        input_file=os.path.join(input_dir, file)
        if ext == ".pdf":
            with tempfile.TemporaryDirectory() as path:
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
                images_from_bytes[0].save(os.path.join(os.getcwd(), "output", file), save_all=True, append_images=images_from_bytes[1:])
                [im.close() for im in images_from_bytes]

if __name__ == "__main__":
    process_pdf()