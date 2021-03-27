def BitCheck(a):
    return 1 if a > 0 else 0


def ShortBitCheck(a, b, c):
    return BitCheck(a) + BitCheck(b) + BitCheck(c)


ShortBitCheck(1, 0, 1)
