import pymongo
from contextlib import ContextDecorator


class get_mconn(ContextDecorator):
    def __init__(self):
        try:
            self.client = ''
        except Exception as err:
            print('err init\n\n' + str(err))

    def __enter__(self):
        try:
            self.client = pymongo.MongoClient("mongodb+srv://user:12345678S@cluster0.cfolx.mongodb.net/miner_app?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE")
            
            db = self.client.miner_app

            return db
        except Exception as err:
            print('err enter\n\n' + str(err))

    def __exit__(self, *exc):
        try:
            self.client.close()
            return False
        except Exception as err:
            print('err exit\n\n' + str(err))