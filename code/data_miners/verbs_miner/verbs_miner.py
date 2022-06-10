import os
import sys
sys.path.insert(0, '../../../')
from code.data_miners.miner_common import *

class VerbDownloader(TableDownloader):
    def loadCustom(self) -> DownloadStatus:
        return DownloadStatus.Ok

def downloadVerb(verbPair: tuple[str, str], o: Writer) -> DownloadStatus:
    print(verbPair)

    serbVerb, rusVerb = verbPair

    SH = 0
    EN = 1

    serbPage = EN

    serbOk, serb = VerbDownloader(serbVerb, 'https://en.wiktionary.org/wiki', 'Serbo-Croatian', 'table', 'inflection-table')()
    rusOk, rus   = VerbDownloader(rusVerb, 'https://ru.wiktionary.org/wiki', None, 'table', 'morfotable ru')()

    if serbOk != DownloadStatus.Ok:
        # try to fallback to `sh` version
        serbOk, serb = VerbDownloader(serbVerb, 'https://sh.wiktionary.org/wiki', 'Srpskohrvatski', 'div', 'NavContent')()
        serbPage = SH

    print(serbOk)
    if serbOk != DownloadStatus.Ok:
        return serbOk

    Present       = ['Prezent',                    'Present'                ][serbPage]
    Active        = ['Glagolski pridjev radni',    'Active past participle' ][serbPage]
    Passive       = ['Glagolski pridjev trpni',    'Passive past participle'][serbPage]
    FutureI       = ['Futur I',                    'Future I'               ][serbPage]
    FutureII      = ['Futur II',                   'Future II'              ][serbPage]
    Imperfect     = ['Imperfekt',                  'Imperfect'              ][serbPage]
    Aorist        = ['Aorist',                     'Aorist'                 ][serbPage]
    CondI         = ['Kondicional I',              'Conditional I'          ][serbPage]
    CondII        = ['Kondicional II',             'Conditional II'         ][serbPage]
    Imperative    = ['Imperativ',                  'Imperative'             ][serbPage]
    PresentAdverb = ['Glagolski prilog sadašnji:', 'Present verbal adverb:' ][serbPage]
    PastAdverb    = ['Glagolski prilog prošli:',   'Past verbal adverb:'    ][serbPage]
    VerbalNoun    = ['Glagolska imenica:',         'Verbal noun:'           ][serbPage]

    SING1 = 0
    SING2 = 1
    SING3 = 2
    PLUR1 = 3
    PLUR2 = 4
    PLUR3 = 5

    PRESENT = 0
    PAST = 1
    POVEL = 2

    MALE = 0
    FEMALE = 1
    NEUTRAL = 2

    o.setTables(serb, rus)
    o.write(serbVerb)

    thirdPresent = serb.get(Cell(Present, SING3))
    if thirdPresent != None and len(thirdPresent) > 1:
        conjugation = PostGarbageFilter(serb.get(Cell(Present, SING3)))[-1]
    else:
        conjugation = 'none'

    o.write('\n{}\n\n'.format(conjugation))

    o.writeLine('inf', rusVerb, serbVerb)
    o.endl()
    
    o.writeDecl('present & sing & first',  Cell('Я', PRESENT), Cell(Present, SING1))
    o.writeDecl('present & sing & second', Cell('Ты', PRESENT), Cell(Present, SING2))
    o.writeDecl('present & sing & third',  Cell('Он', PRESENT), Cell(Present, SING3))
    o.writeDecl('present & plur & first',  Cell('Мы', PRESENT), Cell(Present, PLUR1))
    o.writeDecl('present & plur & second', Cell('Вы', PRESENT), Cell(Present, PLUR2))
    o.writeDecl('present & plur & third',  Cell('Они', PRESENT), Cell(Present, PLUR3))
    o.endl()

    def GetSinglePast(s: str, i: int):
        return s.split()[i]
    
    def SplitParticiple(adjective: str, i: int):
        #print(adjective)
        splitted = adjective.split('/')
        if len(splitted) < 3:
            return ('', '', '')

        m = splitted[0].strip().split()[0]
        f = splitted[1].strip().split()[0]
        n = splitted[2].strip().split()[0]
        
        #print([m, f, n])
        return [m, f, n][i]

    o.writeDecl('perfect & sing & male', Cell('Он', PAST, GetSinglePast, MALE), Cell(Active, 0, SplitParticiple, MALE))
    o.writeDecl('perfect & sing & fem',  Cell('Он', PAST, GetSinglePast, FEMALE), Cell(Active, 0, SplitParticiple, FEMALE))
    o.writeDecl('perfect & sing & neu',  Cell('Он', PAST, GetSinglePast, NEUTRAL), Cell(Active, 0, SplitParticiple, NEUTRAL))
    o.writeDecl('perfect & plur & male', Cell('Они', PAST), Cell(Active, 1, SplitParticiple, MALE))
    o.writeDecl('perfect & plur & fem',  Cell('Они', PAST), Cell(Active, 1, SplitParticiple, FEMALE))
    o.writeDecl('perfect & plur & neu',  Cell('Они', PAST), Cell(Active, 1, SplitParticiple, NEUTRAL))
    o.endl()
    
    def SplitFutur1(futur: str, i: int):
        futur = futur.replace('\n', ' ')
        splitted = futur.split(' ')
        futur_1 = (splitted[0] + ' ' + splitted[1]).strip()
        splitted = splitted[2:]
        futur_2 = ' '.join(splitted).strip()

        #print([futur_1, futur_2])
        return [futur_1, futur_2][i]

    o.writeDecl('futur & sing & first',  None, Cell(FutureI, SING1, SplitFutur1, 1))
    o.writeDecl('futur & sing & second', None, Cell(FutureI, SING2, SplitFutur1, 1))
    o.writeDecl('futur & sing & third',  None, Cell(FutureI, SING3, SplitFutur1, 1))
    o.writeDecl('futur & plur & first',  None, Cell(FutureI, PLUR1, SplitFutur1, 1))
    o.writeDecl('futur & plur & second', None, Cell(FutureI, PLUR2, SplitFutur1, 1))
    o.writeDecl('futur & plur & third',  None, Cell(FutureI, PLUR3, SplitFutur1, 1))
    o.endl()

    o.writeDecl('imperfect & sing & first',  Cell('Он', PAST, GetSinglePast, MALE), Cell(Imperfect, SING1))
    o.writeDecl('imperfect & sing & second', Cell('Он', PAST, GetSinglePast, FEMALE), Cell(Imperfect, SING2))
    o.writeDecl('imperfect & sing & third',  Cell('Он', PAST, GetSinglePast, NEUTRAL), Cell(Imperfect, SING3))
    o.writeDecl('imperfect & plur & first',  Cell('Они', PAST), Cell(Imperfect, PLUR1))
    o.writeDecl('imperfect & plur & second', Cell('Они', PAST), Cell(Imperfect, PLUR2))
    o.writeDecl('imperfect & plur & third',  Cell('Они', PAST), Cell(Imperfect, PLUR3))
    o.endl()

    o.writeLine('# participle & present', None, serb.parseColumnedCell(PresentAdverb))
    o.writeLine('# participle & past', None, serb.parseColumnedCell(PastAdverb))
    o.writeLine('# noun', None, serb.parseColumnedCell(VerbalNoun))
    o.endl()

    o.writeDecl('# futur & sing & first',  None, Cell(FutureI, SING1, SplitFutur1, 0))
    o.writeDecl('# futur & sing & second', None, Cell(FutureI, SING2, SplitFutur1, 0))
    o.writeDecl('# futur & sing & third',  None, Cell(FutureI, SING3, SplitFutur1, 0))
    o.writeDecl('# futur & plur & first',  None, Cell(FutureI, PLUR1, SplitFutur1, 0))
    o.writeDecl('# futur & plur & second', None, Cell(FutureI, PLUR2, SplitFutur1, 0))
    o.writeDecl('# futur & plur & third',  None, Cell(FutureI, PLUR3, SplitFutur1, 0))
    o.endl()

    o.writeDecl('# futur2 & sing & first',  None, Cell(FutureII, SING1))
    o.writeDecl('# futur2 & sing & second', None, Cell(FutureII, SING2))
    o.writeDecl('# futur2 & sing & third',  None, Cell(FutureII, SING3))
    o.writeDecl('# futur2 & plur & first',  None, Cell(FutureII, PLUR1))
    o.writeDecl('# futur2 & plur & second', None, Cell(FutureII, PLUR2))
    o.writeDecl('# futur2 & plur & third',  None, Cell(FutureII, PLUR3))
    o.endl()

    o.writeDecl('# aorist & sing & first',  None, Cell(Aorist, SING1))
    o.writeDecl('# aorist & sing & second', None, Cell(Aorist, SING2))
    o.writeDecl('# aorist & sing & third',  None, Cell(Aorist, SING3))
    o.writeDecl('# aorist & plur & first',  None, Cell(Aorist, PLUR1))
    o.writeDecl('# aorist & plur & second', None, Cell(Aorist, PLUR2))
    o.writeDecl('# aorist & plur & third',  None, Cell(Aorist, PLUR3))
    o.endl()

    o.writeDecl('# cond1 & sing & first',  None, Cell(CondI, SING1))
    o.writeDecl('# cond1 & sing & second', None, Cell(CondI, SING2))
    o.writeDecl('# cond1 & sing & third',  None, Cell(CondI, SING3))
    o.writeDecl('# cond1 & plur & first',  None, Cell(CondI, PLUR1))
    o.writeDecl('# cond1 & plur & second', None, Cell(CondI, PLUR2))
    o.writeDecl('# cond1 & plur & third',  None, Cell(CondI, PLUR3))
    o.endl()

    o.writeDecl('# cond2 & sing & first',  None, Cell(CondII, SING1))
    o.writeDecl('# cond2 & sing & second', None, Cell(CondII, SING2))
    o.writeDecl('# cond2 & sing & third',  None, Cell(CondII, SING3))
    o.writeDecl('# cond2 & plur & first',  None, Cell(CondII, PLUR1))
    o.writeDecl('# cond2 & plur & second', None, Cell(CondII, PLUR2))
    o.writeDecl('# cond2 & plur & third',  None, Cell(CondII, PLUR3))
    o.endl()

    o.writeDecl('# imperativ & sing & first',  Cell('Я', POVEL), Cell(Imperative, SING1))
    o.writeDecl('# imperativ & sing & second', Cell('Ты', POVEL), Cell(Imperative, SING2))
    o.writeDecl('# imperativ & sing & third',  Cell('Он', POVEL), Cell(Imperative, SING3))
    o.writeDecl('# imperativ & plur & first',  Cell('Мы', POVEL), Cell(Imperative, PLUR1))
    o.writeDecl('# imperativ & plur & second', Cell('Вы', POVEL), Cell(Imperative, PLUR2))
    o.writeDecl('# imperativ & plur & third',  Cell('Они', POVEL), Cell(Imperative, PLUR3))
    o.endl()

    o.writeDecl('# passive & sing & male', None, Cell(Passive, 0, SplitParticiple, MALE))
    o.writeDecl('# passive & sing & fem',  None, Cell(Passive, 0, SplitParticiple, FEMALE))
    o.writeDecl('# passive & sing & neu',  None, Cell(Passive, 0, SplitParticiple, NEUTRAL))
    o.writeDecl('# passive & plur & male', None, Cell(Passive, 1, SplitParticiple, MALE))
    o.writeDecl('# passive & plur & fem',  None, Cell(Passive, 1, SplitParticiple, FEMALE))
    o.writeDecl('# passive & plur & neu',  None, Cell(Passive, 1, SplitParticiple, NEUTRAL))
    o.finishWord()

    return DownloadStatus.Ok

def generateVerb(verbPair: tuple[str, str], o: Writer):
    return False

ExecuteMiner('verb', WordsLists.Load('words'), downloadVerb, generateVerb)
