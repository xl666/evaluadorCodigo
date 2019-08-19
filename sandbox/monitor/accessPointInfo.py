import subprocess
import sys

def getPid():
    #Obtener pid de create_ap
    instancias = subprocess.Popen(['create_ap', '--list-running'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode('utf-8')
    return instancias.split('\n')[2].split()[0]
        
def getInfoClients(pid):
    res = []
    clientes = subprocess.Popen(['create_ap', '--list-clients', pid], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode('utf-8')
    if not clientes.startswith('No clients connected'):
        res = clientes.split('\n')[1:] #trim headers
    return res

#regresa una version mas confiable de mac e Ip
def getArpaInfo(interface='wlp0s20f0u2'):
    comando = 'arp -a -i %s' % interface
    entradas = subprocess.Popen(comando.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode('utf-8')
    if entradas.startswith('arp:'): #las invalidas empiezan asi
        return []
    return entradas.split('\n')[:-1]

def getMacsConectados(pid):
    clientes = getInfoClients(pid)
    aux = []
    #obtener solo macs
    for c in clientes:
        if c:
            aux.append(c.split()[0])
    return aux

def getIPMacsConectados(interface='wlp0s20f0u2'):
    clientes = getArpaInfo(interface)
    aux = []
    #obtener macs e IPs
    for c in clientes:
        if c:
            partes = c.split()
            aux.append((partes[3].strip(), partes[1].strip()[1:-1]))
    return aux


def getNameMac(mac, users):
    for m, n in users:
        if mac == m:
            return n
    return None

def getMacIp(ip, ipMacs):
    for m, i in ipMacs:
        if i == ip:
            return m
    return None

def getNameIP(ip, ipMacs, users):
    mac = getMacIP(ip, ipMacs)
    return getNameMac(mac, users)


def getUsers(pathMacs):
    users = ''
    with open(pathMacs) as macs:
        users = macs.read()

    users = users.split('\n')[:-1] #last one always empty
    #create tuple
    aux = []
    for u in users:
        aux.append(tuple(u.split(',')))
    return aux



if __name__ == '__main__':
    pid = getPid()
    print(pid)
    pathMacs = sys.argv[1]
    users = getUsers(pathMacs)
    print(users)
    ipMacs = getIPMacsConectados()
    print(ipMacs)
    print(getNameIP('192.168.12.250', ipMacs, users))
