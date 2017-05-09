import socket

def get_my_ip(nat=False):
    if(nat):
        return "152.7.99.61"

    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    val = s.getsockname()[0]
    s.close()
    return val
