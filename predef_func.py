def punzal_print():


    def eval(*args):
        for arg in args:
            print arg


class PreDefFunc(dict):
    self = {}
    self['print'] = {"TYPE": "Function", "BODY": punzal_print()}


def appendlist(self, x=list()):
    ret = list()
    for i in x:
        if type(i) is list:
            ret = appendlist(i)
            print ret
        else:
            ret.append(i)
    return ret
