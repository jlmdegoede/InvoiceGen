from docx import Document
from docx.shared import Inches


def generate_docx_invoice(invoice, user, products):
    document = Document()

    document.add_heading(invoice.title, 0)

    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True

    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='IntenseQuote')

    document.add_paragraph(
        'first item in unordered list', style='ListBullet'
    )
    document.add_paragraph(
        'first item in ordered list', style='ListNumber'
    )

    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Qty'
    hdr_cells[1].text = 'Id'
    hdr_cells[2].text = 'Desc'
    for product in products:
        row_cells = table.add_row().cells
        row_cells[0].text = str(product.quantity)
        row_cells[1].text = str(product.title)
        row_cells[2].text = str(product.identification_number)

    document.add_page_break()

    document.save('demo.docx')