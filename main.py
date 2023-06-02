import sys
from importlib import reload

import pdfplumber


def filter_non_printable(text):
    return ''.join([c for c in text if ord(c) > 31 or ord(c) == 9])


def extract(*args, in_file_path="./test.pdf", out_file_path="./outText.txt"):
    f = open(out_file_path, "w", encoding="ascii", errors="surrogateescape")
    with pdfplumber.open(in_file_path) as pdf:
        # iterate over requested pages
        index = 0
        length = len(args)
        while index < length:
            # pdf page numbers start at 1
            start_page = args[index] - 1
            index += 1
            if index < length:
                end_page = args[index] + 1
                index += 1
            else:
                end_page = start_page + 1
            current_page = start_page
            while current_page < end_page:
                text = pdf.pages[current_page].extract_text()
                current_page += 1
                text = filter_non_printable(text)
                print(text)
                # get rid of unprintable characters
                text = text.encode(encoding="ascii", errors="replace")
                text = text.decode(encoding="utf-8", errors='replace')
                f.write(text)
        f.close()


if __name__ == '__main__':
    reload(sys)
    temp = sys.getdefaultencoding()

    n = len(sys.argv)
    print("Total arguments passed: ", n)
    # arg[0] start page
    # arg[1] end page
    # arg[2] in file path
    # arg[3] out file path
    extract(20, 28, in_file_path="demo.pdf")
