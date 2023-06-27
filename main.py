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


def extract_full(start_page=0, end_page=0, in_file_path="../Savage_Worlds_Adventure_Edition.pdf",
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


def extract_two_col(start_page=0, end_page=0, in_file_path="../Savage_Worlds_Adventure_Edition.pdf",
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
            page = pdf.pages[start_page]
            left = page.crop((0, 0, 0.5 * page.width, 0.9 * page.height))
            right = page.crop((0.5 * page.width, 0, page.width, page.height))
            l_text = left.extract_text()
            r_text = right.extract_text()
            text = l_text + " " + r_text
            text = filter_text(text)
            f.write(text)
        else:
            current_page = start_page
            while current_page <= end_page:
                # text = pdf.pages[current_page].extract_text()
                page = pdf.pages[current_page]
                left = page.crop((0, 0, 0.5 * page.width, 0.9 * page.height))
                right = page.crop((0.5 * page.width, 0, page.width, page.height))
                l_text = left.extract_text()
                r_text = right.extract_text()
                text = l_text + " " + r_text
                current_page += 1
                text = filter_text(text)
                f.write(text)
    f.close()


def test(in_file_path="../Savage_Worlds_Adventure_Edition.pdf"):
    with pdfplumber.open(in_file_path) as pdf:
        page = pdf.pages[39]
        left = page.crop((0, 0, 0.5 * page.width, 0.9 * page.height))
        right = page.crop((0.5 * page.width, 0, page.width, page.height))
        l_text = left.extract_text()
        r_text = right.extract_text()
        text = l_text + " " + r_text
        print(text)


if __name__ == '__main__':
    reload(sys)
    temp = sys.getdefaultencoding()

    n = len(sys.argv)
    print("Total arguments passed: ", n)
    extract_two_col(39, 55, in_file_path="../Savage_Worlds_Adventure_Edition.pdf")
