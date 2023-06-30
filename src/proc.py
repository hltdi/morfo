import morfo

# Analyzing Guarani word types
def anal_grn(start=0, end=45000):
    morfo.anal_word_counts("grn", "../LingData/Gn/words5.txt", ["tm", "ps", "ns", "po", "no"], write=True)

def proc_grn_feats(pos=None, feat=None):
    """Count different feature values for Guarani word tokens."""
    result = {}
    with open("../LingData/Gn/words5.txt.anl", encoding='utf8') as inf:
        for line in inf:
            item, count = line.split()
            if ';' in item:
                # Otherwise no real analysis, so ignore the line
                count = int(count)
                word, anals = item.split(';')
                anals = anals.split('|')
                nanals = len(anals)
                count1 = count / nanals
                for anal in anals:
                    root_feats = anal.split(':')
                    if len(root_feats) == 1:
                        # No features
                        continue
                    root, feats = anal.split(':')
                    if pos and '_' + pos not in root:
                        continue
                    if feats == '[]':
                        continue
                    feats = morfo.fs.FeatStruct(feats)
                    feats.freeze()
                    if feat:
                        if feat not in feats:
                            continue
                        else:
                            feats = feats[feat]
                    # Update the counts
                    if feats not in result:
                        result[feats] = 0
                    c = result[feats]
                    c = round(c + count1, 2)
                    result[feats] = c
#    result = list(result.items())
#    result.sort(key=lambda x: x[1], reverse=True)
    return result

# Splitting off Grn derived nouns

GNACC = "áéíóúýãẽĩõũỹ"

def split_grn_nouns():
    old = []
    new = []
    with open("morfo/L/grn/lex/n_raizG.lex", encoding='utf8') as file:
        for line in file:
            line = line.strip()
            if ' ' in line:
                old.append(line)
            elif len(line) > 2 and line[-3] in GNACC and line.endswith('va'):
                new.append(line)
            else:
                old.append(line)
    return old, new

def proc_grn_roots(pos=None, features=None):
    """Count different feature-value combinations for each Guarani root that appears
    in word token list."""
    result = {}
    with open("../LingData/Gn/words5.txt.anl", encoding='utf8') as inf:
        for line in inf:
            item, count = line.split()
            if ';' in item:
                # Otherwise no real analysis, so ignore the line
                count = int(count)
                word, anals = item.split(';')
                anals = anals.split('|')
                nanals = len(anals)
                count1 = count / nanals
#                if count1 < 0.2:
#                    print("count1: {}, item: {}, count: {}, n: {}".format(count1, item, count, nanals))
                for anal in anals:
                    root_feats = anal.split(':')
                    if len(root_feats) == 1:
                        # No features
                        if features:
                            continue
                        root = root_feats[0]
                        if pos and '_' + pos not in root:
                            continue
                        if root not in result:
                            result[root] = {}
                        root_feats = result[root]
                        if None not in root_feats:
                            root_feats[None] = 0
                        root_feats[None] += count1
                        continue
                    root, feats = anal.split(':')
                    if pos and '_' + pos not in root:
                        continue
                    if '*' in root:
                        root = root.replace('*', word)
                    root = root.split('_')[0]
                    if root not in result:
                        result[root] = {}
                    root_feats = result[root]
                    if feats == '[]':
                        feats = None
                        if features:
                            continue
                    else:
                        feats = morfo.fs.FeatStruct(feats)
                        feats.freeze()
                        if features:
                            fv = [(feat, feats.get(feat, 'out')) for feat in features]
                            for feat, value in fv:
                                if value != 'out':
                                    if feat not in root_feats:
                                        root_feats[feat] = {}
                                    if value not in root_feats[feat]:
                                        root_feats[feat][value] = 0
                                    rfv = root_feats[feat][value]
                                    rfv = round(rfv + count1, 2)
                                    root_feats[feat][value] = rfv
    todel = []
    for key in result:
        if not result[key]:
            todel.append(key)
    for key in todel:
        del result[key]
##    for item, counts in result.items():
##        for feat, vcounts in counts.items():
##            vcounts = list(vcounts.items())
##            vcounts.sort(key=lambda x: x[1], reverse=True)
##            counts[feat] = vcounts
##    if write:
##        result = list(result.items())
##        result.sort(key=lambda x: x[0])
##        with open(write, 'w', encoding='utf8') as file:
##            for item, counts in result:
##                if counts:
##                    item = item.split('_')[0]
##                    print("{} :: {}".format(item, counts), file=file)
    return result
