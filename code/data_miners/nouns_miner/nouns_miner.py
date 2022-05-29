import os
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

    serbTableMode = EN

    serbOk, serb = NounDownloader(serbNoun, 'https://en.wiktionary.org/wiki', 'Serbo-Croatian', 'table', 'inflection-table')()
    rusOk, rus   = NounDownloader(rusNoun, 'https://ru.wiktionary.org/wiki', None, 'table', 'morfotable ru')()

    if serbOk != DownloadStatus.Ok:
        # try to fallback to `sh` version
        serbOk, serb = NounDownloader(serbNoun, 'https://sh.wiktionary.org/wiki', 'Srpskohrvatski', 'table', 'inflection-table')()
        serbTableMode = SH

    print(serbOk)
    if serbOk != DownloadStatus.Ok:
        return serbOk

    Nominative   = ['nominativ',    'nominative'  ][serbTableMode]
    Genitive     = ['genitiv',      'genitive'    ][serbTableMode]
    Dative       = ['dativ',        'dative'      ][serbTableMode]
    Accusative   = ['akuzativ',     'accusative'  ][serbTableMode]
    Vocative     = ['vokativ',      'vocative'    ][serbTableMode]
    Instrumental = ['instrumental', 'instrumental'][serbTableMode]
    Locative     = ['lokativ',      'locative'    ][serbTableMode]

    o.setTables(serb, rus)
    o.write(serbNoun)
    o.endl()
    if serb != None and serb.gender != None and rus != None and rus.gender != None:
        o.write('{} & {}'.format(serb.gender, rus.gender))
    elif serb != None and serb.gender != None:
        o.write(serb.gender)
    elif rus != None and rus.gender != None:
        o.write(rus.gender)
    else:
        o.write('none')
    o.endl()
    o.endl()
    
    Sing = 0
    Plur = 1

    o.writeDecl('sing & nom',  Cell('Им.', Sing), Cell(Nominative, Sing))
    o.writeDecl('sing & gen',  Cell('Р.', Sing),  Cell(Genitive, Sing))
    o.writeDecl('sing & dat',  Cell('Д.', Sing),  Cell(Dative, Sing))
    o.writeDecl('sing & aku',  Cell('В.', Sing),  Cell(Accusative, Sing))
    o.writeDecl('sing & vok',  Cell('Им.', Sing), Cell(Vocative, Sing))
    o.writeDecl('sing & inst', Cell('Тв.', Sing), Cell(Instrumental, Sing))
    o.writeDecl('sing & lok',  Cell('Пр.', Sing), Cell(Locative, Sing))
    o.endl()

    o.writeDecl('plur & nom',  Cell('Им.', Plur), Cell(Nominative, Plur))
    o.writeDecl('plur & gen',  Cell('Р.', Plur),  Cell(Genitive, Plur))
    o.writeDecl('plur & dat',  Cell('Д.', Plur),  Cell(Dative, Plur))
    o.writeDecl('plur & aku',  Cell('В.', Plur),  Cell(Accusative, Plur))
    o.writeDecl('plur & vok',  Cell('Им.', Plur), Cell(Vocative, Plur))
    o.writeDecl('plur & inst', Cell('Тв.', Plur), Cell(Instrumental, Plur))
    o.writeDecl('plur & lok',  Cell('Пр.', Plur), Cell(Locative, Plur))
    o.finishWord()

    return DownloadStatus.Ok

def generateNoun(nounPair: tuple[str, str], o: Writer):
    return False

ExecuteMiner('noun', WordsLists.Load('words'), downloadNoun, generateNoun)
