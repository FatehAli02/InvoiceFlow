import pdfplumber
from pathlib import Path
import re
from core import models
from utils.helpers import clean_amount, clean_text, normalize_date

def data_extraction(file) -> models.Invoice:
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        raw_data = first_page.extract_text()

        lines = raw_data.split('\n')
        first_line = lines[0] if lines else ""
        vend_name = first_line.replace(" INVOICE", "").strip()

        inv_num = re.findall(r"(?:Invoice No|Inv #|Reference|Invoice #|#)\s*:?\s*([A-Za-z0-9\-]+)",raw_data)
        inv_num = inv_num[0] if inv_num else ""
        date = re.findall(r"(?:Date|Invoice Date|Billed On)\s*:\s*([^\n]+)",raw_data)
        date = date[0] if date else ""
        amount = re.findall(r"(?:Total|Total Amount|Due|Total Due)\s*:\s*((?:PKR|pkr|\$|Rs.|Rs\.?)\s*[0-9,]+\.[0-9]{2})",raw_data)
        amount = amount[0] if amount else ""

        clean_inv_num = clean_text(inv_num)
        clean_vend_name = clean_text(vend_name)
        clean_date = normalize_date(date) if date else "NOT FOUND"
        clean_amt = clean_amount(amount) if amount else 0.0

        return models.Invoice(
            invoice_number=clean_inv_num,
            vendor=clean_vend_name,
            date=clean_date,
            total_amount=clean_amt
        )
