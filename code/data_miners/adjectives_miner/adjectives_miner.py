import sys
sys.path.insert(0, '../../../')
from code.data_miners.miner_common import *

class AdjectiveDownloader(TableDownloader):
    def loadCustom(self) -> DownloadStatus:
        better = None

        if 'ru.' in self.urlBase:
            texts = self.soup.find_all('p')
            for p in texts:
                if p != None:
                    txt: str = p.get_text()
                    seekText = "Сравнительная степень"
                    if seekText in txt:
                        # Сравнительная степень — добре́е, добре́й, подобре́е, подобре́й.

                        #  — добре́е, добре́й, подобре́е, подобре́й.
                        txt = txt[txt.find(seekText) + len(seekText) : ]

                        # добре́е, добре́й, подобре́е, подобре́й.
                        txt = txt[ txt.find(next(filter(str.isalpha, txt))) : ]

                        # добре́е
                        txt = txt[: txt.find(next(filter(lambda s: s == ',' or s == '.', txt)))]

                        better = PreGarbageFilter(txt)
                        break
        
        if better == None:
            # 2 - is female
            self.table.better = self.table.get(Cell('Кратк.', 2))
            if len(self.table.better) > 1:
                self.table.better = self.table.better[:-1] + 'ее'
        else:
            self.table.better = better
        
        return DownloadStatus.Ok

def downloadAdjective(adjectivePair: tuple[str, str], o: Writer) -> DownloadStatus:
    print(adjectivePair)

    serbAdjective, rusAdjective = adjectivePair

    SH = 0
    EN = 1

    serbPage = EN

    serbTables = [None, None, None, None]

    i = 0
    for table in serbTables:
        serbOk, table = AdjectiveDownloader(serbAdjective, 'https://en.wiktionary.org/wiki', 'Serbo-Croatian', 'table', 'inflection-table', i)()
        serbTables[i] = table
        i += 1

    rusOk, rus   = AdjectiveDownloader(rusAdjective, 'https://ru.wiktionary.org/wiki', None, 'table', 'morfotable ru')()

    if serbOk != DownloadStatus.Ok:
        # try to fallback to `sh` version
        i = 0
        for table in serbTables:
            serbOk, table = AdjectiveDownloader(serbAdjective, 'https://sh.wiktionary.org/wiki', 'Srpskohrvatski', 'div', 'NavContent', i)()
            serbTables[i] = table
            i += 1
        serbPage = SH

    serbIndef = serbTables[0]
    serbDef = serbTables[1]
    serbComp = serbTables[2]
    serbSuper = serbTables[3]

    print(serbOk)
    if serbOk != DownloadStatus.Ok:
        return serbOk

    Nominative   = ['nominativ',    'nominative'  ][serbPage]
    Genitive     = ['genitiv',      'genitive'    ][serbPage]
    Dative       = ['dativ',        'dative'      ][serbPage]
    Accusative   = ['akuzativ',     'accusative'  ][serbPage]
    Vocative     = ['vokativ',      'vocative'    ][serbPage]
    Locative     = ['lokativ',      'locative'    ][serbPage]
    Instrumental = ['instrumental', 'instrumental'][serbPage]

    SERB_MALE = 0
    SERB_FEM = 1
    SERB_NEU = 2

    RUS_MALE = 0
    RUS_FEM = 2
    RUS_NEU = 1
    RUS_PLUR = 3

    o.write(serbAdjective)
    o.write('\nnone\n\n')

    o.writeLine('inf', rusAdjective, serbAdjective)
    o.endl()

    def getAnimated(s: str, i: int):
        return s.split()[i]
    
    rusSuperBase = ''
    if rus != None:
        rusSuperBase = rus.get(Cell('Кратк.', RUS_FEM))
        if len(rusSuperBase) > 1:
            rusSuperBase = rusSuperBase[:-1]
    
    rusBetter = ''
    if rus != None:
        rusBetter = rus.better

    NOM = 0
    GEN = 1
    DAT = 2
    AKU = 3
    INST = 4
    LOK = 5

    superSuffixes = [
        ['ейший', 'ейшая', 'ейшее', 'ейшие'],
        ['ейшего', 'ейшей', 'ейшего', 'ейших'],
        ['ейшему', 'ейшей', 'ейшему', 'ейшим'],
        ['ейшего', 'ейшую', 'ейшего', 'ейших'],
        ['ейшим', 'ейшей', 'ейшим', 'ейшими'],
        ['ейшем', 'ейшей', 'ейшем', 'ейших'],
    ]

    def makeRusSuper(case: int, gender: int) -> str:
        return 'наи' + rusSuperBase + superSuffixes[case][gender]
    
    o.setTables(serbIndef, rus)
    o.writeDecl('sing & nom & male & indef', Cell('Кратк.', RUS_MALE), Cell(Nominative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & nom & fem  & indef', Cell('Кратк.', RUS_FEM),  Cell(Nominative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & nom & neu  & indef', Cell('Кратк.', RUS_NEU),  Cell(Nominative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & nom & male & indef', Cell('Кратк.', RUS_PLUR), Cell(Nominative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & nom & fem  & indef', Cell('Кратк.', RUS_PLUR), Cell(Nominative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & nom & neu  & indef', Cell('Кратк.', RUS_PLUR), Cell(Nominative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & gen & male & indef', Cell('Р.', RUS_MALE), Cell(Genitive, SERB_MALE, rowNum=0))
    o.writeDecl('sing & gen & fem  & indef', Cell('Р.', RUS_FEM),  Cell(Genitive, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & gen & neu  & indef', Cell('Р.', RUS_NEU),  Cell(Genitive, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & gen & male & indef', Cell('Р.', RUS_PLUR), Cell(Genitive, SERB_MALE, rowNum=1))
    o.writeDecl('plur & gen & fem  & indef', Cell('Р.', RUS_PLUR), Cell(Genitive, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & gen & neu  & indef', Cell('Р.', RUS_PLUR), Cell(Genitive, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & dat & male & indef', Cell('Д.', RUS_MALE), Cell(Dative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & dat & fem  & indef', Cell('Д.', RUS_FEM),  Cell(Dative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & dat & neu  & indef', Cell('Д.', RUS_NEU),  Cell(Dative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & dat & male & indef', Cell('Д.', RUS_PLUR), Cell(Dative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & dat & fem  & indef', Cell('Д.', RUS_PLUR), Cell(Dative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & dat & neu  & indef', Cell('Д.', RUS_PLUR), Cell(Dative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & aku & male & indef & anim', Cell('одуш.', RUS_MALE), Cell(Accusative, SERB_MALE+1, getAnimated, 1, rowNum=0))
    o.writeDecl('sing & aku & fem  & indef & anim', Cell('одуш.', RUS_FEM),  Cell(Accusative, SERB_FEM+1,  rowNum=0))
    o.writeDecl('sing & aku & neu  & indef & anim', Cell('одуш.', RUS_NEU),  Cell(Accusative, SERB_NEU+1,  rowNum=0))
    o.writeDecl('plur & aku & male & indef & anim', Cell('одуш.', RUS_PLUR), Cell(Accusative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & aku & fem  & indef & anim', Cell('одуш.', RUS_PLUR), Cell(Accusative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & aku & neu  & indef & anim', Cell('одуш.', RUS_PLUR), Cell(Accusative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & aku & male & indef & inanim', Cell('неод.', RUS_MALE), Cell(Accusative, SERB_MALE+1, getAnimated, 0, rowNum=0))
    o.writeDecl('sing & aku & fem  & indef & inanim', Cell('одуш.', RUS_FEM),  Cell(Accusative, SERB_FEM+1,  rowNum=0))
    o.writeDecl('sing & aku & neu  & indef & inanim', Cell('одуш.', RUS_NEU),  Cell(Accusative, SERB_NEU+1,  rowNum=0))
    o.writeDecl('plur & aku & male & indef & inanim', Cell('неод.', RUS_PLUR), Cell(Accusative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & aku & fem  & indef & inanim', Cell('неод.', RUS_PLUR), Cell(Accusative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & aku & neu  & indef & inanim', Cell('неод.', RUS_PLUR), Cell(Accusative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & vok & male & indef', Cell('Кратк.', RUS_MALE), Cell(Vocative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & vok & fem  & indef', Cell('Кратк.', RUS_FEM),  Cell(Vocative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & vok & neu  & indef', Cell('Кратк.', RUS_NEU),  Cell(Vocative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & vok & male & indef', Cell('Кратк.', RUS_PLUR), Cell(Vocative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & vok & fem  & indef', Cell('Кратк.', RUS_PLUR), Cell(Vocative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & vok & neu  & indef', Cell('Кратк.', RUS_PLUR), Cell(Vocative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & lok & male & indef', Cell('П.', RUS_MALE), Cell(Locative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & lok & fem  & indef', Cell('П.', RUS_FEM),  Cell(Locative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & lok & neu  & indef', Cell('П.', RUS_NEU),  Cell(Locative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & lok & male & indef', Cell('П.', RUS_PLUR), Cell(Locative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & lok & fem  & indef', Cell('П.', RUS_PLUR), Cell(Locative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & lok & neu  & indef', Cell('П.', RUS_PLUR), Cell(Locative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & inst & male & indef', Cell('Т.', RUS_MALE), Cell(Instrumental, SERB_MALE, rowNum=0))
    o.writeDecl('sing & inst & fem  & indef', Cell('Т.', RUS_FEM),  Cell(Instrumental, SERB_FEM, rowNum=0))
    o.writeDecl('sing & inst & neu  & indef', Cell('Т.', RUS_NEU),  Cell(Instrumental, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & inst & male & indef', Cell('Т.', RUS_PLUR), Cell(Instrumental, SERB_MALE, rowNum=1))
    o.writeDecl('plur & inst & fem  & indef', Cell('Т.', RUS_PLUR), Cell(Instrumental, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & inst & neu  & indef', Cell('Т.', RUS_PLUR), Cell(Instrumental, SERB_NEU,  rowNum=1))
    o.endl()

    o.setTables(serbDef, rus)
    o.writeDecl('sing & nom & male & defined', Cell('Им.', RUS_MALE), Cell(Nominative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & nom & fem  & defined', Cell('Им.', RUS_FEM),  Cell(Nominative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & nom & neu  & defined', Cell('Им.', RUS_NEU),  Cell(Nominative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & nom & male & defined', Cell('Им.', RUS_PLUR), Cell(Nominative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & nom & fem  & defined', Cell('Им.', RUS_PLUR), Cell(Nominative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & nom & neu  & defined', Cell('Им.', RUS_PLUR), Cell(Nominative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & gen & male & defined', Cell('Р.', RUS_MALE), Cell(Genitive, SERB_MALE, rowNum=0))
    o.writeDecl('sing & gen & fem  & defined', Cell('Р.', RUS_FEM),  Cell(Genitive, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & gen & neu  & defined', Cell('Р.', RUS_NEU),  Cell(Genitive, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & gen & male & defined', Cell('Р.', RUS_PLUR), Cell(Genitive, SERB_MALE, rowNum=1))
    o.writeDecl('plur & gen & fem  & defined', Cell('Р.', RUS_PLUR), Cell(Genitive, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & gen & neu  & defined', Cell('Р.', RUS_PLUR), Cell(Genitive, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & dat & male & defined', Cell('Д.', RUS_MALE), Cell(Dative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & dat & fem  & defined', Cell('Д.', RUS_FEM),  Cell(Dative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & dat & neu  & defined', Cell('Д.', RUS_NEU),  Cell(Dative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & dat & male & defined', Cell('Д.', RUS_PLUR), Cell(Dative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & dat & fem  & defined', Cell('Д.', RUS_PLUR), Cell(Dative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & dat & neu  & defined', Cell('Д.', RUS_PLUR), Cell(Dative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & aku & male & defined & anim', Cell('одуш.', RUS_MALE), Cell(Accusative, SERB_MALE+1, getAnimated, 1, rowNum=0))
    o.writeDecl('sing & aku & fem  & defined & anim', Cell('одуш.', RUS_FEM),  Cell(Accusative, SERB_FEM+1,  rowNum=0))
    o.writeDecl('sing & aku & neu  & defined & anim', Cell('одуш.', RUS_NEU),  Cell(Accusative, SERB_NEU+1,  rowNum=0))
    o.writeDecl('plur & aku & male & defined & anim', Cell('одуш.', RUS_PLUR), Cell(Accusative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & aku & fem  & defined & anim', Cell('одуш.', RUS_PLUR), Cell(Accusative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & aku & neu  & defined & anim', Cell('одуш.', RUS_PLUR), Cell(Accusative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & aku & male & defined & inanim', Cell('неод.', RUS_MALE), Cell(Accusative, SERB_MALE+1, getAnimated, 0, rowNum=0))
    o.writeDecl('sing & aku & fem  & defined & inanim', Cell('одуш.', RUS_FEM),  Cell(Accusative, SERB_FEM+1,  rowNum=0))
    o.writeDecl('sing & aku & neu  & defined & inanim', Cell('одуш.', RUS_NEU),  Cell(Accusative, SERB_NEU+1,  rowNum=0))
    o.writeDecl('plur & aku & male & defined & inanim', Cell('неод.', RUS_PLUR), Cell(Accusative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & aku & fem  & defined & inanim', Cell('неод.', RUS_PLUR), Cell(Accusative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & aku & neu  & defined & inanim', Cell('неод.', RUS_PLUR), Cell(Accusative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & vok & male & defined', Cell('Им.', RUS_MALE), Cell(Vocative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & vok & fem  & defined', Cell('Им.', RUS_FEM),  Cell(Vocative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & vok & neu  & defined', Cell('Им.', RUS_NEU),  Cell(Vocative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & vok & male & defined', Cell('Им.', RUS_PLUR), Cell(Vocative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & vok & fem  & defined', Cell('Им.', RUS_PLUR), Cell(Vocative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & vok & neu  & defined', Cell('Им.', RUS_PLUR), Cell(Vocative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & lok & male & defined', Cell('П.', RUS_MALE), Cell(Locative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & lok & fem  & defined', Cell('П.', RUS_FEM),  Cell(Locative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & lok & neu  & defined', Cell('П.', RUS_NEU),  Cell(Locative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & lok & male & defined', Cell('П.', RUS_PLUR), Cell(Locative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & lok & fem  & defined', Cell('П.', RUS_PLUR), Cell(Locative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & lok & neu  & defined', Cell('П.', RUS_PLUR), Cell(Locative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & inst & male & defined', Cell('Т.', RUS_MALE), Cell(Instrumental, SERB_MALE, rowNum=0))
    o.writeDecl('sing & inst & fem  & defined', Cell('Т.', RUS_FEM),  Cell(Instrumental, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & inst & neu  & defined', Cell('Т.', RUS_NEU),  Cell(Instrumental, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & inst & male & defined', Cell('Т.', RUS_PLUR), Cell(Instrumental, SERB_MALE, rowNum=1))
    o.writeDecl('plur & inst & fem  & defined', Cell('Т.', RUS_PLUR), Cell(Instrumental, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & inst & neu  & defined', Cell('Т.', RUS_PLUR), Cell(Instrumental, SERB_NEU,  rowNum=1))
    o.endl()

    o.setTables(serbComp, rus)
    o.writeDecl('sing & nom & male & comp', rusBetter, Cell(Nominative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & nom & fem  & comp', rusBetter, Cell(Nominative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & nom & neu  & comp', rusBetter, Cell(Nominative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & nom & male & comp', rusBetter, Cell(Nominative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & nom & fem  & comp', rusBetter, Cell(Nominative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & nom & neu  & comp', rusBetter, Cell(Nominative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & gen & male & comp', rusBetter, Cell(Genitive, SERB_MALE, rowNum=0))
    o.writeDecl('sing & gen & fem  & comp', rusBetter, Cell(Genitive, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & gen & neu  & comp', rusBetter, Cell(Genitive, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & gen & male & comp', rusBetter, Cell(Genitive, SERB_MALE, rowNum=1))
    o.writeDecl('plur & gen & fem  & comp', rusBetter, Cell(Genitive, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & gen & neu  & comp', rusBetter, Cell(Genitive, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & dat & male & comp', rusBetter, Cell(Dative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & dat & fem  & comp', rusBetter, Cell(Dative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & dat & neu  & comp', rusBetter, Cell(Dative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & dat & male & comp', rusBetter, Cell(Dative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & dat & fem  & comp', rusBetter, Cell(Dative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & dat & neu  & comp', rusBetter, Cell(Dative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & aku & male & comp & anim', rusBetter, Cell(Accusative, SERB_MALE+1, getAnimated, 1, rowNum=0))
    o.writeDecl('sing & aku & fem  & comp & anim', rusBetter, Cell(Accusative, SERB_FEM+1,  rowNum=0))
    o.writeDecl('sing & aku & neu  & comp & anim', rusBetter, Cell(Accusative, SERB_NEU+1,  rowNum=0))
    o.writeDecl('plur & aku & male & comp & anim', rusBetter, Cell(Accusative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & aku & fem  & comp & anim', rusBetter, Cell(Accusative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & aku & neu  & comp & anim', rusBetter, Cell(Accusative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & aku & male & comp & inanim', rusBetter, Cell(Accusative, SERB_MALE+1, getAnimated, 0, rowNum=0))
    o.writeDecl('sing & aku & fem  & comp & inanim', rusBetter, Cell(Accusative, SERB_FEM+1,  rowNum=0))
    o.writeDecl('sing & aku & neu  & comp & inanim', rusBetter, Cell(Accusative, SERB_NEU+1,  rowNum=0))
    o.writeDecl('plur & aku & male & comp & inanim', rusBetter, Cell(Accusative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & aku & fem  & comp & inanim', rusBetter, Cell(Accusative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & aku & neu  & comp & inanim', rusBetter, Cell(Accusative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & vok & male & comp', rusBetter, Cell(Vocative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & vok & fem  & comp', rusBetter, Cell(Vocative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & vok & neu  & comp', rusBetter, Cell(Vocative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & vok & male & comp', rusBetter, Cell(Vocative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & vok & fem  & comp', rusBetter, Cell(Vocative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & vok & neu  & comp', rusBetter, Cell(Vocative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & lok & male & comp', rusBetter, Cell(Locative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & lok & fem  & comp', rusBetter, Cell(Locative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & lok & neu  & comp', rusBetter, Cell(Locative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & lok & male & comp', rusBetter, Cell(Locative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & lok & fem  & comp', rusBetter, Cell(Locative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & lok & neu  & comp', rusBetter, Cell(Locative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & inst & male & comp', rusBetter, Cell(Instrumental, SERB_MALE, rowNum=0))
    o.writeDecl('sing & inst & fem  & comp', rusBetter, Cell(Instrumental, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & inst & neu  & comp', rusBetter, Cell(Instrumental, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & inst & male & comp', rusBetter, Cell(Instrumental, SERB_MALE, rowNum=1))
    o.writeDecl('plur & inst & fem  & comp', rusBetter, Cell(Instrumental, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & inst & neu  & comp', rusBetter, Cell(Instrumental, SERB_NEU,  rowNum=1))
    o.endl()

    o.setTables(serbSuper, rus)
    o.writeDecl('sing & nom & male & super', makeRusSuper(NOM, RUS_MALE), Cell(Nominative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & nom & fem  & super', makeRusSuper(NOM, RUS_FEM),  Cell(Nominative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & nom & neu  & super', makeRusSuper(NOM, RUS_NEU),  Cell(Nominative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & nom & male & super', makeRusSuper(NOM, RUS_PLUR), Cell(Nominative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & nom & fem  & super', makeRusSuper(NOM, RUS_PLUR), Cell(Nominative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & nom & neu  & super', makeRusSuper(NOM, RUS_PLUR), Cell(Nominative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & gen & male & super', makeRusSuper(GEN, RUS_MALE), Cell(Genitive, SERB_MALE, rowNum=0))
    o.writeDecl('sing & gen & fem  & super', makeRusSuper(GEN, RUS_FEM),  Cell(Genitive, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & gen & neu  & super', makeRusSuper(GEN, RUS_NEU),  Cell(Genitive, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & gen & male & super', makeRusSuper(GEN, RUS_PLUR), Cell(Genitive, SERB_MALE, rowNum=1))
    o.writeDecl('plur & gen & fem  & super', makeRusSuper(GEN, RUS_PLUR), Cell(Genitive, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & gen & neu  & super', makeRusSuper(GEN, RUS_PLUR), Cell(Genitive, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & dat & male & super', makeRusSuper(DAT, RUS_MALE), Cell(Dative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & dat & fem  & super', makeRusSuper(DAT, RUS_FEM),  Cell(Dative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & dat & neu  & super', makeRusSuper(DAT, RUS_NEU),  Cell(Dative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & dat & male & super', makeRusSuper(DAT, RUS_PLUR), Cell(Dative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & dat & fem  & super', makeRusSuper(DAT, RUS_PLUR), Cell(Dative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & dat & neu  & super', makeRusSuper(DAT, RUS_PLUR), Cell(Dative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & aku & male & super & anim', makeRusSuper(AKU, RUS_MALE), Cell(Accusative, SERB_MALE+1, getAnimated, 1, rowNum=0))
    o.writeDecl('sing & aku & fem  & super & anim', makeRusSuper(AKU, RUS_FEM),  Cell(Accusative, SERB_FEM+1,  rowNum=0))
    o.writeDecl('sing & aku & neu  & super & anim', makeRusSuper(AKU, RUS_NEU),  Cell(Accusative, SERB_NEU+1,  rowNum=0))
    o.writeDecl('plur & aku & male & super & anim', makeRusSuper(AKU, RUS_PLUR), Cell(Accusative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & aku & fem  & super & anim', makeRusSuper(AKU, RUS_PLUR), Cell(Accusative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & aku & neu  & super & anim', makeRusSuper(AKU, RUS_PLUR), Cell(Accusative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & aku & male & super & inanim', makeRusSuper(NOM, RUS_MALE), Cell(Accusative, SERB_MALE+1, getAnimated, 0, rowNum=0))
    o.writeDecl('sing & aku & fem  & super & inanim', makeRusSuper(AKU, RUS_FEM),  Cell(Accusative, SERB_FEM+1,  rowNum=0))
    o.writeDecl('sing & aku & neu  & super & inanim', makeRusSuper(NOM, RUS_NEU),  Cell(Accusative, SERB_NEU+1,  rowNum=0))
    o.writeDecl('plur & aku & male & super & inanim', makeRusSuper(AKU, RUS_PLUR), Cell(Accusative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & aku & fem  & super & inanim', makeRusSuper(AKU, RUS_PLUR), Cell(Accusative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & aku & neu  & super & inanim', makeRusSuper(AKU, RUS_PLUR), Cell(Accusative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & vok & male & super', makeRusSuper(NOM, RUS_MALE), Cell(Vocative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & vok & fem  & super', makeRusSuper(NOM, RUS_FEM),  Cell(Vocative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & vok & neu  & super', makeRusSuper(NOM, RUS_NEU),  Cell(Vocative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & vok & male & super', makeRusSuper(NOM, RUS_PLUR), Cell(Vocative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & vok & fem  & super', makeRusSuper(NOM, RUS_PLUR), Cell(Vocative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & vok & neu  & super', makeRusSuper(NOM, RUS_PLUR), Cell(Vocative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & lok & male & super', makeRusSuper(LOK, RUS_MALE), Cell(Locative, SERB_MALE, rowNum=0))
    o.writeDecl('sing & lok & fem  & super', makeRusSuper(LOK, RUS_FEM),  Cell(Locative, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & lok & neu  & super', makeRusSuper(LOK, RUS_NEU),  Cell(Locative, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & lok & male & super', makeRusSuper(LOK, RUS_PLUR), Cell(Locative, SERB_MALE, rowNum=1))
    o.writeDecl('plur & lok & fem  & super', makeRusSuper(LOK, RUS_PLUR), Cell(Locative, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & lok & neu  & super', makeRusSuper(LOK, RUS_PLUR), Cell(Locative, SERB_NEU,  rowNum=1))
    o.endl()

    o.writeDecl('sing & inst & male & super', makeRusSuper(INST, RUS_MALE), Cell(Instrumental, SERB_MALE, rowNum=0))
    o.writeDecl('sing & inst & fem  & super', makeRusSuper(INST, RUS_FEM),  Cell(Instrumental, SERB_FEM,  rowNum=0))
    o.writeDecl('sing & inst & neu  & super', makeRusSuper(INST, RUS_NEU),  Cell(Instrumental, SERB_NEU,  rowNum=0))
    o.writeDecl('plur & inst & male & super', makeRusSuper(INST, RUS_PLUR), Cell(Instrumental, SERB_MALE, rowNum=1))
    o.writeDecl('plur & inst & fem  & super', makeRusSuper(INST, RUS_PLUR), Cell(Instrumental, SERB_FEM,  rowNum=1))
    o.writeDecl('plur & inst & neu  & super', makeRusSuper(INST, RUS_PLUR), Cell(Instrumental, SERB_NEU,  rowNum=1))
    o.finishWord()

    return DownloadStatus.Ok

def generateAdjective(adjectivePair: tuple[str, str], o: Writer):
    return False

ExecuteMiner('adjective', WordsLists.Load('words'), downloadAdjective, generateAdjective)
