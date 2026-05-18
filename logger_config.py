import logging
import os

def registrar_log(mensagem):
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/sistema.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    logging.info(mensagem)
