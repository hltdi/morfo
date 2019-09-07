import morfo

CORP_PATH = "../../Projects/LingData/Es/POS/cess_tags_sents.txt"

CORPUS = []
with open(CORP_PATH, encoding='utf8') as f:
    for line in f:
        if not line.strip():
            CORPUS.append(('EOS', 'X'))
        else:
            CORPUS.append(line.split())

esanal = lambda word: morfo.anal('spa', word, raw=True)

def anal_v(word, tag):
    if tag == 'v':
        analyses = [a[1] for a in esanal(word.lower())]
        v_anals = [a for a in analyses if a.get('pos') == 'v']
        if not v_anals:
            print("Something wrong; can't analyze verb {}".format(word))
            return None
        else:
            v_anal = v_anals[0]
            v_tm = v_anal.get('tm')
            if v_tm in ['prc', 'inf', 'ger']:
                return "v.nonfin"
            else:
                return "v.fin"
    else:
        return None

def proc_v():
    for word_tag in CORPUS:
        if len(word_tag) < 2:
            print("Something wrong with {}".format(word_tag))
        tag = anal_v(word_tag[0], word_tag[1])
        if tag:
            word_tag[1] = tag

def write_corp(path="../../Projects/LingData/Es/POS/cess_tags_sents2.txt"):
    with open(path, 'w', encoding='utf8') as f:
        for word, targ in CORPUS:
            if word == 'EOS':
                print(file=f)
            else:
                print("{} {}".format(word, tag), file=f)
