from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABdNN_XjnZXj19TT4hzP68DWT7HFXvKfdgCDKrFqHAyBWEerBddgjczhISp71jJuaCw3slr09IVoMSUk90rNR3r4sq_6eOVgApJVMneJJH5_7pdMLiECZ3l6GBLbmUdx1jQVOR60m5DFCJXpC-sQOusUyknbn-yY6yk5pRzmzU2vSLgwDk='

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
    