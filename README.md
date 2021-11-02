# PDF-utility
## About

PDF-utility can compress and split scanned PDFs to meet file size restrictions for archivization.

## Usage
```
PDF-utility.exe --input [str - Input folder path] --size [float - max filesize of one pdf file in MB]
```
Example:
```
PDF-utility.exe --input D:\Downloads\pdfs --size 1.0
```
App takes all pdf files from ```D:\Downloads\pdfs``` folder and creates ```D:\Downloads\pdfs-output``` folder with compressed and splitted pdf files.
