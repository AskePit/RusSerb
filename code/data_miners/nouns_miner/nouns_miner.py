from enum import Enum
from urllib.request import urlopen
from urllib import parse
import io
import sys
from bs4 import BeautifulSoup

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

nouns = [
    ('muzej', 'музей'),
    ('mačka', 'кошка'),
    ('pas', 'пёс'),
    ('jaje', 'яйцо'),
    ('grožđa', 'виноград'),
    ('jabuka', 'яблоко'),
    ('maline', 'малина'),
    ('jagode', 'клубника'),
    ('breskve', 'персики'),
    ('narandža', 'апельсин'),
    ('nar', 'гранат'),
    ('šljiva', 'слива'),
    ('dinja', 'дыня'),
    ('lubenica', 'арбуз'),
    ('kajsija', 'абрикос'),
    ('borovnice', 'черника'),
    ('kupine', 'ежевика'),
    ('japanska jabuka', 'хурма'),
    ('smokva', 'инжир'),
    ('dud', 'шелковица'),
    ('murva', 'шелковица'),
    ('trešnje', 'черешня'),
    ('limun', 'лимон'),
    ('limeta', 'лайм'),
    ('kruška', 'груша'),
    ('banana', 'банан'),
    ('grejpfrut', 'грейпфрут'),
    ('ananas', 'ананас'),
    ('mango', 'манго'),
    ('kivi', 'киви'),
    ('azijska trešnja', 'личи'),
    ('longan', 'лонган'),
    ('marakuja', 'маракуйя'),
    ('avokado', 'авокадо'),
    ('kokos', 'кокос'),
    ('pasulj', 'сухая фасоль'),
    ('boranija', 'фасоль'),
    ('grašak', 'горошек'),
    ('crni luk', 'лук'),
    ('beli luk', 'чеснок'),
    ('blitva', 'мангольд'),
    ('cvekla', 'свекла'),
    ('šargarepa', 'морковь'),
    ('krompir', 'картошка'),
    ('kupus', 'капуста'),
    ('patlidžan', 'баклажан'),
    ('tikvice', 'кабачок'),
    ('bundeva', 'тыква'),
    ('krastavac', 'огурец'),
    ('paradajz', 'помидор'),
    ('karfiol', 'цветная капуста'),
    ('celer', 'сельдерей'),
    ('spanać', 'шпинат'),
    ('salata', 'салат'),
    ('rotkvica', 'редис'),
    ('pečurke', 'грибы'),
    ('kukuruz', 'кукуруза'),
    ('praziluk', 'лук-порей'),
    ('artičoka', 'артишок'),
    ('špargla', 'спаржа'),
    ('prokelj', 'брюссельская капуста'),
    ('brokoli', 'брокколи'),
    ('ljuta papričica', 'перец чили'),
    ('čaj', 'чай'),
    ('kafa', 'кофе'),
    ('voda', 'вода'),
    ('sok', 'сок'),
    ('vino', 'вино'),
    ('pivo', 'пиво'),
    ('odeća', 'одежда'),
    ('bluza', 'блузка'),
    ('haljina', 'платье'),
    ('šorc', 'шорты'),
    ('pantalone', 'брюки'),
    ('suknja', 'юбка'),
    ('košulja', 'рубашка'),
    ('majica', 'футболка'),
    ('novčanik', 'сумка'),
    ('kombinezon', 'комбинезон'),
    ('farmerke', 'джинсы'),
    ('odelo', 'костюм'),
    ('helanke', 'леггинсы'),
    ('kaiš', 'ремень'),
    ('kravata', 'галстук'),
    ('kaput', 'пальто'),
    ('jakna', 'куртка'),
    ('mantil', 'плащ'),
    ('marama', 'платок'),
    ('džemper', 'свитер'),
    ('šal', 'шарф'),
    ('rukavice', 'перчатки'),
    ('kapa', 'кепка'),
    ('šešir', 'шляпа'),
    ('čizme', 'сапоги'),
    ('cipele', 'обувь'),
    ('sandale', 'сандалии'),
    ('kišobran', 'зонт'),
    ('leto', 'лето'),
    ('jesen', 'осень'),
    ('zima', 'зима'),
    ('proleće', 'весна'),
    ('ponedeljak', 'понедельник'),
    ('utorak', 'вторник'),
    ('sreda', 'среда'),
    ('četvrtak', 'четверг'),
    ('petak', 'пятница'),
    ('subota', 'суббота'),
    ('nedelja', 'воскресение'),
    ('januar', 'январь'),
    ('februar', 'февраль'),
    ('mart', 'март'),
    ('april', 'апрель'),
    ('maj', 'май'),
    ('jun', 'июнь'),
    ('jul', 'июль'),
    ('avgust', 'август'),
    ('septembar', 'сентябрь'),
    ('oktobar', 'октябрь'),
    ('novembar', 'ноябрь'),
    ('decembar', 'декабрь'),
    ('majka', 'мама'),
    ('otac', 'папа'),
    ('brat', 'брат'),
    ('sestra', 'сестра'),
    ('sin', 'сын'),
    ('ćerka', 'дочь'),
    ('roditelji', 'родители'),
    ('deca', 'дети'),
    ('dete', 'ребёнок'),
    ('maćeha', 'мачеха'),
    ('očuh', 'отчим'),
    ('zet', 'зять'),
    ('snaja', 'невестка'),
    ('supruga', 'жена'),
    ('suprug', 'муж'),
    ('deda', 'дедушка'),
    ('baba', 'бабушка'),
    ('unuk', 'внук'),
    ('unuka', 'внучка'),
    ('unučad', 'внуки'),
    ('tetka', 'тетя'),
    ('teča', 'дядя'),
    ('sestrić', 'племянник'),
    ('sestričina', 'племянница'),
    ('svekar', 'свекор'),
    ('svekrva', 'свекровь'),
    ('zet', 'шурин'),
    ('snaja', 'золовка'),
    ('rođak', 'родственник'),
]

class DownloadStatus(Enum):
    Ok = 0,
    NoUrl = 1
    NoDeclTable = 2
    Fatal = 3

def downloadNoun(nounPair: tuple[str, str]) -> DownloadStatus:

    class DeclTable():
        cells: list[str]

        def __init__(self, cells: list[str], gender: str) -> None:
            self.cells = cells
            self.gender = gender
        
        def extractCell(self, idx: int):
            if idx >= len(self.cells):
                return ''
            return self.cells[idx]
        
        def findCell(self, pattern: str):
            index = 0
            for cell in self.cells:
                if pattern in cell:
                    if pattern[-1] == 'I' and pattern[-2] != 'I' and 'II' in cell:
                        continue
                    return index
                index += 1
            return None
        
        def getHeaderCell(self, headerIndex: int, cellIndex: int):
            if headerIndex == None:
                return ''
            else:
                return self.extractCell(headerIndex + cellIndex + 1)

        def getRow(self, header: str, count: int) -> list[str]:
            res = []

            headerIdx = self.findCell(header)
            for i in range(count):
                res.append(self.getHeaderCell(headerIdx, i))
            return res

    def getDeclinationTable(noun: str, urlBase: str, tag: str, tagClass: str) -> tuple[DownloadStatus, DeclTable]:
        try:
            url = "{}/{}".format(urlBase, noun)
            url = parse.urlparse(url)
            url = url.scheme + "://" + url.netloc + parse.quote(url.path)
            pagecontent = urlopen(url).read()
            soup = BeautifulSoup(pagecontent, features="html.parser")
        except:
            return (DownloadStatus.NoUrl, None)

        tableTag = soup.find_all(tag, {'class': tagClass})

        if len(tableTag) == 0:
            return (DownloadStatus.NoDeclTable, None)
        if len(tableTag) > 1:
            print('multiple tables for `{}`! choosing the first one'.format(noun))

        cells = []
        for c in tableTag[0].find_all("td"):
            txt = c.get_text()
            txt = txt.replace('1', '')
            txt = txt.replace('2', '')
            txt = txt.replace('-', '')
            txt = txt.strip()
            cells.append(txt)

        gender = 'none'
        genderSpans = soup.find_all('span', {'class': 'gender'})
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

        return (DownloadStatus.Ok, DeclTable(cells, gender))
    
    print(nounPair)

    serbNoun, rusNoun = nounPair

    serbOk, serbTable = getDeclinationTable(serbNoun, 'https://sh.wiktionary.org/wiki', 'table', 'inflection-table')
    rusOk, rusTable  = getDeclinationTable(rusNoun, 'https://ru.wiktionary.org/wiki', 'table', 'morfotable ru')

    if serbOk != DownloadStatus.Ok:
        return serbOk

    def getRowOrEmpty(table, header):
        if table != None:
            return table.getRow(header, 2)
        else:
            return ['', '']

    serbNom  = getRowOrEmpty(serbTable, 'nominativ')
    serbGen  = getRowOrEmpty(serbTable, 'genitiv')
    serbDat  = getRowOrEmpty(serbTable, 'dativ')
    serbAku  = getRowOrEmpty(serbTable, 'akuzativ')
    serbVok  = getRowOrEmpty(serbTable, 'vokativ')
    serbInst = getRowOrEmpty(serbTable, 'instrumental')
    serbLok  = getRowOrEmpty(serbTable, 'lokativ')

    rusNom  = getRowOrEmpty(rusTable, 'Им.')
    rusGen  = getRowOrEmpty(rusTable, 'Р.')
    rusDat  = getRowOrEmpty(rusTable, 'Д.')
    rusAku  = getRowOrEmpty(rusTable, 'В.')
    rusVok  = rusNom
    rusInst = getRowOrEmpty(rusTable, 'Тв.')
    rusLok  = getRowOrEmpty(rusTable, 'Пр.')

    with io.open('out.txt', 'a', encoding='utf-8') as o:
        def endl():
            o.write('\n')

        def finish():
            o.write('\n---\n\n')

        def writeLine(template, rusForm, serbForm):
            if rusForm == None:
                rusForm = ''
            o.write('{}: {} | {}\n'.format(template, rusForm, serbForm))

        o.write(serbNoun)
        endl()
        o.write(serbTable.gender)
        endl()
        endl()
        
        Sing = 0
        Plur = 1

        writeLine('sing & nom',  rusNom[Sing],  serbNom[Sing])
        writeLine('sing & gen',  rusGen[Sing],  serbGen[Sing])
        writeLine('sing & dat',  rusDat[Sing],  serbDat[Sing])
        writeLine('sing & aku',  rusAku[Sing],  serbAku[Sing])
        writeLine('sing & vok',  rusVok[Sing],  serbVok[Sing])
        writeLine('sing & inst', rusInst[Sing], serbInst[Sing])
        writeLine('sing & lok',  rusLok[Sing],  serbLok[Sing])
        endl()

        writeLine('plur & nom',  rusNom[Plur],  serbNom[Plur])
        writeLine('plur & gen',  rusGen[Plur],  serbGen[Plur])
        writeLine('plur & dat',  rusDat[Plur],  serbDat[Plur])
        writeLine('plur & aku',  rusAku[Plur],  serbAku[Plur])
        writeLine('plur & vok',  rusVok[Plur],  serbVok[Plur])
        writeLine('plur & inst', rusInst[Plur], serbInst[Plur])
        writeLine('plur & lok',  rusLok[Plur],  serbLok[Plur])
        finish()

    return DownloadStatus.Ok

def generateNoun(noun: tuple[str, str]):
    print('{} generation'.format(noun))
    pass

with io.open('out.txt', 'w', encoding='utf-8') as o:
    o.write('fixed noun\n\n')

for noun in nouns:
    status = downloadNoun(noun)

    if status == DownloadStatus.NoUrl:
        print('ERROR: no URL for `{}`'.format(noun))
    elif status == DownloadStatus.NoDeclTable:
        print('ERROR: no declination table for `{}`'.format(noun))
    elif status == DownloadStatus.Fatal:
        print('ERROR: FATAL for `{}`'.format(noun))

    if not status == DownloadStatus.Ok:
        generateNoun(noun)
