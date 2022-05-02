from enum import Enum
from urllib.request import urlopen
from urllib import parse
import io
import sys
from bs4 import BeautifulSoup

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

verbs = [
]

nonTabledVerbs = [
]

modalVerbs = [
    'morati',
    'treba',
    'moći',
    'znati',
    'umeti',
    'smeti',
    'želeti',
    'voleti',
    'hteti'
]

class DownloadStatus(Enum):
    Ok = 0,
    NoUrl = 1
    NoDeclTable = 2
    Fatal = 3

def downloadVerb(verb: str) -> DownloadStatus:
    print(verb)

    try:
        url = "https://sh.wiktionary.org/wiki/{}".format(verb)
        url = parse.urlparse(url)
        url = url.scheme + "://" + url.netloc + parse.quote(url.path)
        pagecontent = urlopen(url).read()
        soup = BeautifulSoup(pagecontent, features="html.parser")
    except:
        return DownloadStatus.NoUrl

    try:
        tbody = soup.find_all("tbody")

        if len(tbody) == 0:
            return DownloadStatus.NoDeclTable
        if len(tbody) > 1:
            print('multiple tables for `{}`! choosing the first one'.format(verb))

        cells = []
        for c in tbody[0].find_all("td"):
            txt = c.get_text()
            txt = txt.replace('1', '')
            txt = txt.replace('2', '')
            txt = txt.replace('-', '')
            txt = txt.strip()
            cells.append(txt)

        def extractCell(idx: int):
            if idx >= len(cells):
                return ''
            return cells[idx]
        
        def findCell(pattern: str):
            index = 0
            for cell in cells:
                if pattern in cell:
                    if pattern[-1] == 'I' and pattern[-2] != 'I' and 'II' in cell:
                        continue
                    return index
                index += 1
            return None

        def extractAfterColumn(line: str):
            return line.split(':')[1].strip()

        def parseColumnedCell(pattern: str):
            found = findCell(pattern)
            if found == None:
                return ''
            else:
                return extractAfterColumn(extractCell(found))
        
        def getHeaderCell(headerIndex: int, cellIndex: int):
            if headerIndex == None:
                return ''
            else:
                return extractCell(headerIndex + cellIndex + 1)

        infinitiv = parseColumnedCell('Infinitiv:')
        participle_present = parseColumnedCell('Glagolski prilog sadašnji:')
        participle_past = parseColumnedCell('Glagolski prilog prošli:')
        verbal_noun = parseColumnedCell('Glagolska imenica:')

        def splitFutur1(futur: str):
            futur = futur.replace('\n', ' ')
            splitted = futur.split(' ')
            futur_1 = (splitted[0] + ' ' + splitted[1]).strip()
            splitted = splitted[2:]
            futur_2 = ' '.join(splitted).strip()

            #print((futur_1, futur_2))
            return (futur_1, futur_2)

        def splitVerbalAdjective(adjective: str):
            #print(adjective)
            splitted = adjective.split('/')
            if len(splitted) < 3:
                return ('', '', '')

            m = splitted[0].strip()[:-3]
            f = splitted[1].strip()[:-3]
            n = splitted[2].strip()[:-2]
            
            #print((m, f, n))
            return (m, f, n)

        presentHeader = findCell('Prezent')
        present_sing_1 = getHeaderCell(presentHeader, 0)
        present_sing_2 = getHeaderCell(presentHeader, 1)
        present_sing_3 = getHeaderCell(presentHeader, 2)
        present_plur_1 = getHeaderCell(presentHeader, 3)
        present_plur_2 = getHeaderCell(presentHeader, 4)
        present_plur_3 = getHeaderCell(presentHeader, 5)

        futur1Header = findCell('Futur I')
        futur1_sing_1, futur1_sing_1_alt = splitFutur1(getHeaderCell(futur1Header, 0))
        futur1_sing_2, futur1_sing_2_alt = splitFutur1(getHeaderCell(futur1Header, 1))
        futur1_sing_3, futur1_sing_3_alt = splitFutur1(getHeaderCell(futur1Header, 2))
        futur1_plur_1, futur1_plur_1_alt = splitFutur1(getHeaderCell(futur1Header, 3))
        futur1_plur_2, futur1_plur_2_alt = splitFutur1(getHeaderCell(futur1Header, 4))
        futur1_plur_3, futur1_plur_3_alt = splitFutur1(getHeaderCell(futur1Header, 5))

        futur2Header = findCell('Futur II')
        futur2_sing_1 = getHeaderCell(futur2Header, 0)
        futur2_sing_2 = getHeaderCell(futur2Header, 1)
        futur2_sing_3 = getHeaderCell(futur2Header, 2)
        futur2_plur_1 = getHeaderCell(futur2Header, 3)
        futur2_plur_2 = getHeaderCell(futur2Header, 4)
        futur2_plur_3 = getHeaderCell(futur2Header, 5)

        perfektHeader = findCell('Perfekt')
        perfekt_sing_1 = getHeaderCell(perfektHeader, 0)
        perfekt_sing_2 = getHeaderCell(perfektHeader, 1)
        perfekt_sing_3 = getHeaderCell(perfektHeader, 2)
        perfekt_plur_1 = getHeaderCell(perfektHeader, 3)
        perfekt_plur_2 = getHeaderCell(perfektHeader, 4)
        perfekt_plur_3 = getHeaderCell(perfektHeader, 5)

        pluskvamperfektHeader = findCell('Pluskvamperfekt')
        pluskvamperfekt_sing_1 = getHeaderCell(pluskvamperfektHeader, 0)
        pluskvamperfekt_sing_2 = getHeaderCell(pluskvamperfektHeader, 1)
        pluskvamperfekt_sing_3 = getHeaderCell(pluskvamperfektHeader, 2)
        pluskvamperfekt_plur_1 = getHeaderCell(pluskvamperfektHeader, 3)
        pluskvamperfekt_plur_2 = getHeaderCell(pluskvamperfektHeader, 4)
        pluskvamperfekt_plur_3 = getHeaderCell(pluskvamperfektHeader, 5)

        aoristHeader = findCell('Aorist')
        aorist_sing_1 = getHeaderCell(aoristHeader, 0)
        aorist_sing_2 = getHeaderCell(aoristHeader, 1)
        aorist_sing_3 = getHeaderCell(aoristHeader, 2)
        aorist_plur_1 = getHeaderCell(aoristHeader, 3)
        aorist_plur_2 = getHeaderCell(aoristHeader, 4)
        aorist_plur_3 = getHeaderCell(aoristHeader, 5)

        imperfektHeader = findCell('Imperfekt')
        imperfekt_sing_1 = getHeaderCell(imperfektHeader, 0)
        imperfekt_sing_2 = getHeaderCell(imperfektHeader, 1)
        imperfekt_sing_3 = getHeaderCell(imperfektHeader, 2)
        imperfekt_plur_1 = getHeaderCell(imperfektHeader, 3)
        imperfekt_plur_2 = getHeaderCell(imperfektHeader, 4)
        imperfekt_plur_3 = getHeaderCell(imperfektHeader, 5)

        conditional1Header = findCell('Kondicional I')
        conditional1_sing_1 = getHeaderCell(conditional1Header, 0)
        conditional1_sing_2 = getHeaderCell(conditional1Header, 1)
        conditional1_sing_3 = getHeaderCell(conditional1Header, 2)
        conditional1_plur_1 = getHeaderCell(conditional1Header, 3)
        conditional1_plur_2 = getHeaderCell(conditional1Header, 4)
        conditional1_plur_3 = getHeaderCell(conditional1Header, 5)

        conditional2Header = findCell('Kondicional II')
        conditional2_sing_1 = getHeaderCell(conditional2Header, 0)
        conditional2_sing_2 = getHeaderCell(conditional2Header, 1)
        conditional2_sing_3 = getHeaderCell(conditional2Header, 2)
        conditional2_plur_1 = getHeaderCell(conditional2Header, 3)
        conditional2_plur_2 = getHeaderCell(conditional2Header, 4)
        conditional2_plur_3 = getHeaderCell(conditional2Header, 5)

        imperativHeader = findCell('Imperativ')
        imperativ_sing_1 = getHeaderCell(imperativHeader, 0)
        imperativ_sing_2 = getHeaderCell(imperativHeader, 1)
        imperativ_sing_3 = getHeaderCell(imperativHeader, 2)
        imperativ_plur_1 = getHeaderCell(imperativHeader, 3)
        imperativ_plur_2 = getHeaderCell(imperativHeader, 4)
        imperativ_plur_3 = getHeaderCell(imperativHeader, 5)

        activeHeader = findCell('Glagolski pridjev radni')
        verbal_adjective_active_sing_m, verbal_adjective_active_sing_f, verbal_adjective_active_sing_n = splitVerbalAdjective(getHeaderCell(activeHeader, 0))
        verbal_adjective_active_plur_m, verbal_adjective_active_plur_f, verbal_adjective_active_plur_n = splitVerbalAdjective(getHeaderCell(activeHeader, 1))

        passiveHeader = findCell('Glagolski pridjev trpni')
        verbal_adjective_passive_sing_m, verbal_adjective_passive_sing_f, verbal_adjective_passive_sing_n = splitVerbalAdjective(getHeaderCell(passiveHeader, 0))
        verbal_adjective_passive_plur_m, verbal_adjective_passive_plur_f, verbal_adjective_passive_plur_n = splitVerbalAdjective(getHeaderCell(passiveHeader, 1))

        with io.open('out.txt', 'a', encoding='utf-8') as o:
            o.write(infinitiv)
            o.write('\nnone\n\n')

            def writeLine(template, form):
                o.write('{}:  | {}\n'.format(template, form))

            def endl():
                o.write('\n')

            def finish():
                o.write('\n---\n\n')

            writeLine('inf', infinitiv)
            endl()
            
            writeLine('present & sing & first', present_sing_1)
            writeLine('present & sing & second', present_sing_2)
            writeLine('present & sing & third', present_sing_3)
            writeLine('present & plur & first', present_plur_1)
            writeLine('present & plur & second', present_plur_2)
            writeLine('present & plur & third', present_plur_3)
            endl()
            
            writeLine('futur & sing & first', futur1_sing_1_alt)
            writeLine('futur & sing & second', futur1_sing_2_alt)
            writeLine('futur & sing & third', futur1_sing_3_alt)
            writeLine('futur & plur & first', futur1_plur_1_alt)
            writeLine('futur & plur & second', futur1_plur_2_alt)
            writeLine('futur & plur & third', futur1_plur_3_alt)
            endl()

            writeLine('perfect & sing & first', perfekt_sing_1)
            writeLine('perfect & sing & second', perfekt_sing_2)
            writeLine('perfect & sing & third', perfekt_sing_3)
            writeLine('perfect & plur & first', perfekt_plur_1)
            writeLine('perfect & plur & second', perfekt_plur_2)
            writeLine('perfect & plur & third', perfekt_plur_3)
            endl()

            writeLine('imperfect & sing & first', imperfekt_sing_1)
            writeLine('imperfect & sing & second', imperfekt_sing_2)
            writeLine('imperfect & sing & third', imperfekt_sing_3)
            writeLine('imperfect & plur & first', imperfekt_plur_1)
            writeLine('imperfect & plur & second', imperfekt_plur_2)
            writeLine('imperfect & plur & third', imperfekt_plur_3)
            endl()

            writeLine('# participle & present', participle_present)
            writeLine('# participle & past', participle_past)
            writeLine('# noun', verbal_noun)
            endl()

            writeLine('# futur & sing & first', futur1_sing_1)
            writeLine('# futur & sing & second', futur1_sing_2)
            writeLine('# futur & sing & third', futur1_sing_3)
            writeLine('# futur & plur & first', futur1_plur_1)
            writeLine('# futur & plur & second', futur1_plur_2)
            writeLine('# futur & plur & third', futur1_plur_3)
            endl()

            writeLine('# futur2 & sing & first', futur2_sing_1)
            writeLine('# futur2 & sing & second', futur2_sing_2)
            writeLine('# futur2 & sing & third', futur2_sing_3)
            writeLine('# futur2 & plur & first', futur2_plur_1)
            writeLine('# futur2 & plur & second', futur2_plur_2)
            writeLine('# futur2 & plur & third', futur2_plur_3)
            endl()

            writeLine('# pluskvamperfekt & sing & first', pluskvamperfekt_sing_1)
            writeLine('# pluskvamperfekt & sing & second', pluskvamperfekt_sing_2)
            writeLine('# pluskvamperfekt & sing & third', pluskvamperfekt_sing_3)
            writeLine('# pluskvamperfekt & plur & first', pluskvamperfekt_plur_1)
            writeLine('# pluskvamperfekt & plur & second', pluskvamperfekt_plur_2)
            writeLine('# pluskvamperfekt & plur & third', pluskvamperfekt_plur_3)
            endl()

            writeLine('# aorist & sing & first', aorist_sing_1)
            writeLine('# aorist & sing & second', aorist_sing_2)
            writeLine('# aorist & sing & third', aorist_sing_3)
            writeLine('# aorist & plur & first', aorist_plur_1)
            writeLine('# aorist & plur & second', aorist_plur_2)
            writeLine('# aorist & plur & third', aorist_plur_3)
            endl()

            writeLine('# cond1 & sing & first', conditional1_sing_1)
            writeLine('# cond1 & sing & second', conditional1_sing_2)
            writeLine('# cond1 & sing & third', conditional1_sing_3)
            writeLine('# cond1 & plur & first', conditional1_plur_1)
            writeLine('# cond1 & plur & second', conditional1_plur_2)
            writeLine('# cond1 & plur & third', conditional1_plur_3)
            endl()

            writeLine('# cond2 & sing & first', conditional2_sing_1)
            writeLine('# cond2 & sing & second', conditional2_sing_2)
            writeLine('# cond2 & sing & third', conditional2_sing_3)
            writeLine('# cond2 & plur & first', conditional2_plur_1)
            writeLine('# cond2 & plur & second', conditional2_plur_2)
            writeLine('# cond2 & plur & third', conditional2_plur_3)
            endl()

            writeLine('# imperativ & sing & first', imperativ_sing_1)
            writeLine('# imperativ & sing & second', imperativ_sing_2)
            writeLine('# imperativ & sing & third', imperativ_sing_3)
            writeLine('# imperativ & plur & first', imperativ_plur_1)
            writeLine('# imperativ & plur & second', imperativ_plur_2)
            writeLine('# imperativ & plur & third', imperativ_plur_3)
            endl()

            writeLine('# active & sing & m', verbal_adjective_active_sing_m)
            writeLine('# active & sing & f', verbal_adjective_active_sing_f)
            writeLine('# active & sing & n', verbal_adjective_active_sing_n)
            writeLine('# active & plur & m', verbal_adjective_active_plur_m)
            writeLine('# active & plur & f', verbal_adjective_active_plur_f)
            writeLine('# active & plur & n', verbal_adjective_active_plur_n)
            endl()

            writeLine('# passive & sing & m', verbal_adjective_passive_sing_m)
            writeLine('# passive & sing & f', verbal_adjective_passive_sing_f)
            writeLine('# passive & sing & n', verbal_adjective_passive_sing_n)
            writeLine('# passive & plur & m', verbal_adjective_passive_plur_m)
            writeLine('# passive & plur & f', verbal_adjective_passive_plur_f)
            writeLine('# passive & plur & n', verbal_adjective_passive_plur_n)
            finish()

        return DownloadStatus.Ok
    except:
        return DownloadStatus.Fatal

def generateVerb(verb: str):
    print('{} generation'.format(verb))
    pass

with io.open('out.txt', 'w', encoding='utf-8') as o:
    o.write('fixed verb\n\n')

for verb in verbs:
    status = downloadVerb(verb)

    if status == DownloadStatus.NoUrl:
        print('ERROR: no URL for `{}`'.format(verb))
    elif status == DownloadStatus.NoDeclTable:
        print('ERROR: no declination table for `{}`'.format(verb))
    elif status == DownloadStatus.Fatal:
        print('ERROR: FATAL for `{}`'.format(verb))

    if not status == DownloadStatus.Ok:
        generateVerb(verb)
