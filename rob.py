# -*- coding: utf-8 -*-
__author__ = 'marcin'

def u(s):
    return unicode(s, 'utf-8').encode('utf-8')


print "ąśćłóþ"

print u("ąśćłóþ")