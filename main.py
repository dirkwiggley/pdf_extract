import sys
from importlib import reload

import pdfplumber


def filter_non_printable(text):
    return ''.join([c for c in text if ord(c) > 31 or ord(c) == 9])


# get rid of unprintable characters
def filter_text(text):
    text = filter_non_printable(text)
    text = ascii(text)
    return text.replace(r"\u201c", '"').replace(r"\u201d", '"').replace(r"\u2212", "-") \
        .replace(r"\u2019", "'").replace("SDLROW", ' ')


def extract(start_page=0, end_page=0, in_file_path="../Savage_Worlds_Adventure_Edition.pdf",
            out_file_path="./outText.txt"):
    f = open(out_file_path, "w", encoding="ascii", errors="surrogate-escape")
    with pdfplumber.open(in_file_path) as pdf:
        # page numbers are 0 based
        start_page -= 1
        end_page -= 1
        if start_page < 0:
            start_page = 0
        if start_page > end_page:
            end_page = start_page
        if start_page == end_page:
            text = pdf.pages[start_page].extract_text()
            text = filter_text(text)
            f.write(text)
        else:
            current_page = start_page
            while current_page <= end_page:
                text = pdf.pages[current_page].extract_text()
                current_page += 1
                text = filter_text(text)
                f.write(text)
    f.close()


if __name__ == '__main__':
    reload(sys)
    temp = sys.getdefaultencoding()

    n = len(sys.argv)
    print("Total arguments passed: ", n)
    extract(20, 20, in_file_path="../Savage_Worlds_Adventure_Edition.pdf")
