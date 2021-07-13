
import numpy as np
import math

MAX_VAL = 1000000 # ...


class TrieNode:

    def __init__(self, char, parent):

        self.char        = char
        self.parent      = parent
        self.idx_word    = -1
        self.children    = {}
        self.old_cost    = MAX_VAL
        self.cost        = MAX_VAL
        self.active      = False

    def reset(self):
        self.old_cost    = MAX_VAL
        self.cost        = MAX_VAL
        self.active      = False

        for k in self.children.keys():
            self.children[k].reset()

    def add(self, word, idx_word):

        if len(word)==0: return False # should not happen

        c         = word[0]
        remaining = word[1:]
        
        if c in self.children:
            node = self.children[c]
        else:
            node = TrieNode(c, self)
            self.children[c] = node

        if len(remaining)>0:
            return node.add(remaining, idx_word)

        node.idx_word = idx_word
        return True
    

    def find_index_of(self, word):

        if len(word)==0: return self.idx_word
                    
        c = word[0]
        remaining = word[1:]
        
        if c in self.children:
            node = self.children[c]
            if len(remaining)==0:
                return node[c].idx_word
            else:
                return node.find_index_of(remaining)
        return -1

    def get_all_descendent(self):

        L = []
        for c in self.children:
            L = L + [self.children[c]] + self.children[c].get_all_descendent()

        return L

    
################################################################################################
def load_dictionary(filename):
    
    root  = TrieNode('', None)
    words = []
    with open(filename, 'r') as file:

        for line in file:
            word = line.rstrip('\n')
            words.append(word)
            root.add(word, len(words)-1)

    return words, root
            
################################################################################################

# search version 1 without prunning, always keep all nodes in working mem
def nn_search(root, b):

    root.reset()
    root.old_cost = -1
    root.active   = True

    all_nodes = root.get_all_descendent() # all except root
    
    n = len(b)
    for j in range(1, n+1):

        # propagate score
        root.old_cost = root.old_cost + 1
        for node in all_nodes:
            node.old_cost = min(node.old_cost, node.parent.old_cost+1)

        # update for new character
        for node in all_nodes:
            c2 = node.old_cost + 1
            c3 = (0 if node.char == b[j-1] else 0.99) + node.parent.old_cost*1.01
            
            node.cost = min(c2, c3)

        # update old_cost
        for node in all_nodes:
            node.old_cost = node.cost

    # propagate score
    for node in all_nodes:
        node.old_cost = min(node.old_cost, node.parent.old_cost+1)
    
    # find best terminal node
    ed, idx_word = MAX_VAL, -1
    for node in all_nodes:
        if node.idx_word==-1: continue

        if ed>node.old_cost:
            ed       = node.old_cost
            idx_word = node.idx_word


    return idx_word, ed
    

################################################################################################

def expand(node, L, threshold):

    if node.old_cost + 1 >= threshold: return

    for c in node.children:
        if not node.children[c].active:
            node.children[c].old_cost = node.old_cost+1
            node.children[c].active   = True 
            
            L.append(node.children[c])

            expand(node.children[c], L, threshold)
    
    

# search version 2 with prunning
def approx_nn_search(root, b, beam):

    threshold = beam

    root.reset()
    root.old_cost = -1
    root.active   = True

    active_nodes = [root]
    
    n = len(b)
    for j in range(1, n+1):

        # propagate score
        for node in active_nodes:
            if node.parent is None or not node.parent.active:
                node.old_cost = node.old_cost + 1
            else:
                node.old_cost = min(node.old_cost, node.parent.old_cost+1)

        # expand for new nodes
        L = []
        for node in active_nodes:
            expand(node, L, threshold)
        active_nodes = active_nodes + L
            
        
        # update for new character
        for node in active_nodes:
            c2 = node.old_cost + 1
            if node.parent is None or not node.parent.active:
                node.cost = min(node.old_cost, c2)
            else:
                c3 = (0 if node.char == b[j-1] else 0.99) + node.parent.old_cost*1.01
                node.cost = min(c2, c3)


        # update threshold
        threshold = min([node.cost for node in active_nodes]) + beam
                
        # update old_cost
        new_nodes = []
        for node in active_nodes:
            if node.cost<threshold:
                node.old_cost = node.cost
                new_nodes.append(node)                
            else:
                node.active = False

        active_nodes = new_nodes
                
    # propagate score
    for node in active_nodes:
        if node.parent is None or not node.parent.active:
            node.old_cost = node.old_cost + 1
        else:
            node.old_cost = min(node.old_cost, node.parent.old_cost+1)
    
    # find best terminal node
    ed, idx_word = MAX_VAL, -1
    for node in active_nodes:
        if node.idx_word==-1: continue

        if ed>node.old_cost:
            ed       = node.old_cost
            idx_word = node.idx_word


    return idx_word, ed
    

################################################################################################
def spell_correction(words, root, beam, transit_cost, separator, query):
    
    word_graph = word_graph_construction(words, root, beam, query)
    result = best_path(word_graph, len(query), transit_cost)
    #print(result)

    return separator.join(result)
    
def word_graph_construction(words, root, beam, b):

    word_graph = []
    n = len(b)
    for beg in range(n-1):
        for end in range(beg+1, n+1):
            idx,ed = approx_nn_search(root, b[beg:end], beam)
            word_graph.append( (beg, end, words[idx], ed) )
            
    return word_graph


def best_path(word_graph, l, transit_cost):

    best_accum_score = MAX_VAL * np.ones(l+1)
    best_candidate   = -1 * np.ones(l+1, dtype=np.int)
    best_accum_score[0] = 0
    for i in range(l):
        for j, (beg, end, w, ed) in enumerate(word_graph):
            if beg == i:
                s = best_accum_score[beg] + ed + transit_cost
                if s < best_accum_score[end]:
                    best_accum_score[end] = s
                    best_candidate[end]   = j

                    
    

    result = []
    t = l
    while(t>0):
        j = best_candidate[t]
        if j==-1: #
            print('Something\'s wrong! The word_graph does not contain any complete path. Please try again with larger \'beam\'')
            return result
        
        (beg, end, w, ed) = word_graph[j]
        result.insert(0, w)

        t = beg

    return result

################################################################################################
import argparse

from enum import Enum
class Op(Enum):
    search        = 1
    approx_search = 2
    spell         = 3

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return Op[s]
        except KeyError:
            raise ValueError()
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('op', type=Op.from_string, choices=list(Op))
    parser.add_argument('-d', '--dict', type=str, help='the dictionary', required=True) 
    parser.add_argument('-q', '--query', type=str, help='the query string without quotes', required=True) 
    parser.add_argument('-b', '--beam', type=int, default=3)
    parser.add_argument('--transit_cost', type=int, default=1)
    parser.add_argument('--sep', type=str, default='', help='the word separator')

    args = parser.parse_args()


    words,root = load_dictionary(args.dict)

    print(args.op)
    
    if args.op == Op.search:
        idx, score = nn_search(root, args.query)
        print('query \'%s\' || closest \'%s\', distance %d' % (args.query, words[idx], score))

    elif args.op == Op.approx_search:
        idx, score = approx_nn_search(root, args.query, 3)
        print('query \'%s\' || closest \'%s\', distance %d' % (args.query, words[idx], score))

    else:
        res = spell_correction(words, root, args.beam, args.transit_cost, args.sep, args.query)
        print(res)
