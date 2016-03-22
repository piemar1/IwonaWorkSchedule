__author__ = 'marcin'



name = "marcin pieczynski"


def filtr(elem):
    if elem in ('aeomi'):
        return True
    return False


re = filter(filtr, name)
print re