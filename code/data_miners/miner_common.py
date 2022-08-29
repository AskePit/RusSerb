from dataclasses import dataclass
import io
import sys
import copy
import glob
from enum import Enum
from typing import Callable
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

class DownloadStatus(Enum):
    Ok = 0,
    NoUrl = 1
    NoDeclTable = 2
    Fatal = 3

@dataclass
class Cell:
    row: str
    column: int
    subcolumnGetter: Callable[[str, int], str] = None
    subcolumn: int = 0,
    rowNum: int = 0

@dataclass
class DeclTable():
    cells: list[str]

    def accessCell(self, idx: int):
        if idx >= len(self.cells):
            return ''
        return self.cells[idx]

    def accessHeaderCell(self, headerIndex: int, cellIndex: int):
        if headerIndex == None:
            return ''
        else:
            return self.accessCell(headerIndex + cellIndex + 1)
    
    def findCell(self, rowPattern: str, rowNum: int = 0):
        # full match
        index = 0
        ri = 0

        for cell in self.cells:
            if rowPattern == cell:
                if ri < rowNum:
                    ri += 1
                else:
                    return index
            index += 1
        
        # partial match
        index = 0
        ri = 0

        for cell in self.cells:
            if rowPattern in cell:
                if rowPattern[-1] == 'I' and rowPattern[-2] != 'I' and 'II' in cell:
                    continue
                else:
                    if ri < rowNum:
                        ri += 1
                    else:
                        return index
            index += 1
        return None

    def parseColumnedCell(self, pattern: str, rowNum: int = 0):
        def extractAfterColumn(line: str):
            return line.split(':')[1].strip()
            
        found = self.findCell(pattern, rowNum)
        if found == None:
            return ''
        else:
            return extractAfterColumn(self.accessCell(found))
    
    def get(self, cell: Cell) -> str:
        if cell == None:
            return ''

        headerIdx = self.findCell(cell.row, cell.rowNum)
        if headerIdx == None:
            return ''

        text = self.accessHeaderCell(headerIdx, cell.column)
        if cell.subcolumnGetter != None:
            text = cell.subcolumnGetter(text, cell.subcolumn)
        return text

def PreGarbageFilter(txt: str) -> str:
    for toDel in ['1', '2', '-', '—', '△', '*']:
        txt = txt.replace(toDel, '')

    replaceMap = {
        # rus
        'а́': 'а',
        'е́': 'е',
        'и́': 'и',
        'о́': 'о',
        'у́': 'у',
        'ы́': 'ы',
        'э́': 'э',
        'ю́': 'ю',
        'я́': 'я',

        # serb
        'ȉ': 'i',
        'ȋ': 'i',
        'ī': 'i',
        'ì': 'i',
        'í': 'i',

        'ȕ': 'u',
        'ȗ': 'u',
        'ū': 'u',
        'ù': 'u',
        'ú': 'u',

        'ȅ': 'e',
        'ȇ': 'e',
        'ē': 'e',
        'è': 'e',
        'é': 'e',

        'ȍ': 'o',
        'ȏ': 'o',
        'ō': 'o',
        'ò': 'o',
        'ó': 'o',

        'ȁ': 'a',
        'â': 'a',
        'ā': 'a',
        'à': 'a',
        'á': 'a',
    }

    for k, v in replaceMap.items():
        txt = txt.replace(k, v)

    txt = txt.strip()
    return txt

def PostGarbageFilter(txt: str) -> str:
    for toTrunk in ['/', '(', ',', ' ']:
        idx = txt.find(toTrunk)
        if idx != -1:
            txt = txt[:idx].strip()
    return txt

@dataclass
class TableDownloader:
    word: str
    urlBase: str
    header: str
    tag: str
    tagClass: str
    tagIdx: int = 0
    table: list[str] = None

    def downloadSoup(self):
        url = f'{self.urlBase}/{self.word}'
        url = parse.urlparse(url)
        url = url.scheme + "://" + url.netloc + parse.quote(url.path)
        pagecontent = urlopen(url).read()
        self.soup = BeautifulSoup(pagecontent, features="html.parser")
        for line_break in self.soup.findAll('br'): # loop through line break tags
            line_break.replaceWith(' ')            # replace br tags with delimiter

    def loadTable(self) -> DownloadStatus:
        start = self.soup
        tableTags = None
        if self.header != None:
            start = self.soup.find('span', {'class': 'mw-headline'}, True, self.header)
            if start != None:
                start = start.parent
            if start != None:    
                tableTags = start.find_all_next(self.tag, {'class': self.tagClass})
        else:
            tableTags = start.find_all(self.tag, {'class': self.tagClass})

        if tableTags == None:
            return (DownloadStatus.NoDeclTable, None)
        if len(tableTags) == 0:
            return (DownloadStatus.NoDeclTable, None)
        if len(tableTags) <= self.tagIdx:
            return (DownloadStatus.NoDeclTable, None)
        if len(tableTags) > self.tagIdx + 1:
            print(f'multiple tables for `{self.word}`! choosing the first one')

        cells: list[str] = []
        for c in tableTags[self.tagIdx].find_all(["td", "th"]):
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

    def writeLine(self, template, rusForm, serbForm, postGarbage = True):
        if rusForm == None:
            rusForm = ''
        if serbForm == None:
            serbForm = ''
        
        if postGarbage:
            rusForm = PostGarbageFilter(rusForm)
            serbForm = PostGarbageFilter(serbForm)

        self.file.write(f'{template}: {serbForm} | {rusForm}\n')

    def endl(self):
        self.file.write('\n')

    def writeDecl(self, decl: str, rusCell: Cell|str, serbCell: Cell|str):
        postGarbage = True

        if type(rusCell) is Cell:
            ru = self.rus.get(rusCell) if self.rus != None else ''
        else:
            ru = rusCell
            postGarbage = False

        if type(serbCell) is Cell:
            se = self.serb.get(serbCell) if self.serb != None else ''
        else:
            se = serbCell
            postGarbage = False

        self.writeLine(decl, ru, se, postGarbage)
    
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
    listFilename: str
    vocFilename: str
    words: list[tuple[str, str]]
    failedWords: list[str]

    def __init__(self):
        self.listFilename = ''
        self.vocFilename = ''
        self.words = []
        self.failedWords = []
    
    def Load(listFilename: str) -> 'WordsFile':
        res = WordsFile()
        res.listFilename = listFilename

        with io.open(listFilename, encoding='utf-8') as f:
            data = f.readlines()
            data = [l for l in data if not l.isspace()]
            res.vocFilename = data[0].strip()

            data = data[1:]

            for l in data:
                splitted = l.split('|')
                serb = splitted[0].strip()
                rus = splitted[1].strip()

                if serb.startswith('#'):
                    serb = serb[1:].strip()
                    res.failedWords.append(serb)

                res.words.append((serb, rus))
        
        res.words.sort(key=lambda tup: tup[0])
        return res
    
    def __str__(self):
        res = self.vocFilename
        res += '\n\n'

        for w in self.words:
            failed = w[0] in self.failedWords
            possibleComment = '# ' if failed else ''
            res += f'{possibleComment}{w[0]} | {w[1]}\n'
        return res
    
    def markFailed(self, serbWord: str):
        self.failedWords.append(serbWord)
    
    def save(self):
        with io.open(self.listFilename, 'w', encoding='utf-8') as f:
            f.write(str(self))

class WordsLists:
    files: list[WordsFile]

    def __init__(self) -> None:
        self.files = []

    def add(self, filename: str, words: list[tuple[str, str]]):
        self.files.append(WordsFile(filename, words=words))
        return self
    
    def Load(dirname: str): # -> WordsLists
        res = WordsLists()

        listRegex = f'{dirname}/**/*.list'
        for filename in glob.glob(listRegex, recursive=True):
            res.files.append(WordsFile.Load(filename))

        return res

    def __str__(self):
        res = ''

        for f in self.files:
            res += str(f)
            res += '\n'

        return res
    
    def save(self):
        for f in self.files:
            f.save()

def ExecuteMiner(
    speechPart: str,
    wordsLists: WordsLists,
    downloadFunc: Callable[[tuple[str, str], Writer], DownloadStatus],
    generateFunc: Callable[[tuple[str, str], Writer], None],
):
    for wordsFile in wordsLists.files:
        file = wordsFile.vocFilename
        desired = copy.deepcopy(wordsFile.words)

        existed: dict[str, list[str]] = LoadExistedData(file)

        # check if we really need to do any work
        allCovered = True
        for w in desired:
            if w[0] in wordsFile.failedWords:
                continue
            if w[0] not in existed:
                allCovered = False
                break
        
        # if no - just exit
        if allCovered:
            print(f'{wordsFile.listFilename} is already up to date!')
            wordsFile.save()
            continue
        
        # extend `desired` by `existed` to have a proper sorted order of all words
        desired += [(w, '') for w in existed if w not in dict(desired)]
        desired.sort(key=lambda tup: tup[0])

        o = Writer(file)
        o.file.write(f'declined {speechPart}\n\n')

        for word in desired:
            if word[0] in existed:
                o.dumpText(existed[word[0]])
                continue

            if word[0] in wordsFile.failedWords:
                continue

            status = downloadFunc(word, o)

            if status == DownloadStatus.NoUrl:
                print(f'ERROR: no URL for `{word}`')
            elif status == DownloadStatus.NoDeclTable:
                print(f'ERROR: no declination table for `{word}`')
            elif status == DownloadStatus.Fatal:
                print(f'ERROR: FATAL for `{word}`')

            if status != DownloadStatus.Ok:
                res = generateFunc(word, o)
                if res == False:
                    wordsFile.markFailed(word[0])
        
        o.finish()
        wordsFile.save()
