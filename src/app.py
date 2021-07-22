import tkinter as tk
import PyPDF2
import os

from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile

FONT = 'Raleway'

def define_paths():
    base = os.path.dirname(os.path.abspath(__file__))[:-4]
    return {
        'base': base,
        'src': os.path.join(base, 'src'),
        'resource': os.path.join(base, 'resource')
    }

def show_logo(path):
    logo = Image.open(os.path.join(path, 'logo.png'))
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo)
    logo_label.image = logo
    logo_label.grid(column=1, row=0)

def show_instructions(root):
    instructions = tk.Label(root, text='Select a PDF file on your computer to extract all its text', font=FONT)
    instructions.grid(columnspan=3, column=0, row=1)

def show_browse_button(root):
    browse_text = tk.StringVar()
    browse_btn = tk.Button(root, textvariable=browse_text, font=FONT, bg='#20bebe', fg='white', height=2, width=15, command=lambda:open_file(root, browse_text))
    browse_text.set('Browse')
    browse_btn.grid(column=1, row=2)
    show_bottom_margin(root, 3)

def show_bottom_margin(root, row):
    margin = tk.Label(root, text='', font=FONT)
    margin.grid(columnspan=3, column=0, row=row)

def open_file(root, browse_text):
    browse_text.set ('Loading...')
    file = askopenfile(parent=root, mode='rb', title='Choose a file', filetype=[("PDF file", '*.pdf')])

    if file:
        read_file(file, root)

    browse_text.set('Browse')
        
def read_file(file, root):
    read_pdf = PyPDF2.PdfFileReader(file)
    page = read_pdf.getPage(0)
    page_content = page.extractText()
    print(page_content)

    text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
    text_box.insert(1.0, page_content)
    text_box.tag_configure('center', justify='center')
    text_box.tag_add('center', 1.0, 'end')
    text_box.grid(column=1, row=4)
    show_bottom_margin(root, 5)


if __name__ == '__main__':
    path = define_paths()

    root = tk.Tk()
    root.title("Extract PDF do Text")

    canvas = tk.Canvas(root, width=600, height=300)
    canvas.grid(columnspan=3)

    show_logo(path['resource'])
    show_instructions(root)
    show_browse_button(root)

    root.mainloop()