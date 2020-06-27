import morfo

CORP_PATH = "../../Projects/LingData/Es/POS/cess_tags_sents.txt"

CORPUS = []

with open(CORP_PATH, encoding='utf8') as f:
    """Read in the CESS corpus, replacing empty lines with ('EOS', 'X')."""
    for line in f:
        if not line.strip():
            CORPUS.append(('EOS', 'X'))
        else:
            CORPUS.append(line.split())

esanal = lambda word: morfo.anal('spa', word, raw=True)

def anal_v(word, tag):
    '''If word is verb, analyze with morfo, replacing tag with more
    specific one.'''
    if tag == 'v':
        analyses = [a[1] for a in esanal(word.lower())]
        v_anals = [a for a in analyses if a.get('pos') == 'v']
        if not v_anals:
#            print("Something wrong; can't analyze verb {}".format(word))
            return None
        else:
            v_anal = v_anals[0]
            v_tm = v_anal.get('tm')
            if v_tm in ['prc', 'inf', 'ger']:
                return "v." + v_tm
            else:
                return "v.fin"
    else:
        return None

def anal_v_feats(word, tag):
    '''If word is verb, analyze with morfo, replacing tag with more
    specific one.'''
    if tag == 'v':
        analyses = [a[1] for a in esanal(word.lower())]
        v_anals = [a for a in analyses if a.get('pos') == 'v']
        if not v_anals:
#            print("Something wrong; can't analyze verb {}".format(word))
            return None
        else:
            impv = []
            fin = []
            nonfin = []
            for v_anal in v_anals:
                tm = v_anal.get('tm')
                if tm == 'ipv':
                    impv.append(v_anal)
                elif tm in ['prc', 'inf', 'ger']:
                    nonfin.append(v_anal)
                else:
                    fin.append(v_anal)
            if fin:
                if not impv and not nonfin:
                    return "v.fin"
            elif impv and not nonfin:
                return "v.ipv"
    else:
        return None

def proc_v():
    '''Do anal_v on whole corpus.'''
    for word_tag in CORPUS:
        if len(word_tag) < 2:
            print("Something wrong with {}".format(word_tag))
        tag = anal_v(word_tag[0], word_tag[1])
        if tag:
            word_tag[1] = tag
            

def proc_v_feats():
    '''Do anal_v_feats on whole corpus.'''
    n_ipv = 0
    for index, word_tag in enumerate(CORPUS):
        if (index + 1) % 1000 == 0:
            print("Processed {} words".format(index))
        if len(word_tag) < 2:
            print("Something wrong with {}".format(word_tag))
        tag = anal_v_feats(word_tag[0], word_tag[1])
        if tag:
            if tag == 'v.ipv':
                n_ipv += 1
            word_tag[1] = tag
    return n_ipv

def write_corp(path="../../Projects/LingData/Es/POS/cess_tags_sents3.txt"):
    '''Write the modified corpus.'''
    with open(path, 'w', encoding='utf8') as f:
        for word, tag in CORPUS:
            if word == 'EOS':
                print(file=f)
            else:
                print("{} {}".format(word, tag), file=f)
