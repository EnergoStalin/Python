def ToBase(num: int, base: int):
    if num < base:
        return num
    cvt = ""
    while(num >= base):
        cvt += str(num % base)
        num //= base
    return (cvt + str(num))[::-1]