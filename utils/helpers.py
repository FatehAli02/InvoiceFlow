import re
from dateutil import parser

def clean_amount(raw_amount : str) -> float:
    raw_amount = raw_amount.replace(",","")
    return float(re.findall(r"\d+\.\d+|\d+", raw_amount)[0])

def normalize_date(raw_date : str) -> str:
    dt = parser.parse(raw_date)
    return dt.strftime("%Y-%m-%d")

def clean_text(raw_text : str) -> str:
    if not raw_text or not raw_text.strip():
        return "NULL"
    return(raw_text.strip())
