import sys
sys.path.insert(0, '../../../')
from code.data_miners.miner_common import *

class NounDownloader(TableDownloader):
    def loadCustom(self) -> DownloadStatus:
        gender = None

        if 'sh.' in self.urlBase or 'en.' in self.urlBase: # serb page
            genderSpans = self.soup.find_all('span', {'class': 'gender'})
            for genderSpan in genderSpans:
                if genderSpan != None:
                    abbr = genderSpan.find_all('abbr')[0]
                    if abbr != None:
                        txt = abbr.get_text()
                        if txt == 'm':
                            gender = 'male'
                        elif txt == 'f':
                            gender = 'fem'
                        elif txt == 'n':
                            gender = 'neu'
                    break
        else: # ru page
            ruText = self.soup.find_all('div', {'class': 'mw-parser-output'})[0]
            if ruText != None:
                ps = ruText.find_all('p')
                for p in ps:
                    if 'мужской род' in p.get_text():
                        gender = 'ru_male'
                        break
                    elif 'женский род' in p.get_text():
                        gender = 'ru_fem'
                        break
                    elif 'средний род' in p.get_text():
                        gender = 'ru_neu'
                        break
        
        self.table.gender = gender
        return DownloadStatus.Ok

def downloadNoun(nounPair: tuple[str, str], o: Writer) -> DownloadStatus:
    print(nounPair)

    serbNoun, rusNoun = nounPair

    SH = 0
    EN = 1

    serbPage = EN

    serbOk, serb = NounDownloader(serbNoun, 'https://en.wiktionary.org/wiki', 'Serbo-Croatian', 'table', 'inflection-table')()
    rusOk, rus   = NounDownloader(rusNoun, 'https://ru.wiktionary.org/wiki', None, 'table', 'morfotable ru')()

    if serbOk != DownloadStatus.Ok:
        # try to fallback to `sh` version
        serbOk, serb = NounDownloader(serbNoun, 'https://sh.wiktionary.org/wiki', 'Srpskohrvatski', 'table', 'inflection-table')()
        serbPage = SH

    print(serbOk)
    if serbOk != DownloadStatus.Ok:
        return serbOk

    Nominative   = ['nominativ',    'nominative'  ][serbPage]
    Genitive     = ['genitiv',      'genitive'    ][serbPage]
    Dative       = ['dativ',        'dative'      ][serbPage]
    Accusative   = ['akuzativ',     'accusative'  ][serbPage]
    Vocative     = ['vokativ',      'vocative'    ][serbPage]
    Instrumental = ['instrumental', 'instrumental'][serbPage]
    Locative     = ['lokativ',      'locative'    ][serbPage]

    o.setTables(serb, rus)
    o.write(serbNoun)
    o.endl()
    if serb != None and serb.gender != None and rus != None and rus.gender != None:
        o.write(f'{serb.gender} & {rus.gender}')
    elif serb != None and serb.gender != None:
        o.write(serb.gender)
    elif rus != None and rus.gender != None:
        o.write(rus.gender)
    else:
        o.write('none')
    o.endl()
    o.endl()
    
    SING = 0
    PLUR = 1

    o.writeDecl('sing & nom',  Cell('Им.', SING), Cell(Nominative, SING))
    o.writeDecl('sing & gen',  Cell('Р.', SING),  Cell(Genitive, SING))
    o.writeDecl('sing & dat',  Cell('Д.', SING),  Cell(Dative, SING))
    o.writeDecl('sing & aku',  Cell('В.', SING),  Cell(Accusative, SING))
    o.writeDecl('sing & vok',  Cell('Им.', SING), Cell(Vocative, SING))
    o.writeDecl('sing & inst', Cell('Тв.', SING), Cell(Instrumental, SING))
    o.writeDecl('sing & lok',  Cell('Пр.', SING), Cell(Locative, SING))
    o.endl()

    o.writeDecl('plur & nom',  Cell('Им.', PLUR), Cell(Nominative, PLUR))
    o.writeDecl('plur & gen',  Cell('Р.', PLUR),  Cell(Genitive, PLUR))
    o.writeDecl('plur & dat',  Cell('Д.', PLUR),  Cell(Dative, PLUR))
    o.writeDecl('plur & aku',  Cell('В.', PLUR),  Cell(Accusative, PLUR))
    o.writeDecl('plur & vok',  Cell('Им.', PLUR), Cell(Vocative, PLUR))
    o.writeDecl('plur & inst', Cell('Тв.', PLUR), Cell(Instrumental, PLUR))
    o.writeDecl('plur & lok',  Cell('Пр.', PLUR), Cell(Locative, PLUR))
    o.finishWord()

    return DownloadStatus.Ok

def generateNoun(nounPair: tuple[str, str], o: Writer):
    return False

ExecuteMiner('noun', WordsLists.Load('words'), downloadNoun, generateNoun)
