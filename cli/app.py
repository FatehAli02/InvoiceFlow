import typer
from pathlib import Path

from core.processor import run_processor, file_processing

cli_app = typer.Typer(help="InvoiceFlow: Automated PDF Invoice Processing Pipeline")

@cli_app.callback()
def main():
    """
    InvoiceFlow: Automated PDF Invoice Processing Pipeline
    """
    pass

@cli_app.command()
def process(
    source_folder : str = typer.Argument(...,help="The path to the folder containing PDF invoices"),
    dest_folder : str = typer.Option(None, "--output", "-o", help="Optional: Specify a custom output folder for the Excel report")
):
    src_path = Path(source_folder)

    if not src_path.exists() or not src_path.is_dir():
        typer.secho(f"Error: The folder '{source_folder}' does not exist.", fg=typer.colors.RED)
        raise typer.Exit()
    
    if dest_folder:
        dest_path = Path(dest_folder)
        dest_path.mkdir(parents=True, exist_ok=True)

    else:
        dest_path = src_path
    typer.secho(f"Starting InvoiceFlow on: {src_path}", fg=typer.colors.CYAN)

    try:
        invoice_list = run_processor(src_folder=src_path, dst_folder=dest_path)
        if invoice_list:
            typer.secho(f"\nProcessing complete! Excel report saved to: {dest_path}", fg=typer.colors.GREEN)
            total_invoices = len(invoice_list)
            total_amount = sum(inv.total_amount for inv in invoice_list)

            typer.secho("\n" + "="*30, fg=typer.colors.MAGENTA, bold=True)
            typer.secho(" 🧾 INVOICEFLOW SUMMARY", fg=typer.colors.WHITE, bold=True)
            typer.secho("="*30, fg=typer.colors.MAGENTA, bold=True)
            typer.secho(f"Total Processed : {total_invoices}", fg=typer.colors.WHITE)
            typer.secho(f"Total Amount    : {total_amount:,.2f}", fg=typer.colors.GREEN, bold=True)
            typer.secho("="*30 + "\n", fg=typer.colors.MAGENTA, bold=True)
        else:
            typer.secho("\nNo valid invoices were found in this directory. Excel report skipped.", fg=typer.colors.YELLOW)
            
        typer.secho("Check logs/app.log for detailed execution history.", fg=typer.colors.YELLOW)
    except Exception as e:
        typer.secho(f"\nA critical system error occurred: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    cli_app()