#!/usr/bin/python3

from elasticsearch import Elasticsearch
from datetime import datetime
from croniter import croniter
from threading import Thread
import socket
import json
import pause
import logging
import getpass
import sys

ls = []

class Apk:
    """
        Send syslog UDP packet to given host and port.
        """

    def __init__(self, host='127.0.0.1', port=514, configaddr='config.json'):
        self.host = host
        self.port = port
        self.configaddr = configaddr
        self.log = Log()

    def syslog(self, message):
        host = self.host
        port = self.port
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(str(message).encode(), (host, port))
        except Exception as e:
            print(e)
        sock.close()
        self.log.logger.info(f"Document {message['_id']} from index {message['_index']} stored in syslog")

    def check_index(self, data, index):
        es = Elasticsearch("localhost:9200")
        base = datetime.now()
        itr = croniter(data['check_time'], base)
        while True:
            next_time = itr.get_next(datetime)
            pause.until(next_time)
            res = {}
            try:
                res = es.search(index=index, body={"_source": False, "query": {
                    "match_all": {}
                }})
            except Exception as e:
                print(e)
            """
                compare number of total document in an index and maximum documents could it have.
                """
            if int(res['hits']['total']['value']) > int(data['max_value']):
                try:
                    """
                    gets old documents that need to be deleted.
                    """
                    res = es.search(index=index, size=int(res['hits']['total']['value']), body={
                        "from": data['max_value'],
                        "query": {
                            "match_all": {}
                        },
                        "sort": [
                            {
                                "created": {
                                    "order": "desc"
                                }
                            }
                        ]
                    })
                except Exception as e:
                    print(e)
                this = sys.modules[__name__]
                """
                sends documents to syslog service
                """
                for doc in res['hits']['hits']:
                    self.syslog(doc)
                setattr(this, '%s_additional_doc_id' % index, [])
                """"
                appends document's ids that need to be deleted to a list
                """
                for id in res['hits']['hits']:
                    getattr(this, '%s_additional_doc_id' % index).append(id['_id'])

                    """
                    deletes documents in index that their Ids are in ids[]
                    """
                try:
                    es.delete_by_query(index=index, body={
                        "query": {
                            "terms": {
                                "_id": getattr(this, '%s_additional_doc_id' % index)
                            }
                        }
                    })
                except Exception as e:
                    print(e)
                self.log.logger.info(
                    f"{int(res['hits']['total']['value']) - int(data['max_value'])} documents deleted from index {index}. ")

    def make_thread(self, data, index):
        global ls
        t = Thread(target=self.check_index, args=[data, index])
        ls.append(t)
        t.start()

    def run(self):
        self.log.logger.info(f"Script ran by {getpass.getuser()}")
        try:
            with open(self.configaddr, "r") as file:
                data = json.load(file)
                for index in data:
                    self.make_thread(data[index], index)
        except Exception as e:
            print(e)


class Log:
    def __init__(self):
        logging.basicConfig(filename="apk.log",
                            format='%(asctime)s %(message)s',
                            filemode='a+')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
