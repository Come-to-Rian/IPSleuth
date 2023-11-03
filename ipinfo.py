""" Busca informações sobre o IP por meio de uma API """

import requests
from time import sleep

# API usada para conseguir informações sobre o IP
whoisapi = "https://ipwho.is/"


class IPInfo:
    def __init__(self, ip_addr):
        self.ip_info = self._get_ip_info(ip_addr)
        self.format_template = "%-15s %-30s %-15s %s"


    def _get_ip_info(self, ip):

        if self._check_privateip(ip):
            print(f"\033[91mIP reservado (privado): {ip}\033[00m")
            return None
        
        response = requests.get(f'{whoisapi}{ip}')

        if response.status_code == 200:
            if response.json()['success'] == True : return response.json()

        else:
            print('Error:', response.status_code)
            return None
    

    def _check_privateip(self, ip):
        octetos = ip.split(".")

        if octetos[0] == "10":
            return True

        if octetos[0] == "172" and octetos[1] >= "16" and octetos[1] <= "31":
            return True

        if octetos[0] == "192" and octetos[1] == "168":
            return True

        return False


    @property
    # Exibe informações regionais sobre o IP
    def display_ipinfo(self):

        if self.ip_info == None:
            return
        
        print('\033[92mLOCALIZAÇÂO\033[00m')

#        pais = f"{self.ip_info['flag']['emoji']} {self.ip_info['country']}-{self.ip_info['country_code']}" # Opção com bandeira do país
        pais = f"{self.ip_info['country']}-{self.ip_info['country_code']}" # sem a bandeira do país

        estado = f"{self.ip_info['region']}-{self.ip_info['region_code']}"
        cidade = self.ip_info['city']
        latlon = str(f"{self.ip_info['latitude']:.2f}:{self.ip_info['longitude']:.2f}")

        print(self.format_template % ('País ', 'Estado', 'Cidade', 'LAT:LON'))
        print(self.format_template % (pais, estado, cidade, latlon))


    @property
    # Exibe informações da conexão como o provedor, orgão
    def display_coninfo(self):
        if self.ip_info == None:
            return

        print('\033[93mCONEXÃO\033[00m')

        connection = self.ip_info['connection']
        asn = str(connection['asn'])
        orgao = connection['org']
        isp = connection['isp']
        dominio = connection['domain']

        print(self.format_template % ('ASN', 'Orgao', 'ISP', 'Dominio'))
        print(self.format_template % (asn, orgao, isp, dominio))


    @property
    # Não disponivel
    def display_secinfo(self):
        if self.ip_info == None:
            return
        
        print("\033[91mSEGURANÇA:\033[00m ")

        template = "%15s %15s %15s %15s"

        sec = self.ip_info['security']
        anonimo = sec['anonymous']
        proxy = sec['proxy']
        vpn = sec['vpn']
        tor = sec['tor']
        hosting = sec['hosting']

        print(template % ('Anonimo', 'Proxy', 'VPN', 'TOR', 'Hosting'))
        print(template % (anonimo, proxy, vpn, tor, hosting))




if __name__ == '__main__':
    IPInfo('8.8.8.8').display_ipinfo