from code.core_types import *
from code.excercise_types import *
import io
import sys
import glob
import os

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

SEPARATORS_REGEXP: str = '\n'
INLINE_SEPARATOR: str = '|'

def ConvertLinesToTokens(lines: list[str]) -> list[str]:
    megaLine = ''.join(lines)
    res = megaLine.split(SEPARATORS_REGEXP)
    res[:] = [x for x in res if x]
    return res
    
class Header:
    speechPart = SpeechPart.noun
    formsSequence: list[Declination] = []
    cursor = 0

    def __init__(self) -> None:
        self.speechPart = SpeechPart.noun
        self.formsSequence = []
        self.cursor = 0

    def parseHeader(self, speechPart: SpeechPart, lines: list[str]):
        self.speechPart = speechPart
        
        parseSequence = ConvertLinesToTokens(lines)
        for seq in parseSequence:
            self.formsSequence.append(Declination.Parse(seq))
        
    def yieldDeclination(self) -> Declination:
        if len(self.formsSequence) == 0:
            return None

        if self.cursor >= len(self.formsSequence):
            return None
        
        res = self.formsSequence[self.cursor]
        self.cursor += 1
        return res
    
    def resetYield(self):
        self.cursor = 0
    
    def toString(self):
        res = ""
        for decl in self.formsSequence:
            res += decl.toString() + '\n'
        return res

def LoadDeclined(data: list[str], speechPart: SpeechPart, theWords: WordList):
    # read data
    data = ConvertLinesToTokens(data)
    
    stage = 0
    theWord = Word.Make(speechPart)

    for l in data:
        if l.startswith('-'):
            # word end
            theWord.normalize()
            theWords.words.append(theWord)
            theWord = Word.Make(speechPart)
            stage = 0
        elif stage == 0:
            # title
            theWord.title = l.strip()
            stage += 1
        elif stage == 1:
            # metaDeclination
            if l.strip() != 'none':
                theWord.metaDeclination = Declination.Parse(l.strip())
            stage += 1
        elif stage == 2:
            # declinations and forms
            declWriting = l.split(':')

            decl = declWriting[0].strip()
            writing = declWriting[1].strip()
            
            words = writing.split(INLINE_SEPARATOR)
            rus = words[0].strip()
            serb = words[1].strip()

            declinedWord = DeclinedWord.Make(Declination.Parse(decl), rus, serb)
            theWord.forms.append(declinedWord)

def LoadPhrases(title: str, data: list[str], thePhrases: PhrasesList):
    # read data
    data = ConvertLinesToTokens(data)
    
    thePhrases.title = title
    
    for w in data:
        words = w.split(INLINE_SEPARATOR)
        rus = words[0].strip()
        serb = words[1].strip()
        aux = words[2].strip() if len(words) > 2 else None
        thePhrases.phrases.append(Phrase(rus, serb, aux))

def LoadFile(filename: str, title: str):
    with io.open(filename, encoding='utf-8') as f:
        data = f.readlines()
        if not len(data):
            return
        
        headerP = data[0].strip().split(' ')
        headerType = headerP[0]

        if len(headerP) > 1:
            speechPart = SpeechPart[headerP[1]]

        data = data[2:]
        data = [l for l in data if not l.startswith('#')]

        if headerType == 'declined':
            theWords = WordList()
            LoadDeclined(data, speechPart, theWords)
            return theWords
        elif headerType == 'phrases':
            thePhrases = PhrasesList()
            LoadPhrases(title, data, thePhrases)
            return thePhrases

VOCABULARY_EXT = 'voc'
EXCERCISE_EXT = 'exc'
EXCERCISE_TITLE_FILENAME = '_title'

def LoadVocabulary():
    vocRegex = '**/*.{}'.format(VOCABULARY_EXT)
    for f in glob.glob(vocRegex, recursive=True):
        collectionName = os.path.splitext(os.path.basename(f))[0]
        data = LoadFile(f, collectionName)

        if isinstance(data, WordList):
            unwrapped = data.tryUnwrap()
            if unwrapped != None:
                data = unwrapped

        vocabulary[collectionName] = data

def LoadExcercises():
    def LoadDir(dirname, parent: ExcerciseDescsDir) -> ExcerciseDescsDir:
        number = GetSerialNumber(dirname)
        excDir = ExcerciseDescsDir(parent, number)

        for f in glob.glob('{}/**'.format(dirname)):
            if os.path.isdir(f):
                excDir.children.append(LoadDir(f, excDir))
            elif os.path.isfile(f):
                if os.path.basename(f) == EXCERCISE_TITLE_FILENAME:
                    excDir.name = LoadTitle(f)
                else:
                    excDir.excercises.append(LoadExcercise(f, excDir))
        return excDir

    def LoadExcercise(filename, parent: ExcerciseDescsDir) -> ExcerciseDesc:
        with io.open(filename, encoding='utf-8') as f:
            number = GetSerialNumber(filename)
            data = f.readlines()

            name = data[0].strip()
            type = ExcerciseType[data[1].strip()]

            if type == ExcerciseType.phrases:
                voc = data[2].strip()
                return ExcerciseDesc.MakePhrasesEx(name, voc, parent, number)
            else:
                funcName = data[2].strip()
                return ExcerciseDesc.MakeCustomEx(name, funcName, parent, number)
    
    def LoadTitle(filename) -> str:
        with io.open(filename, encoding='utf-8') as f:
            data = f.readlines()
            return data[0] if len(data) else ''

    def GetSerialNumber(filename: str):
        f = os.path.basename(filename)

        if ' ' in f:
            return int(f.split(' ')[0].strip())
        return 0

    return LoadDir('excercises', None)
