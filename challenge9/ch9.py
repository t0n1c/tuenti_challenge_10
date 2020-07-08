
def crack_key(msg, encrypted):
    key = []
    encrypted = [encrypted[i : i + 2] for i in range(0, len(encrypted), 2)]
    for c, hex_char in zip(msg, encrypted):
        cryp_chr = int(hex_char, base=16)
        key_chr = cryp_chr ^ ord(c)
        key.append(str(key_chr))
    return "".join(key)[::-1]


def decrypt(encrypted, key="40614178165780923111223"):
    msg = []
    encrypted = [encrypted[i : i + 2] for i in range(0, len(encrypted), 2)]
    for k, hex_char in zip(reversed(key), encrypted):
        cryp_chr = int(hex_char, base=16)
        asc_chr = cryp_chr ^ int(k)
        msg.append(chr(asc_chr))
    return "".join(msg)


def main():
    #msg = "514;248;980;347;145;332"
    #encrypted = "3633363A33353B393038383C363236333635313A353336"
    #key = crack_key(msg, encrypted)
    #print(key)
    encrypted = "3A3A333A333137393D39313C3C3634333431353A37363D"
    print(decrypt(encrypted))


if __name__ == "__main__":
    main()
