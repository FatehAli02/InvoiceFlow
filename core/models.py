from dataclasses import dataclass

@dataclass
class Invoice:
    invoice_number : str
    vendor : str
    date : str
    total_amount : float