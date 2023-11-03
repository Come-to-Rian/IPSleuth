import argparse

from time import sleep

from connections import Connections
from ipinfo import IPInfo


description = """Esse programa mostra conexões no socket à algum IP remoto, 
                 com funcionalidade de verificar informações sobre cada um desses IPs """


class Main():
    def __init__(self) -> None:
        self.connections = Connections()
        self.con_ips = self.connections.filtered_con['IP Remoto']

    def display_con(self):
        sleep(0.5)

        print('-=' * 40)
        self.connections.display
        print('-=' * 40)

    
    def display_ipinfo(self):
        sleep(0.5)

        for ip in self.con_ips:
            ip_info = IPInfo(ip.split(':')[0])
            sleep(0.5)
            ip_info.display_ipinfo
            ip_info.display_coninfo
            sleep(2)

        print('-=' * 40)
        




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--Info', action='store_true', help='Mostra inforamções sobre os IPs')
    
    args = parser.parse_args()

    a = Main()
    a.display_con()
    if args.Info:
        a.display_ipinfo()