""" Listar todas conexões com alguma IP remoto por meio dos sockets """


import socket
from socket import AF_INET
from socket import SOCK_DGRAM
from socket import SOCK_STREAM
from datetime import datetime

import psutil

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (SOCK_STREAM): 'tcp',
    (SOCK_STREAM): 'tcp', # TODO: tcp6
    (SOCK_DGRAM): 'udp',
    (SOCK_DGRAM): 'udp', # TODO: udp6
}



# TODO: IPV6 support


class Connections:
    def __init__(self):

        self.text_template = "%-15s %-25s %-13s %s"

        self.con = self._get_connections(); 
        self.filtered_con = self._filter_connections(self.con); # Dicionário selecionado com informações úteis


    # Exibe as conexões organizadas
    @property
    def display(self):

        now = datetime.now()
        c_time = now.strftime("%H:%M:%S")
        print(f"Reportado {self.filtered_con['Total']} conexões às {c_time}.")

        print(self.text_template % ('Protocolo', 'IP Remoto', 'Status', 'Aplicacao'))
        
        # Iteração para cada conexão 
        for c in range(0, self.filtered_con['Total']):
            print(self.text_template % (
                self.filtered_con['Protocolo'][c],
                self.filtered_con['IP Remoto'][c],
                self.filtered_con['Status'][c],
                self.filtered_con['Aplicacao'][c]))


    # Retorna conexões que estão ativas ou paradas
    def _get_connections(self):
        connections = list();
        for c in psutil.net_connections(kind='inet'):
            if (c.raddr):
                connections.append(c)

            else:
                continue

        return connections

    # Filtra as conexões com informações úteis e retorna um dict
    def _filter_connections(self, connections = []) -> dict:
        filtered_con = {'Total' : 0, 'Protocolo' : [], 'IP Remoto' : [], 'Status' : [], 'Aplicacao' : []}

        # Organiza os dados adicionando no dicionário
        for c in connections:
            filtered_con['Total'] += 1;
            filtered_con['Protocolo'].append(proto_map[c.type])
            filtered_con['IP Remoto'].append("%s:%s" %(c.raddr))
            filtered_con['Status'].append(c.status)

            # Caso há um valor PID, procura pelo nome de sua aplicação, caso não, só adiciona o valor
            if c.pid : filtered_con['Aplicacao'].append(self._get_app(c.pid))
            else : filtered_con['Aplicacao'].append(c.pid)

        return filtered_con

    # Retorna nome da aplicacao baseado no PID
    def _get_app(self, pid) -> str:
        if psutil.pid_exists(pid):
            for p in psutil.process_iter(['pid', 'name']):
                if p.info['pid'] == pid:
                    return str(p.info['name'])



if __name__ == '__main__':
    Connections()
