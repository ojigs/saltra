import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler('logs/app.log', encoding='utf-8')
    ]
)

def get_logger(name):
    return logging.getLogger(name)