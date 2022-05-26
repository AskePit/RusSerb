import os
import sys
sys.path.append(os.path.abspath('../'))
from miner_common import *

nouns = [
    ('muzej', 'музей'),
    ('mačka', 'кошка'),
    ('pas', 'пёс'),
    ('jaje', 'яйцо'),
    '''
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
    ('celer', 'сельдерей'),
    ('spanać', 'шпинат'),
    ('salata', 'салат'),
    ('rotkvica', 'редис'),
    ('pečurke', 'грибы'),
    ('kukuruz', 'кукуруза'),
    ('praziluk', 'лук-порей'),
    ('artičoka', 'артишок'),
    ('špargla', 'спаржа'),
    ('brokoli', 'брокколи'),
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
    '''
]

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

    o.writeDecl('sing & nom',  Cell('Им.', Plur), Cell('nominativ', Plur))
    o.writeDecl('sing & gen',  Cell('Р.', Plur),  Cell('genitiv', Plur))
    o.writeDecl('sing & dat',  Cell('Д.', Plur),  Cell('dativ', Plur))
    o.writeDecl('sing & aku',  Cell('В.', Plur),  Cell('akuzativ', Plur))
    o.writeDecl('sing & vok',  Cell('Им.', Plur), Cell('vokativ', Plur))
    o.writeDecl('sing & inst', Cell('Тв.', Plur), Cell('instrumental', Plur))
    o.writeDecl('sing & lok',  Cell('Пр.', Plur), Cell('lokativ', Plur))
    o.finishWord()

    return DownloadStatus.Ok

def generateNoun(noun: tuple[str, str]):
    print('{} generation'.format(noun))
    pass

ExecuteMiner('noun', nouns, downloadNoun, generateNoun, 'out.txt')
