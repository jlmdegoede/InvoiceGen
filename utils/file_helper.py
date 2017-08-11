import os

from Invoicegen.settings import BASE_DIR


def get_temp_folder_path():
    return os.path.join(BASE_DIR, 'temp')