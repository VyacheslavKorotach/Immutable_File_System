import os
import json
import time
from eospy.cleos import Cleos
import eospy.cleos
import eospy.keys
import pytz
import requests
import base64


class EosFile:
    account = ''
    path = ''
    file_name = ''

    def __init__(self, account: str, path: str, file_name: str):
        self.account = account
        self.path = path
        self.file_name = file_name

    def ping(self):
        print("I'm here")

    def put_file(self, file_name: str) -> bool:
        pass
        return False

    def get_file(self, account: str, file_name: str, path: str) -> str:
        pass
        return ''

    def get_dir(self, account: str):
        pass

    def get_all_files(self, account: str, path: str) -> int:
        '''
        :returns quantity of saved files
        '''
        pass

    def __encode_file(self, file_name: str) -> str:
        s0 = "test string"
        b1 = base64.b64encode(bytes(s0, 'utf-8'))
        s1 = b1.decode('utf-8')
        print(s1)
        return s1

    def __decode_file(self, encoded_data: str):
        b1 = base64.b64decode(encoded_data)
        # s2 = base64.b64decode(encoded_data).decode("utf-8", "ignore")
        print(b1)
        return b1
