def LongBitCheck(a, b, c):
    retval = 0
    if a > 0:
        retval = retval + 1
    if b > 0:
        retval = retval + 1
    if c > 0:
        retval = retval + 1
    return retval


LongBitCheck(1, 0, 1)
