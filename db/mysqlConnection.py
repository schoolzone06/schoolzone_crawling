import pymysql
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


connection_pool = pymysql.connect(
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PW"),
    host=os.getenv("DB_HOST"),
    db=os.getenv("DB_NAME"),
    charset="utf8"
)
