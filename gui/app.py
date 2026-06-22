import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
import os
import sys
import subprocess

from core.processor import run_processor

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class InvoiceFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("InvoiceFlow Pipeline")
        self.geometry("750x550")
        self.resizable(False, False)

        self.selected_folder = None
        self.output_folder = None

        
        self.header = ctk.CTkLabel(self, text="InvoiceFlow Pipeline", font=ctk.CTkFont(size=26, weight="bold"))
        self.header.pack(pady=(20, 10))

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10, fill="x", padx=40)
        
        self.select_btn = ctk.CTkButton(self.input_frame, text="📁 Select Invoices Folder", command=self.select_source_folder, width=200)
        self.select_btn.grid(row=0, column=0, padx=(0, 15), pady=5)
        self.source_label = ctk.CTkLabel(self.input_frame, text="No source folder selected", text_color="gray", font=ctk.CTkFont(size=13))
        self.source_label.grid(row=0, column=1, sticky="w", pady=5)

        self.dest_btn = ctk.CTkButton(self.input_frame, text="📂 Select Output Folder", command=self.select_dest_folder, width=200, fg_color="transparent", border_width=1, text_color=("black", "white"))
        self.dest_btn.grid(row=1, column=0, padx=(0, 15), pady=5)
        self.dest_label = ctk.CTkLabel(self.input_frame, text="Default: Same as source", text_color="gray", font=ctk.CTkFont(size=13, slant="italic"))
        self.dest_label.grid(row=1, column=1, sticky="w", pady=5)

        self.process_btn = ctk.CTkButton(self, text="🚀 Process Invoices", font=ctk.CTkFont(weight="bold", size=15), 
                                         height=45, width=250, command=self.process_invoices, state="disabled")
        self.process_btn.pack(pady=(15, 5))

        self.status_label = ctk.CTkLabel(self, text="Waiting for source folder...", font=ctk.CTkFont(size=14, slant="italic"), text_color="gray")
        self.status_label.pack(pady=(0, 10))

        self.summary_box = ctk.CTkTextbox(self, width=650, height=160, state="disabled", fg_color="transparent", border_width=2, font=ctk.CTkFont(family="Courier", size=14))
        self.summary_box.pack(pady=5)

        self.open_btn = ctk.CTkButton(self, text="📊 Open Excel Report", font=ctk.CTkFont(weight="bold"), 
                                      command=self.open_report, state="disabled")
        self.open_btn.pack(pady=(15, 20))

    # --- LOGIC ---

    def truncate_path(self, path):
        path_str = str(path)
        return f"...{path_str[-45:]}" if len(path_str) > 45 else path_str

    def select_source_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder containing PDFs")
        if folder_path:
            self.selected_folder = Path(folder_path)
            self.source_label.configure(text=self.truncate_path(self.selected_folder), text_color=("black", "white"))
            
            self.process_btn.configure(state="normal")
            self.status_label.configure(text="Ready to process.", text_color=("black", "white"))
            
            self.open_btn.configure(state="disabled")
            self.update_summary_box("")

    def select_dest_folder(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder (Optional)")
        if folder_path:
            self.output_folder = Path(folder_path)
            self.dest_label.configure(text=self.truncate_path(self.output_folder), text_color=("black", "white"), font=ctk.CTkFont(size=13, slant="roman"))

    def process_invoices(self):
        if not self.selected_folder:
            return

        final_dest = self.output_folder if self.output_folder else self.selected_folder

        self.status_label.configure(text="Processing... Please wait.", text_color="#17a2b8")
        self.process_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.dest_btn.configure(state="disabled")
        self.update() 

        try:
            invoice_list = run_processor(src_folder=self.selected_folder, dst_folder=final_dest)

            if invoice_list:
                total_invoices = len(invoice_list)
                total_amount = sum(inv.total_amount for inv in invoice_list)

                summary_text = (
                    f"{'='*46}\n"
                    f"{'🧾 INVOICEFLOW SUMMARY':^46}\n"
                    f"{'='*46}\n\n"
                    f"  Total Processed : {total_invoices}\n"
                    f"  Total Amount    : {total_amount:,.2f}\n\n"
                    f"  Output Location : {self.truncate_path(final_dest)}\n"
                    f"{'='*46}\n"
                )
                
                self.status_label.configure(text=f"✅ Done! Successfully processed {total_invoices} invoices.", text_color="green")
                self.update_summary_box(summary_text)
                
                self.open_btn.configure(state="normal")
            else:
                self.status_label.configure(text="⚠️ No valid invoices found in source.", text_color="#d4a017")
                self.update_summary_box("\n\n        No data to summarize.")

        except Exception as e:
            self.status_label.configure(text="❌ A critical error occurred. Check logs.", text_color="red")
            self.update_summary_box(f"Error Details:\n{e}")

        self.process_btn.configure(state="normal")
        self.select_btn.configure(state="normal")
        self.dest_btn.configure(state="normal")

    def update_summary_box(self, text):
        self.summary_box.configure(state="normal")
        self.summary_box.delete("1.0", "end")
        self.summary_box.insert("1.0", text)
        self.summary_box.configure(state="disabled")

    def open_report(self):
        final_dest = self.output_folder if self.output_folder else self.selected_folder
        if final_dest:
            file_path = final_dest / "invoice_report.xlsx"
            if file_path.exists():
                if sys.platform == "win32":
                    os.startfile(file_path)
                elif sys.platform == "darwin":
                    subprocess.call(["open", file_path])
                else:
                    subprocess.call(["xdg-open", file_path])

if __name__ == "__main__":
    app = InvoiceFlowApp()
    app.mainloop()