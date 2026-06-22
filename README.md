# 🧾 InvoiceFlow: Automated PDF Invoice Processing Pipeline 📂

**InvoiceFlow** is a deterministic ETL (Extract, Transform, Load) pipeline designed to automatically process standardized B2B PDF invoices. It extracts key billing data, cleans it, and compiles it into a stylized, multi-sheet Excel report.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-green)
![CLI](https://img.shields.io/badge/CLI-Typer-orange)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

While probabilistic extraction (like LLMs) is popular, real-world financial systems require 100% accuracy. Therefore, this engine is designed to strictly parse standard vendor templates, mirroring how large enterprises enforce portal submissions to prevent data corruption.

**⚠️ Current Scope & Formatting:**
Currently, the regex extraction engine is tightly configured to process standard templates generated via **Invoice-Generator.com**. It extracts key billing data (Invoice Number, Vendor Name, Date, and Amount), cleans it, and compiles it into a stylized, multi-sheet Excel report.

A major architectural feature of this project is its **Core Engine Reusability**. The exact same backend logic seamlessly powers both a Command Line Interface (CLI) for developers and a Graphical User Interface (GUI) for standard users.

## ✨ Features

### 1. 📄 Automated Data Extraction
Accurately parses Invoice Number, Vendor Name, Date, and Total Amount from PDF files.

### 2. 🧹 Robust Data Cleaning
Built-in helper functions normalize dates, strip currency symbols (e.g., "$", "PKR"), and safely handle missing data without crashing.

### 3. 🖥️ Dual Interfaces
- **Typer CLI:** Fully functional command-line interface for developers.
- **CustomTkinter GUI:** Modern, green-themed visual dashboard for standard users.

### 4. 📊 Formatted Excel Export
Automatically generates `invoice_report.xlsx` with a "Raw Data" sheet and an aggregated "Summary" sheet (including total invoices, total amount, and vendor-wise totals), styled with professional corporate colors.

### 5. 🗄️ Archival System & Logging
- Automatically moves processed PDFs to an `/Archive/` folder to prevent accidental double-processing.
- Tracks background successes, failures, and missing fields in `logs/app.log`.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **PDF Parsing:** `pdfplumber`
- **Excel Generation:** `openpyxl`
- **Interfaces:** `typer` (CLI), `customtkinter` (GUI)
- **Data Parsing:** `python-dateutil`, `re` (Regular Expressions)

## 📦 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/fatehali02/InvoiceFlow.git](https://github.com/fatehali02/InvoiceFlow.git)
   cd InvoiceFlow
- Option A: Using Standard pip
**Create and activate a virtual environment**
    ```bash
    python -m venv venv
    ```
    - On Windows:
    ```PowerShell
    venv\Scripts\activate
    ```
    - On Mac/Linux:
    ```bash
    source venv/bin/activate
    ```
**Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
- Option B: Using uv (Extremely Fast)
**Create and activate a virtual environment**
    ```bash
    uv venv
    ```
    - On Windows:
    ```Powershell
    .venv\Scripts\activate
    ```
    - On Mac/Linux:
    ```bash
    source .venv/bin/activate
    ```
**Install Dependencies**
    ```bash
    uv pip install -r requirements.txt
    ```
## 🎯 Usage
Because of the smart routing in main.py, launching the app is incredibly simple. (Note: If you are using uv, you can replace python with uv run in the commands below).
**Option 1: The Graphical User Interface (GUI)**
Ideal for standard users who prefer a visual dashboard.
```bash
python main.py
```
- Click "Select Invoices Folder" to choose your input directory.

- Optionally, select an output folder (defaults to the source folder).

- Click "Process Invoices" to extract the data and view the on-screen summary dashboard.

**Option 2: The Command Line Interface (CLI)**
Ideal for developers and automated terminal scripts.
```bash
python main.py process [".../invoices"]
```
- Use the --output or -o flag to specify a custom destination for the Excel file.

- Example: python main.py process ./invoices -o ./reports

## 📁 Project Structure
InvoiceFlow/
│
├── main.py                 # Entry point 
├── core/
│   ├── processor.py        # Main pipeline logic
│   ├── models.py           # Invoice class (OOP)
│   └── extractor.py        # PDF parsing logic
├── export/
│   └── excel_writer.py     # openpyxl logic
├── cli/
│   └── app.py              # Typer CLI
├── gui/
│   └── app.py              # CustomTkinter UI
├── utils/
│   ├── logger.py           # logging setup
│   └── helpers.py          # date/amount cleaning
├── logs/
│   └── app.log
├── invoices/               # sample input
├── output/
│   └── invoice_report.xlsx
├── requirements.txt
└── README.md

## 👨‍💻 Author
Made by Fateh Ali 
[LinkedIn](https://www.linkedin.com/in/fateh-ali-072348352/) | [GitHub](https://github.com/fatehali02) 

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer
- This project is for educational and portfolio purposes.

- Always ensure you have backups of your files before running automated archival scripts.