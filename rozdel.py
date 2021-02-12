from time import sleep
from os import listdir, getenv, mkdir, _exit, chdir, path
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter
import glob

vstup = "U:/dokumenty/.spolecne/Rozdeleni_PDF/IN/"
vystup = "U:/dokumenty/.spolecne/Rozdeleni_PDF/OUT/"     # výstupní cesta
slouceni_vstup = vystup
cesta_ulozeni = "U:/dokumenty/.spolecne/Rozdeleni_PDF/Sloucene_stranky/"



try:
    chdir(vstup)
except FileNotFoundError:
    mkdir(vstup)

try:
    chdir(vystup)
except FileNotFoundError:
    mkdir(vystup)

try:
    chdir(cesta_ulozeni)
except FileNotFoundError:
    mkdir(cesta_ulozeni)


def vstup_pro_rozdeleni(vstup):
    while True:
        try:
            cesta = str(listdir(vstup))  # načte názvy všech souborů do proměnné jako řetězec
        except FileNotFoundError:
            print("Cesta ke vstupním souborům nebyla nalezena.")
            input()
            _exit(0)
        if cesta == "[]":
            print("Nebyly nalezeny soubory ke spracování.")
            print("Vložte soubory a pokračujte klávesou Enter.")
            input()
        else:
            cesta = cesta.replace("[", "")  # ošetří neplatné znaky v názvech souborů
            cesta = cesta.replace("]", "")
            cesta = cesta.replace("'", "")
            return cesta
            break


def vystup_f(vystup):
    try:
        vystup = str(listdir(vystup))
    except FileNotFoundError:
        print("Cesta k výstupním souborům nebyla nalezena. Ukončuji program.")
        input()
        _exit(0)


def split(vstupni_cesta, cesta_ulozeni):
    pdf = PdfFileReader(vstupni_cesta)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        page = page + 1
        output = f'{cesta_ulozeni}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)


vstupni_cesta = ""
vystupni_cesta = ""

otestovany_vstup = vstup_pro_rozdeleni(vstup)
otestovany_vystup = vystup_f(vystup)


def rozdelit_PDF():
    for cesta_pdf in otestovany_vstup.split(","):  # cyklus pro více pdf souborů ve vstupním adresáři
        cesta_pdf = cesta_pdf.strip()
        vstupni_cesta = vstup + cesta_pdf
        vystupni_cesta = cesta_pdf.replace(".", "_")
        vystupni_cesta = vystup + vystupni_cesta
        print()
        try:
            split(vstupni_cesta, vystupni_cesta[:-3])
        except FileNotFoundError:
            print()
            print("Vstupní data nenalezena!")
            print("Vlož data do vstupního adresáře a spusť program znovu.")
            _exit(0)


def split2(vstup, cesta2, stejne, cesta_ulozeni):
    vstupni_cesta = vstup + cesta2 # absolutní cesta k souboru
    pdf = PdfFileReader(vstupni_cesta) # načtení souboru
    pocet_stranek = pdf.getNumPages() # načtení počet stránek v souboru pdf
    smazat_stranky = []
    vsechny_stranky = []
    ponechat_stranky = []
    for vsechny in range(1, pocet_stranek + 1):
        vsechny_stranky.append(vsechny)
    for ponechat in range(1, pocet_stranek, stejne):
        ponechat_stranky.append(ponechat)
    
    for smaz in vsechny_stranky:
        if smaz not in ponechat_stranky:
            smazat_stranky.append(smaz)

    pdf_writer = PdfFileWriter()
    for qqq in ponechat_stranky:
        pdf_writer.addPage(pdf.getPage(qqq))
    output = cesta_ulozeni + cesta2
    with open(output, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


def program():
    while True:
        print("Pro rozdělení PDF na samostatné soubory stiskněte 1. ")
        print("Pro zpracování výstupu pro Leterschop stiskněte 2. ")
        print()
        volba = int(input("Zadej volbu pro zpracování: "))
        if volba == 1:
            print()
            print("Čekej pracuji.")
            rozdelit_PDF()
            print()
            print("Hotovo, soubory jsou ve složce 'OUT'")
            break
        elif volba == 2:
            stejne = int(input("Počet stejných stránek: "))
            print()
            print("Čekej, pracuji")
            cesta2 = vstup_pro_rozdeleni(vstup)
            split2(vstup, cesta2, stejne, cesta_ulozeni)
            print()
            print("Hotovo, soubory jsou ve složce 'Sloucene_stranky'")
            # seznam_vstupu = vstup_pro_slouceni(slouceni_vstup)
            # sloucit_PDF(seznam_vstupu, stejne_stranky)
            break
        else:
            print()
            print("Neznámá volba.")

    input("Stiskem klávesy Enter ukončíš program.")

program()
