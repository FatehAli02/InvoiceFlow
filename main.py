import sys

from gui.app import InvoiceFlowApp
from cli.app import cli_app

def main():
    if len(sys.argv) > 1:
        cli_app()
    else:
        app = InvoiceFlowApp()
        app.mainloop()

if __name__ == "__main__":
    main()