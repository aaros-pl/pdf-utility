import os
from PIL import Image
from tempfile import TemporaryDirectory
from pdf2image import convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from tools import pdf_split

input_dir = os.path.join(os.getcwd(), "input")
output_dir = os.path.join(os.getcwd(), "output")


def process_pdf():
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
        pdf_split.main_split(os.path.join(output_dir, file), 1.0)
        os.remove(os.path.join(output_dir, file))
                
if __name__ == "__main__":
    process_pdf()