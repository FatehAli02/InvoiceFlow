from pathlib import Path
from core.extractor import data_extraction
from export.excel_writer import generate_excel_report
import shutil

def file_processing(src_folder : Path) -> list:
    invoices = []
    archive = src_folder / "Archive"
    archive.mkdir(parents=True, exist_ok=True)
    for file in src_folder.glob("*.pdf"):
        try:
            invoice = data_extraction(file)
            invoices.append(invoice) 
            shutil.move(file,archive)

            print(f"Successfully processed and archived: {file.name}")

        except Exception as e:
            print(f"Failed to process {file.name}: {e}")
            continue
    return invoices

def run_processor(src_folder, dst_folder):
    invoice_list = file_processing(src_folder)
    if invoice_list:
        generate_excel_report(invoice_list, dst_folder)
    else:
        print("No valid invoices were processed. Excel report skipped.")
