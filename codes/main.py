from apk import Apk
import argparse
from conf_api import ConfApi

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', "--configaddr", dest='configaddr', help="Address of config file.", type=str,
                        default='/home/javad/PycharmProjects/apk/config.json')
    # parser.add_argument('-P', "--port", dest='port', help="Syslog port.", type=int, default=514)
    parser.add_argument('-H', "--host", dest='host', help="Remote syslog server ip.", type=str, default="127.0.0.1")
    args = parser.parse_args()

    apk = Apk(host=args.host, configaddr=args.configaddr)
    config = ConfApi()
    apk.run()
    config.run()
