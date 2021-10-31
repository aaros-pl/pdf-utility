import pdf_split_tool.file_handler as file_handler
import pdf_split_tool.pdf_splitter as pdf_splitter

from math import floor

def _confirm_split_file(filepath: str, max_size_bytes: int) -> None:
    """Split file if user confirms or is valid.

    Args:
        filepath: PDF path.
        max_size_bytes: max size in bytes.
    """
    splitter = pdf_splitter.PdfSplitter(filepath)
    valid = splitter.validate_resolution()
    if not valid:
        print("Warning: {} has more than 200kb per page.").format(filepath)
        print("Consider reducing resolution before splitting.")
        return
    splitter.split_max_size(max_size_bytes)

def main_split(filepath: str, max_size: float) -> None:
    """Pdf Split Tool."""
    max_size_bytes = floor(max_size * 1024 * 1024)  # convert to bytes
    if filepath.endswith(".pdf"):
        _confirm_split_file(filepath, max_size_bytes)
    else:
        filepaths = file_handler.get_filenames(filepath, "*.pdf")
        for path in filepaths:
            _confirm_split_file(path, max_size_bytes)
