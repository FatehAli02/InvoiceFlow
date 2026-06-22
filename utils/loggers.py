import logging
from pathlib import Path

def setup_logger():

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    return logging.getLogger("InvoiceFlow")

logger = setup_logger()