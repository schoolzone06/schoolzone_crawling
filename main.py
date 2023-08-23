from getSchoolInfoList import SchoolInfo
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

if __name__ == '__main__':
    getSchoolInfo = SchoolInfo(os.getenv("NEIS_API_KEY"))
    getSchoolInfo.save_data()
