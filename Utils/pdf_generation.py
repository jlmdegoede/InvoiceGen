from Utils.date_helper import *
import os


def generate_title(file, user):
    file.writelines("\\color{textGray} \n")
    file.writelines("\\pagenumbering{gobble} \n")
    file.writelines("\\vspace*{25pt}\n")
    file.writelines("\\Huge\n")
    file.writelines("\\BgThispage\n")
    file.writelines("\\textcolor{black}{\\textbf {Factuur}}\n")
    file.writelines("\n")
    file.writelines("\\textcolor{black}{\\textbf{" + get_today_string() +"}}\n")
    file.writelines("\n")
    file.writelines("\\textcolor{black}{\\textbf{Freelancer " + user.name +  "}}\n")
    file.writelines("\\BgThispage\n")
    file.writelines("\\vspace*{20pt}\n")
    file.writelines("\n")


def generate_gegevens_factuur(file,invoice):
    file.writelines("%% Gegevens Factuur\n")
    file.writelines("\\LARGE \n")
    file.writelines("\\noindent\\colorbox{materialGreen}\n")
    file.writelines("{\\parbox[c][25pt][c]{\\textwidth}{\\hspace{15pt}\\textcolor{white}{\\textbf{Gegevens factuur}}}}\n")
    file.writelines("\\begin{tabular}{l l}\n")
    file.writelines("\\InvullenTwee{Volgnummer}{" +str(invoice.invoice_number)+"}{20}   \n")
    file.writelines("\\InvullenTwee{Datum}{" + get_today_string() + "}{20}\n")
    file.writelines("\\end{tabular} \\\\ \n")
    file.writelines("\n")


def generate_gegevens_leverancier(file,user):
    file.writelines("%% Gegevens Leverancier\n")
    file.writelines("\\LARGE \n")
    file.writelines("\\noindent\\colorbox{materialGreen}\n")
    file.writelines("{\\parbox[c][25pt][c]{\\textwidth}{\\hspace{15pt}\\textcolor{white}{\\textbf{Gegevens leverancier}}}}\n")
    file.writelines("\\begin{tabular}{l l}\n")
    file.writelines("\\InvullenTwee{Naam}{" + user.name + "}{0}   \n")
    file.writelines("\\InvullenTwee{Adres}{" + user.address + "}{0}   \n")
    file.writelines("\\InvullenTwee{Postcode, plaats}{" + user.city_and_zipcode + "}{0}   \n")
    file.writelines("\\InvullenTwee{E-mail}{" + user.email + "}{0}   \n")
    file.writelines("\\InvullenTwee{IBAN}{" + user.iban + "}{0}   \n")
    file.writelines("\\end{tabular} \\\\ \n")
    file.writelines("\n")


def generate_gegevens_afnemer(file, invoice):
    file.writelines("%% Gegevens Afnemer\n")
    file.writelines("\\LARGE \n")
    file.writelines("\\noindent\\colorbox{materialGreen}\n")
    file.writelines("{\\parbox[c][25pt][c]{\\textwidth}{\\hspace{15pt}\\textcolor{white}{\\textbf{Gegevens afnemer}}}}\n")
    file.writelines("\\begin{tabular}{l l}\n")
    file.writelines("\\InvullenTwee{Bedrijfsnaam}{" + invoice.to_company.company_name + "}{0}   \n")
    file.writelines("\\InvullenTwee{Adres}{" + invoice.to_company.company_address + "}{0}   \n")
    file.writelines("\\InvullenTwee{Postcode, plaats}{" + invoice.to_company.company_city_and_zipcode + "}{0}   \n")
    file.writelines("\\end{tabular} \\\\ \n")
    file.writelines("\n")


def generate_geleverd(file, products):
    file.writelines("%% Geleverd\n")
    file.writelines("\\LARGE \n")
    file.writelines("\\noindent\\colorbox{materialGreen}\n")
    file.writelines("{\\parbox[c][25pt][c]{\\textwidth}{\\hspace{15pt}\\textcolor{white}{\\textbf{Geleverd}}}}\n")
    file.writelines("\\begin{tabular}{l l l l}\n")
    file.writelines("\\InvullenVierBold{Opdracht}{Volgnummer}{Kwantiteit}{Prijs}\n")
    for product in products:
        file.writelines("\\InvullenVier{" + product.title + "}{" + str(product.identification_number ) + "}{" + str(product.quantity)+"x" + "}{" + str(product.get_price()) + "}\n")
    file.writelines("\\end{tabular} \\\\\\\\ \n")


def generate_final_section(file, invoice, tax_rate):
    file.writelines("\\begin{changemargin}{1cm}{1cm}")
    if tax_rate:
        file.writelines("\large \\textbf{Subtotaal: \\euro" + str(invoice.get_totaalbedrag()) + "}\n")
        file.writelines("\\\\")
        file.writelines("\\\\")
        file.writelines("\large \\textbf{BTW: \\euro" + str(invoice.get_btw()) + "}\n")
        file.writelines("\\\\")
        file.writelines("\\\\")
        file.writelines("\large \\textbf{Totaal te voldoen: \\euro" + str(invoice.get_totaalbedrag() + invoice.get_btw()) + "}\n")
    else:
        file.writelines("\large \\textbf{Totaal te voldoen: \\euro" + str(invoice.get_totaalbedrag()) + "}\n")

    file.writelines("\\end{changemargin}")
    file.writelines("\n")


def generate_pdf(products, user, invoice):
    entry_file = "Templates/MaterialDesign/temp/entry.tex"
    with open(entry_file, 'w') as file:
        generate_title(file, user)
        generate_gegevens_factuur(file, invoice)
        generate_gegevens_leverancier(file, user)
        generate_gegevens_afnemer(file, invoice)
        generate_geleverd(file, products)
        generate_final_section(file, invoice, products[0].tax_rate != 0)
    os.chdir("Templates/MaterialDesign/temp/")
    os.system("xelatex main.tex")
    os.chdir("../../..")
    return