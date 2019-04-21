
TERM = '**'
COUNT = '//'
class Trie (object):
    def __init__ (self):
        self.root = {}
        self.root[COUNT] = 0

    def add (self, a):
        n = self.root
        for i in a:
            if i not in n:
                n[i] = {}
                n[i][COUNT] = 1
            else:
                n[i][COUNT] += 1
            n = n[i]
        n[TERM] = None

    def find (self, a):
        n = self.root
        for i in a:
            if i not in n:
                return 0
            n = n[i]
        return n[COUNT]

    @staticmethod
    def countTerms (n):
        t = 0
        for i in n:
            if i == TERM:
                t += 1
            else:
                t += Contacts.countTerms(n[i])
        return t
        
