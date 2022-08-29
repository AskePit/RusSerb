import sys
sys.path.insert(0, '../../../')
from code.data_miners.miner_common import *

class VerbDownloader(TableDownloader):
    def loadCustom(self) -> DownloadStatus:
        aspect = 'impf'
        selfness = 'no_se'

        if 'en.' in self.urlBase: # serb page
            aspectSpans = self.soup.find_all('span', {'class': 'gender'})
            for aspectSpan in aspectSpans:
                if aspectSpan != None:
                    abbr = aspectSpan.find_all('abbr')[0]
                    if abbr != None:
                        txt = abbr.get_text()
                        if txt == 'impf' or txt == 'pf':
                            aspect = txt
                    break
            text = self.soup.find_all('div', {'class': 'mw-parser-output'})[0]
            if text != None:
                listElems = text.find_all('li')
                for li in listElems:
                    if 'reflexive' in li.get_text():
                        selfness = 'opt_se'
                        break
        else: # ru page
            ruText = self.soup.find_all('div', {'class': 'mw-parser-output'})[0]
            if ruText != None:
                ps = ruText.find_all('p')
                for p in ps:
                    if 'несовершенный вид' in p.get_text():
                        aspect = 'impf'
                        break
                    elif 'совершенный вид' in p.get_text():
                        aspect = 'pf'
                        break
        
        self.table.aspect = aspect
        self.table.selfness = selfness
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
    Imperfect     = ['Imperfekt',                  'Imperfect'              ][serbPage]
    Aorist        = ['Aorist',                     'Aorist'                 ][serbPage]
    Imperative    = ['Imperativ',                  'Imperative'             ][serbPage]

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

    declination = ''

    thirdPresent = serb.get(Cell(Present, SING3))
    if thirdPresent != None and len(thirdPresent) > 1:
        declination = PostGarbageFilter(serb.get(Cell(Present, SING3)))[-1]

    if len(declination) > 0:
        declination += ' & '
    declination += serb.aspect + ' & ' + serb.selfness
    
    if len(declination) == 0:
        declination = 'none'

    o.write(f'\n{declination}\n\n')

    o.writeLine('inf', copy.copy(rusVerb), copy.copy(serbVerb))
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

    o.writeDecl('futur & sing & first',  None if rus == None else f'буду {rusVerb}' if rus.aspect == 'impf' else Cell('Я', PRESENT), Cell(FutureI, SING1, SplitFutur1, 1))
    o.writeDecl('futur & sing & second', None if rus == None else f'будешь {rusVerb}' if rus.aspect == 'impf' else Cell('Ты', PRESENT), Cell(FutureI, SING2, SplitFutur1, 1))
    o.writeDecl('futur & sing & third',  None if rus == None else f'будет {rusVerb}' if rus.aspect == 'impf' else Cell('Он', PRESENT), Cell(FutureI, SING3, SplitFutur1, 1))
    o.writeDecl('futur & plur & first',  None if rus == None else f'будем {rusVerb}' if rus.aspect == 'impf' else Cell('Мы', PRESENT), Cell(FutureI, PLUR1, SplitFutur1, 1))
    o.writeDecl('futur & plur & second', None if rus == None else f'будете {rusVerb}' if rus.aspect == 'impf' else Cell('Вы', PRESENT), Cell(FutureI, PLUR2, SplitFutur1, 1))
    o.writeDecl('futur & plur & third',  None if rus == None else f'будут {rusVerb}' if rus.aspect == 'impf' else Cell('Они', PRESENT), Cell(FutureI, PLUR3, SplitFutur1, 1))
    o.endl()

    o.writeDecl('imperfect & sing & first & male',  Cell('Он', PAST, GetSinglePast, MALE), Cell(Imperfect, SING1))
    o.writeDecl('imperfect & sing & first & fem',  Cell('Он', PAST, GetSinglePast, FEMALE), Cell(Imperfect, SING1))
    o.writeDecl('imperfect & sing & first & neu',  Cell('Он', PAST, GetSinglePast, NEUTRAL), Cell(Imperfect, SING1))
    o.writeDecl('imperfect & sing & second & male',  Cell('Он', PAST, GetSinglePast, MALE), Cell(Imperfect, SING2))
    o.writeDecl('imperfect & sing & second & fem',  Cell('Он', PAST, GetSinglePast, FEMALE), Cell(Imperfect, SING2))
    o.writeDecl('imperfect & sing & second & neu',  Cell('Он', PAST, GetSinglePast, NEUTRAL), Cell(Imperfect, SING2))
    o.writeDecl('imperfect & sing & third & male',  Cell('Он', PAST, GetSinglePast, MALE), Cell(Imperfect, SING3))
    o.writeDecl('imperfect & sing & third & fem',  Cell('Он', PAST, GetSinglePast, FEMALE), Cell(Imperfect, SING3))
    o.writeDecl('imperfect & sing & third & neu',  Cell('Он', PAST, GetSinglePast, NEUTRAL), Cell(Imperfect, SING3))
    o.writeDecl('imperfect & plur & first',  Cell('Они', PAST), Cell(Imperfect, PLUR1))
    o.writeDecl('imperfect & plur & second', Cell('Они', PAST), Cell(Imperfect, PLUR2))
    o.writeDecl('imperfect & plur & third',  Cell('Они', PAST), Cell(Imperfect, PLUR3))
    o.endl()

    o.writeDecl('aorist & sing & first & male',  Cell('Он', PAST, GetSinglePast, MALE), Cell(Aorist, SING1))
    o.writeDecl('aorist & sing & first & fem',  Cell('Он', PAST, GetSinglePast, FEMALE), Cell(Aorist, SING1))
    o.writeDecl('aorist & sing & first & neu',  Cell('Он', PAST, GetSinglePast, NEUTRAL), Cell(Aorist, SING1))
    o.writeDecl('aorist & sing & second & male',  Cell('Он', PAST, GetSinglePast, MALE), Cell(Aorist, SING2))
    o.writeDecl('aorist & sing & second & fem',  Cell('Он', PAST, GetSinglePast, FEMALE), Cell(Aorist, SING2))
    o.writeDecl('aorist & sing & second & neu',  Cell('Он', PAST, GetSinglePast, NEUTRAL), Cell(Aorist, SING2))
    o.writeDecl('aorist & sing & third & male',  Cell('Он', PAST, GetSinglePast, MALE), Cell(Aorist, SING3))
    o.writeDecl('aorist & sing & third & fem',  Cell('Он', PAST, GetSinglePast, FEMALE), Cell(Aorist, SING3))
    o.writeDecl('aorist & sing & third & neu',  Cell('Он', PAST, GetSinglePast, NEUTRAL), Cell(Aorist, SING3))
    o.writeDecl('aorist & plur & first',  Cell('Они', PAST), Cell(Aorist, PLUR1))
    o.writeDecl('aorist & plur & second', Cell('Они', PAST), Cell(Aorist, PLUR2))
    o.writeDecl('aorist & plur & third',  Cell('Они', PAST), Cell(Aorist, PLUR3))
    o.endl()

    o.writeDecl('imperativ & sing & second', Cell('Ты', POVEL), Cell(Imperative, SING2))
    o.writeDecl('imperativ & plur & first',  None, Cell(Imperative, PLUR1))
    o.writeDecl('imperativ & plur & second', Cell('Вы', POVEL), Cell(Imperative, PLUR2))
    o.endl()

    o.writeDecl('passive & sing & male', None, Cell(Passive, 0, SplitParticiple, MALE))
    o.writeDecl('passive & sing & fem',  None, Cell(Passive, 0, SplitParticiple, FEMALE))
    o.writeDecl('passive & sing & neu',  None, Cell(Passive, 0, SplitParticiple, NEUTRAL))
    o.writeDecl('passive & plur & male', None, Cell(Passive, 1, SplitParticiple, MALE))
    o.writeDecl('passive & plur & fem',  None, Cell(Passive, 1, SplitParticiple, FEMALE))
    o.writeDecl('passive & plur & neu',  None, Cell(Passive, 1, SplitParticiple, NEUTRAL))
    o.finishWord()

    return DownloadStatus.Ok

def generateVerb(verbPair: tuple[str, str], o: Writer):
    return False

ExecuteMiner('verb', WordsLists.Load('words'), downloadVerb, generateVerb)
