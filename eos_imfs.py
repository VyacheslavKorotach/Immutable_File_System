import os
import json
import time
from eospy.cleos import Cleos
import eospy.cleos
import eospy.keys
import pytz
import requests
import base64

eos_endpoint = 'https://eosbp.atticlab.net'
depth = 33


# imfs_provider_account = 'wealthysnake'
# active_privat_key = os.environ['IMFS_PROVIDER_PRIVAT_KEY']


class EosFile:
    account = ''
    path = ''
    file_name = ''
    sender_account = ''
    sender_privat_key = ''

    def __init__(self, account: str, path: str, file_name: str, sender_account: str, sender_privat_key: str):
        self.account = account
        self.path = path
        self.file_name = file_name
        self.sender_account = sender_account
        self.sender_privat_key = sender_privat_key

    def ping(self):
        print("I'm here")

    def put_file(self) -> int:
        '''
        :return: block number of file header block
        '''
        fc = ''
        block_size = 200
        fb = open(f'{self.path}/{self.file_name}', 'rb')
        fc = fb.read()
        print('file content = ', fc)
        fb.close()
        fc_encoded = self.__encode_str(fc)
        block_num = 0
        while fc_encoded != '':
            if len(fc_encoded) >= block_size:
                data_block = fc_encoded[:block_size]
                fc_encoded = fc_encoded[block_size:]
            else:
                data_block = fc_encoded[:len(fc_encoded)]
                fc_encoded = fc_encoded[len(fc_encoded):]
            print(data_block)
            data_json = f'{{"file":"{self.file_name}","next_block":{block_num},"data":"{data_block}"}}'
            ret = self.__send_block(data_json)
            if ('transaction_id' in ret):
                print(ret)
                block_num = ret['processed']['block_num']
                print(block_num)
            else:
                return 0
            time.sleep(1)
        self.update_dir(block_num)
        return block_num

    def get_file(self, head_block: int) -> str:
        pass
        return ''

    def get_dir(self):
        memos = self.__get_last_actions()
        memos.reverse()
        for m in memos:
            memo = m['memo']
            if self.__is_json(memo):
                memo_d = json.loads(memo)
                if ('imfs' in memo_d.keys()):
                    return memo_d
        return {}

    def update_dir(self, head_block: int):
        cur_dir = self.get_dir()
        upd_dir = cur_dir
        if cur_dir == {}:
            upd_dir = {
                "imfs": "v_0.1",
                "next_dir": 0
            }
        upd_dir[self.file_name] = head_block
        upd_dir = json.dumps(upd_dir)
        print(str(upd_dir))
        return self.__send_block(str(upd_dir))

    def get_all_files(self, account: str, path: str) -> int:
        '''
        :returns quantity of saved files
        '''
        pass

    def __is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        return True

    def __encode_str(self, bytes_to_encode) -> str:
        b1 = base64.b64encode(bytes_to_encode)
        s1 = b1.decode('utf-8')
        print(s1)
        return s1

    def __decode_str(self, encoded_data: str):
        b1 = base64.b64decode(encoded_data)
        # s2 = base64.b64decode(encoded_data).decode("utf-8", "ignore")
        print(b1)
        return b1

    def __send_block(self, memo: str):
        ce = Cleos(url=eos_endpoint)
        arguments = {
            "from": self.sender_account,  # sender
            "to": self.account,  # receiver
            "quantity": '0.0001 EOS',  # In Token
            "memo": memo,
        }
        payload = {
            "account": 'eosio.token',
            "name": 'transfer',
            "authorization": [{
                "actor": self.sender_account,
                "permission": 'active',
            }],
        }
        # Converting payload to binary
        data = ce.abi_json_to_bin(payload['account'], payload['name'], arguments)
        # Inserting payload binary form as "data" field in original payload
        payload['data'] = data['binargs']
        # final transaction formed
        trx = {"actions": [payload]}
        import datetime as dt
        trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))
        key = eospy.keys.EOSKey(self.sender_privat_key)
        resp = ce.push_transaction(trx, key, broadcast=True)
        if ('transaction_id' in resp.keys()):
            return resp
        else:
            return ''

    def __get_last_actions(self):
        out = {}
        ce = Cleos(url=eos_endpoint)
        actions = ce.get_actions(self.account, pos=-1, offset=-depth)
        if 'actions' in actions.keys():
            out = actions['actions']
        memos = []
        for s in out:
            receiver = s['action_trace']['receipt']['receiver']
            data = s['action_trace']['act']['data']
            if s['action_trace']['act']['name'] == 'transfer' \
                    and receiver == self.account \
                    and 'to' in data.keys() \
                    and data['to'] == self.account \
                    and 'from' in data.keys() \
                    and 'quantity' in data.keys() \
                    and (data['quantity'].find('EOS') != -1 or data['quantity'].find('KNYGA') != -1):
                data['recv_sequence'] = s['action_trace']['receipt']['recv_sequence']
                data['account'] = s['action_trace']['act']['account']
                memos.append(data)
        # memos.reverse()
        return memos
