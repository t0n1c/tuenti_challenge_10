from math import gcd


def load_bin(filepath):
    with open(filepath, "rb") as fp:
        return fp.read()


def get_modulus(text1, text2, ciphered1, ciphered2):
    """The key in this challenge was to realize there were no padding and 
    therefore it might be a textbook RSA. It is deterministic. I totally forgot 
    about the math behind the RSA. So i had to study a little bit. Then after 
    doing the proper encoding (math work with numbers!),and using some fundamental
    arithmetic notions you come to the next pair of equations:
    
    m1**e = c1 + n * d1 
    m2**e = c2 + n * d2
    
    where
 
    n: modulus (thats what we have to figure out)
    m: message
    c: ciphered
    e: public exponent (we dont know. We know (n, e) forms the public key)
    d: a quotient (another x to solve for? We dont want that!)
    we know that n = p*q (being p and q large --prime-- numbers)
    we know that n must divide a=(m1**e -c1) AND b=(m2**e -c2). So there you have
    a divisor, the greatest! actually. since n = p*q and those are primes.
    So we get our n by trying different exponents e and when gcd(a,b)!= 1

    """
    commom_e = [3, 5, 17, 37, 257, 65537]
    for byteorder in ["big", "little"]:
        for strip_flag in [False, True]:
            if strip_flag:
                data = [d.strip() for d in [text1, ciphered1, text2, ciphered2]]
            else:
                data = [text1, ciphered1, text2, ciphered2]

            data = [int.from_bytes(d, byteorder) for d in data]
            m1, c1, m2, c2 = data
            for e in commom_e:
                n = gcd(m1 ** e - c1, m2 ** e - c2)
                if n != 1: #it measn m1 ** e % n == c1
                    return n


def main():
    paths = [
        "plaintexts/test1.txt",
        "plaintexts/test2.txt",
        "ciphered/test1.txt",
        "ciphered/test2.txt",
    ]
    data = [load_bin(path) for path in paths]
    print(get_modulus(*data))



if __name__ == "__main__":

    main()
