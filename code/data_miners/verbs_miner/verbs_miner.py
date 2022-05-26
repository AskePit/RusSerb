import os
import sys
sys.path.insert(0, '../../../')
from code.data_miners.miner_common import *

verbs = [
]

nonTabledVerbs = [
]

modalVerbs = [
    ('morati', 'должен'),
    ('moći', 'мочь'),
    # ('treba', 'надо'),
    # ('znati', 'уметь'),
    # ('umeti', 'уметь'),
    # ('smeti', 'мочь'),
    # ('želeti', 'желать'),
    # ('voleti', 'любить'),
    # ('hteti', 'хотеть'),
]

class VerbDownloader(TableDownloader):
    def loadCustom(self) -> DownloadStatus:
        return DownloadStatus.Ok

def downloadVerb(verbPair: tuple[str, str], o: Writer) -> DownloadStatus:
    print(verbPair)

    serbVerb, rusVerb = verbPair

    serbOk, serb = VerbDownloader(serbVerb, 'https://sh.wiktionary.org/wiki', 'div', 'NavContent')()
    rusOk, rus   = VerbDownloader(rusVerb, 'https://ru.wiktionary.org/wiki', 'table', 'morfotable ru')()

    print(serbOk)
    if serbOk != DownloadStatus.Ok:
        return serbOk

    Sing1 = 0
    Sing2 = 1
    Sing3 = 2
    Plur1 = 3
    Plur2 = 4
    Plur3 = 5

    Present = 0
    Past = 1
    Povel = 2

    Male = 0
    Female = 1
    Neutral = 2

    o.setTables(serb, rus)
    o.write(serbVerb)
    o.write('\nnone\n\n')

    o.writeLine('inf', rusVerb, serbVerb)
    o.endl()
    
    o.writeDecl('present & sing & first',  Cell('Я', Present), Cell('Prezent', Sing1))
    o.writeDecl('present & sing & second', Cell('Ты', Present), Cell('Prezent', Sing2))
    o.writeDecl('present & sing & third',  Cell('Он', Present), Cell('Prezent', Sing3))
    o.writeDecl('present & plur & first',  Cell('Мы', Present), Cell('Prezent', Plur1))
    o.writeDecl('present & plur & second', Cell('Ты', Present), Cell('Prezent', Plur2))
    o.writeDecl('present & plur & third',  Cell('Они', Present), Cell('Prezent', Plur3))
    o.endl()

    def GetSinglePast(s: str, i: int):
        n = int((len(s) - 4) / 3)
        # могмогламогло -> мог могла могло
        return [s[:n], s[n:(2*n+2)], s[(2*n+2):]][i]
    
    def SplitParticiple(adjective: str, i: int):
        #print(adjective)
        splitted = adjective.split('/')
        if len(splitted) < 3:
            return ('', '', '')

        m = splitted[0].strip()[:-3]
        f = splitted[1].strip()[:-3]
        n = splitted[2].strip()[:-2]
        
        #print([m, f, n])
        return [m, f, n][i]

    o.writeDecl('perfect & sing & male', Cell('Он', Past, GetSinglePast, Male), Cell('Glagolski pridjev radni', 0, SplitParticiple, Male))
    o.writeDecl('perfect & sing & fem',  Cell('Он', Past, GetSinglePast, Female), Cell('Glagolski pridjev radni', 0, SplitParticiple, Female))
    o.writeDecl('perfect & sing & neu',  Cell('Он', Past, GetSinglePast, Neutral), Cell('Glagolski pridjev radni', 0, SplitParticiple, Neutral))
    o.writeDecl('perfect & plur & male', Cell('Они', Past), Cell('Glagolski pridjev radni', 1, SplitParticiple, Male))
    o.writeDecl('perfect & plur & fem',  Cell('Они', Past), Cell('Glagolski pridjev radni', 1, SplitParticiple, Female))
    o.writeDecl('perfect & plur & neu',  Cell('Они', Past), Cell('Glagolski pridjev radni', 1, SplitParticiple, Neutral))
    o.endl()
    
    def SplitFutur1(futur: str, i: int):
        futur = futur.replace('\n', ' ')
        splitted = futur.split(' ')
        futur_1 = (splitted[0] + ' ' + splitted[1]).strip()
        splitted = splitted[2:]
        futur_2 = ' '.join(splitted).strip()

        #print([futur_1, futur_2])
        return [futur_1, futur_2][i]

    o.writeDecl('futur & sing & first',  None, Cell('Futur I', Sing1, SplitFutur1, 1))
    o.writeDecl('futur & sing & second', None, Cell('Futur I', Sing2, SplitFutur1, 1))
    o.writeDecl('futur & sing & third',  None, Cell('Futur I', Sing3, SplitFutur1, 1))
    o.writeDecl('futur & plur & first',  None, Cell('Futur I', Plur1, SplitFutur1, 1))
    o.writeDecl('futur & plur & second', None, Cell('Futur I', Plur2, SplitFutur1, 1))
    o.writeDecl('futur & plur & third',  None, Cell('Futur I', Plur3, SplitFutur1, 1))
    o.endl()

    o.writeDecl('imperfect & sing & first',  Cell('Он', Past, GetSinglePast, Male), Cell('Imperfekt', Sing1))
    o.writeDecl('imperfect & sing & second', Cell('Он', Past, GetSinglePast, Female), Cell('Imperfekt', Sing2))
    o.writeDecl('imperfect & sing & third',  Cell('Он', Past, GetSinglePast, Neutral), Cell('Imperfekt', Sing3))
    o.writeDecl('imperfect & plur & first',  Cell('Они', Past), Cell('Imperfekt', Plur1))
    o.writeDecl('imperfect & plur & second', Cell('Они', Past), Cell('Imperfekt', Plur2))
    o.writeDecl('imperfect & plur & third',  Cell('Они', Past), Cell('Imperfekt', Plur3))
    o.endl()

    o.writeLine('# participle & present', None, serb.parseColumnedCell('Glagolski prilog sadašnji:'))
    o.writeLine('# participle & past', None, serb.parseColumnedCell('Glagolski prilog prošli:'))
    o.writeLine('# noun', None, serb.parseColumnedCell('Glagolska imenica:'))
    o.endl()

    o.writeDecl('# futur & sing & first',  None, Cell('Futur I', Sing1, SplitFutur1, 0))
    o.writeDecl('# futur & sing & second', None, Cell('Futur I', Sing2, SplitFutur1, 0))
    o.writeDecl('# futur & sing & third',  None, Cell('Futur I', Sing3, SplitFutur1, 0))
    o.writeDecl('# futur & plur & first',  None, Cell('Futur I', Plur1, SplitFutur1, 0))
    o.writeDecl('# futur & plur & second', None, Cell('Futur I', Plur2, SplitFutur1, 0))
    o.writeDecl('# futur & plur & third',  None, Cell('Futur I', Plur3, SplitFutur1, 0))
    o.endl()

    o.writeDecl('# futur2 & sing & first',  None, Cell('Futur II', Sing1))
    o.writeDecl('# futur2 & sing & second', None, Cell('Futur II', Sing2))
    o.writeDecl('# futur2 & sing & third',  None, Cell('Futur II', Sing3))
    o.writeDecl('# futur2 & plur & first',  None, Cell('Futur II', Plur1))
    o.writeDecl('# futur2 & plur & second', None, Cell('Futur II', Plur2))
    o.writeDecl('# futur2 & plur & third',  None, Cell('Futur II', Plur3))
    o.endl()

    o.writeDecl('# aorist & sing & first',  None, Cell('Aorist', Sing1))
    o.writeDecl('# aorist & sing & second', None, Cell('Aorist', Sing2))
    o.writeDecl('# aorist & sing & third',  None, Cell('Aorist', Sing3))
    o.writeDecl('# aorist & plur & first',  None, Cell('Aorist', Plur1))
    o.writeDecl('# aorist & plur & second', None, Cell('Aorist', Plur2))
    o.writeDecl('# aorist & plur & third',  None, Cell('Aorist', Plur3))
    o.endl()

    o.writeDecl('# cond1 & sing & first',  None, Cell('Kondicional I.', Sing1))
    o.writeDecl('# cond1 & sing & second', None, Cell('Kondicional I.', Sing2))
    o.writeDecl('# cond1 & sing & third',  None, Cell('Kondicional I.', Sing3))
    o.writeDecl('# cond1 & plur & first',  None, Cell('Kondicional I.', Plur1))
    o.writeDecl('# cond1 & plur & second', None, Cell('Kondicional I.', Plur2))
    o.writeDecl('# cond1 & plur & third',  None, Cell('Kondicional I.', Plur3))
    o.endl()

    o.writeDecl('# cond2 & sing & first',  None, Cell('Kondicional II.', Sing1))
    o.writeDecl('# cond2 & sing & second', None, Cell('Kondicional II.', Sing2))
    o.writeDecl('# cond2 & sing & third',  None, Cell('Kondicional II.', Sing3))
    o.writeDecl('# cond2 & plur & first',  None, Cell('Kondicional II.', Plur1))
    o.writeDecl('# cond2 & plur & second', None, Cell('Kondicional II.', Plur2))
    o.writeDecl('# cond2 & plur & third',  None, Cell('Kondicional II.', Plur3))
    o.endl()

    o.writeDecl('# imperativ & sing & first',  Cell('Я', Povel), Cell('Imperativ', Sing1))
    o.writeDecl('# imperativ & sing & second', Cell('Ты', Povel), Cell('Imperativ', Sing2))
    o.writeDecl('# imperativ & sing & third',  Cell('Он', Povel), Cell('Imperativ', Sing3))
    o.writeDecl('# imperativ & plur & first',  Cell('Мы', Povel), Cell('Imperativ', Plur1))
    o.writeDecl('# imperativ & plur & second', Cell('Вы', Povel), Cell('Imperativ', Plur2))
    o.writeDecl('# imperativ & plur & third',  Cell('Они', Povel), Cell('Imperativ', Plur3))
    o.endl()

    o.writeDecl('# passive & sing & male', None, Cell('Glagolski pridjev trpni', 0, SplitParticiple, Male))
    o.writeDecl('# passive & sing & fem',  None, Cell('Glagolski pridjev trpni', 0, SplitParticiple, Female))
    o.writeDecl('# passive & sing & neu',  None, Cell('Glagolski pridjev trpni', 0, SplitParticiple, Neutral))
    o.writeDecl('# passive & plur & male', None, Cell('Glagolski pridjev trpni', 1, SplitParticiple, Male))
    o.writeDecl('# passive & plur & fem',  None, Cell('Glagolski pridjev trpni', 1, SplitParticiple, Female))
    o.writeDecl('# passive & plur & neu',  None, Cell('Glagolski pridjev trpni', 1, SplitParticiple, Neutral))
    o.finishWord()

    return DownloadStatus.Ok

def generateVerb(verb: str):
    print('{} generation'.format(verb))
    pass

ExecuteMiner(SpeechPart.verb, verbs+modalVerbs+nonTabledVerbs, downloadVerb, generateVerb, 'out.txt')