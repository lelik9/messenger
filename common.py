from os.path import exists, join
from os import makedirs

TMP_DIR_PATH = 'tmp'
DATA_PATH = 'data'
SQLITE_FILE_PATH = join('tmp', 'sql.db')

if not exists(TMP_DIR_PATH):
    makedirs(TMP_DIR_PATH)