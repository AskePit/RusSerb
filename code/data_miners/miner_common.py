from enum import Enum
from typing import Callable
from urllib.request import urlopen
from urllib import parse
import io
import sys
import copy
from bs4 import BeautifulSoup

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

class DownloadStatus(Enum):
    Ok = 0,
    NoUrl = 1
    NoDeclTable = 2
    Fatal = 3

class Cell:
    def __init__(self, row: str, column: int, subcolumnGetter: Callable[[str, int], str] = None, subcolumn: int = 0):
        self.row = row
        self.column = column
        self.subcolumnGetter = subcolumnGetter
        self.subcolumn = subcolumn

class DeclTable():
    cells: list[str]

    def __init__(self, cells: list[str]) -> None:
        self.cells = cells
    
    def extractCell(self, idx: int):
        if idx >= len(self.cells):
            return ''
        return self.cells[idx]
    
    def findCell(self, pattern: str):
        index = 0

        for cell in self.cells:
            if pattern == cell:
                return index
            index += 1
        
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
    
    def parseColumnedCell(self, pattern: str):
        def extractAfterColumn(line: str):
            return line.split(':')[1].strip()
            
        found = self.findCell(pattern)
        if found == None:
            return ''
        else:
            return extractAfterColumn(self.extractCell(found))
    
    def get(self, cell: Cell) -> str:
        if cell == None:
            return ''

        headerIdx = self.findCell(cell.row)
        if headerIdx == None:
            return ''

        text = self.getHeaderCell(headerIdx, cell.column)
        if cell.subcolumnGetter != None:
            text = cell.subcolumnGetter(text, cell.subcolumn)
        return text

def PreGarbageFilter(txt: str) -> str:
    for toDel in ['1', '2', '-', '—', '△', '*']:
        txt = txt.replace(toDel, '')

    replaceMap = {
        # rus
        'а́': 'а',
        'о́': 'о',
        'у́': 'у',
        'и́': 'и',
        'е́': 'е',
        'ю́': 'ю',
        'я́': 'я',
        'ы́': 'ы',

        # serb
        'ȉ': 'i',
        'ȕ': 'u',
        'ū': 'u',
        'ȇ': 'e',
        'ē': 'e',
        'ȅ': 'e',
        'ȍ': 'o',
        'ȁ': 'a',
        'ā': 'a',
    }

    for k, v in replaceMap.items():
        txt = txt.replace(k, v)

    txt = txt.strip()
    return txt

def PostGarbageFilter(txt: str) -> str:
    for toTrunk in ['/', '(']:
        idx = txt.find(toTrunk)
        if idx != -1:
            txt = txt[:idx].strip()
    return txt

class TableDownloader:
    def __init__(self, word: str, urlBase: str, tag: str, tagClass: str):
        self.word = word
        self.urlBase = urlBase
        self.tag = tag
        self.tagClass = tagClass
        self.table: list[str] = None

    def downloadSoup(self):
        url = "{}/{}".format(self.urlBase, self.word)
        url = parse.urlparse(url)
        url = url.scheme + "://" + url.netloc + parse.quote(url.path)
        pagecontent = urlopen(url).read()
        self.soup = BeautifulSoup(pagecontent, features="html.parser")

    def loadTable(self) -> DownloadStatus:
        tableTag = self.soup.find_all(self.tag, {'class': self.tagClass})

        if len(tableTag) == 0:
            return (DownloadStatus.NoDeclTable, None)
        if len(tableTag) > 1:
            print('multiple tables for `{}`! choosing the first one'.format(self.word))

        cells: list[str] = []
        for c in tableTag[0].find_all("td"):
            txt = c.get_text()
            txt = PreGarbageFilter(txt)
            cells.append(txt)

        self.table = DeclTable(cells)
        return DownloadStatus.Ok
    
    def loadCustom(self) -> DownloadStatus:
        # override it for custom stuff
        return DownloadStatus.Ok
    
    def __call__(self) -> tuple[DownloadStatus, DeclTable]:
        try:
            self.downloadSoup()
        except:
            return (DownloadStatus.NoUrl, None)

        res = self.loadTable()
        if res != DownloadStatus.Ok:
            return (res, None)

        res = self.loadCustom()
        if res != DownloadStatus.Ok:
            return (res, None)

        return (res, self.table)

class Writer:
    def __init__(self, file: str) -> None:
        self.file = io.open(file, 'w', encoding='utf-8')

    def setTables(self, serbTable: DeclTable, rusTable: DeclTable):
        self.serb = serbTable
        self.rus = rusTable

    def write(self, s: str):
        self.file.write(s)

    def writeLine(self, template, rusForm, serbForm):
        if rusForm == None:
            rusForm = ''
        if serbForm == None:
            serbForm = ''
        
        rusForm = PostGarbageFilter(rusForm)
        serbForm = PostGarbageFilter(serbForm)

        self.file.write('{}: {} | {}\n'.format(template, rusForm, serbForm))

    def endl(self):
        self.file.write('\n')

    def writeDecl(self, decl: str, rusCell: Cell, serbCell: Cell):
        ru = self.rus.get(rusCell) if self.rus != None else ''
        se = self.serb.get(serbCell) if self.serb != None else ''

        self.writeLine(decl, ru, se)
    
    def dumpText(self, text: list[str]):
        for l in text:
            self.file.write(l)

    def finishWord(self):
        self.file.write('\n---\n\n')
        self.file.flush()

    def finish(self):
        self.file.flush()
        self.file.close()

def LoadExistedData(filename: str) -> dict[str, list[str]]: # word name -> file piece
    voc = {}

    with io.open(filename, encoding='utf-8') as f:
        data = f.readlines()
        if not len(data):
            return voc

        # read data
        data = data[2:]
        
        TITLE = 0
        BODY = 1
        SPACE = 2

        stage = TITLE

        key: str = ''
        theWord: list[str] = []

        for l in data:
            if stage == SPACE:
                stage = TITLE
                continue

            theWord.append(l)

            if l.startswith('-'):
                # word end
                theWord.append('\n')
                voc[key] = copy.deepcopy(theWord)
                theWord = []
                stage = SPACE
            elif stage == TITLE:
                # title
                if l.isspace():
                    continue
                key = l.strip()                
                stage = BODY
    return voc

class WordsFile:
    filename: str
    words: list[tuple[str, str]]

    def __init__(self, filename: str, words: list[tuple[str, str]]):
        self.filename = filename
        self.words = words

class WordsLists:
    files: list[WordsFile]

    def __init__(self) -> None:
        self.files = []

    def add(self, filename: str, words: list[tuple[str, str]]):
        self.files.append(WordsFile(filename, words))
        return self

def ExecuteMiner(
    speechPart: str,
    wordsLists: WordsLists,
    downloadFunc: Callable[[tuple[str, str], Writer], DownloadStatus],
    generateFunc: Callable[[tuple[str, str], Writer], None],
):
    for wordsFile in wordsLists.files:
        file = wordsFile.filename
        desired = wordsFile.words

        existed: dict[str, list[str]] = LoadExistedData(file)

        # check if we really need to do any work
        allCovered = True
        for w in desired:
            if w[0] not in existed:
                allCovered = False
                break
        
        # if no - just exit
        if allCovered:
            print('Already up to date!')
            return
        
        # extend `desired` by `existed` to have a proper sorted order of all words
        desired += [(w, '') for w in existed if w not in dict(desired)]
        desired.sort(key=lambda tup: tup[0])

        o = Writer(file)
        o.file.write('declined {}\n\n'.format(speechPart))

        for word in desired:
            if word[0] in existed:
                o.dumpText(existed[word[0]])
                continue

            status = downloadFunc(word, o)

            if status == DownloadStatus.NoUrl:
                print('ERROR: no URL for `{}`'.format(word))
            elif status == DownloadStatus.NoDeclTable:
                print('ERROR: no declination table for `{}`'.format(word))
            elif status == DownloadStatus.Fatal:
                print('ERROR: FATAL for `{}`'.format(word))

            if not status == DownloadStatus.Ok:
                generateFunc(word, o)
        
        o.finish()
