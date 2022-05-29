import os
import sys
sys.path.insert(0, '../../../')
from code.data_miners.miner_common import *

class NounDownloader(TableDownloader):
    def loadCustom(self) -> DownloadStatus:
        gender = None

        if 'sh.' in self.urlBase: # serb page
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

    serbOk, serb = NounDownloader(serbNoun, 'https://sh.wiktionary.org/wiki', 'table', 'inflection-table')()
    rusOk, rus   = NounDownloader(rusNoun, 'https://ru.wiktionary.org/wiki', 'table', 'morfotable ru')()

    if serbOk != DownloadStatus.Ok:
        return serbOk

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

    o.writeDecl('sing & nom',  Cell('Им.', Sing), Cell('nominativ', Sing))
    o.writeDecl('sing & gen',  Cell('Р.', Sing),  Cell('genitiv', Sing))
    o.writeDecl('sing & dat',  Cell('Д.', Sing),  Cell('dativ', Sing))
    o.writeDecl('sing & aku',  Cell('В.', Sing),  Cell('akuzativ', Sing))
    o.writeDecl('sing & vok',  Cell('Им.', Sing), Cell('vokativ', Sing))
    o.writeDecl('sing & inst', Cell('Тв.', Sing), Cell('instrumental', Sing))
    o.writeDecl('sing & lok',  Cell('Пр.', Sing), Cell('lokativ', Sing))
    o.endl()

    o.writeDecl('plur & nom',  Cell('Им.', Plur), Cell('nominativ', Plur))
    o.writeDecl('plur & gen',  Cell('Р.', Plur),  Cell('genitiv', Plur))
    o.writeDecl('plur & dat',  Cell('Д.', Plur),  Cell('dativ', Plur))
    o.writeDecl('plur & aku',  Cell('В.', Plur),  Cell('akuzativ', Plur))
    o.writeDecl('plur & vok',  Cell('Им.', Plur), Cell('vokativ', Plur))
    o.writeDecl('plur & inst', Cell('Тв.', Plur), Cell('instrumental', Plur))
    o.writeDecl('plur & lok',  Cell('Пр.', Plur), Cell('lokativ', Plur))
    o.finishWord()

    return DownloadStatus.Ok

def generateNoun(nounPair: tuple[str, str], o: Writer):
    return False

ExecuteMiner('noun', WordsLists.Load('words'), downloadNoun, generateNoun)
