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
    
def LoadDeclined(data: list[str], speechPart: SpeechPart, theWords: WordList):
    # read data
    data = ConvertLinesToTokens(data)
    
    TITLE = 0
    META_DECL = 1
    DECL = 2

    stage = TITLE
    theWord = Word(speechPart)

    for l in data:
        if l.startswith('-'):
            # word end
            theWord.normalize()
            theWords.words.append(theWord)
            theWord = Word(speechPart)
            stage = TITLE
        elif stage == TITLE:
            # title
            theWord.title = l.strip()
            stage = META_DECL
        elif stage == META_DECL:
            # metaDeclination
            if l.strip() != 'none':
                theWord.metaDeclination = Declination.Parse(l.strip())
            else:
                theWord.metaDeclination = Declination()
            stage = DECL
        elif stage == DECL:
            # declinations and forms
            declWriting = l.split(':')

            decl = declWriting[0].strip()
            writing = declWriting[1].strip()
            
            words = writing.split(INLINE_SEPARATOR)
            serb = words[0].strip()
            rus = words[1].strip()

            declinedWord = WordForm(theWord, Declination.Parse(decl), rus, serb)
            theWord.forms.append(declinedWord)

def LoadPhrases(title: str, data: list[str], thePhrases: PhrasesList):
    # read data
    data = ConvertLinesToTokens(data)
    
    thePhrases.title = title
    
    for w in data:
        words = w.split(INLINE_SEPARATOR)
        serb = words[0].strip()
        rus = words[1].strip()
        aux = words[2].strip() if len(words) > 2 else None
        thePhrases.phrases.append(Phrase(rus, serb, aux))

def LoadBlockPhrases(title: str, data: list[str], thePhrases: PhrasesList):
    # read data
    data = ConvertLinesToTokens(data)
    
    SERB = 0
    RUS = 1

    stage = SERB
    thePhrase = Phrase([], [])

    for l in data:
        if l.startswith('---'):
            # phrase end
            thePhrase.normalize()
            thePhrases.phrases.append(copy.deepcopy(thePhrase))
            thePhrase = Phrase([], [])
            
            stage = SERB
        elif l.startswith('|'):
            # title
            stage = RUS
        elif stage == SERB:
            thePhrase.serb.append(l.strip())
        elif stage == RUS:
            thePhrase.rus.append(l.strip())

def LoadVocFile(filename: str, title: str):
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
        elif headerType == 'phrases' or headerType == 'unique':
            thePhrases = PhrasesList()
            LoadPhrases(title, data, thePhrases)
            return thePhrases
        elif headerType == 'block_phrases':
            thePhrases = PhrasesList()
            LoadBlockPhrases(title, data, thePhrases)
            return thePhrases

VOCABULARY_EXT = 'voc'
MAN_EXT = 'man'
EXCERCISE_EXT = 'exc'
EXCERCISE_TITLE_FILENAME = '_title'

def LoadVocabulary(path='.'):
    vocRegex = '{}/**/*.{}'.format(path, VOCABULARY_EXT)
    for f in glob.glob(vocRegex, recursive=True):
        collectionName = os.path.splitext(os.path.basename(f))[0]
        data = LoadVocFile(f, collectionName)

        if isinstance(data, WordList):
            unwrapped = data.tryUnwrap()
            if unwrapped != None:
                data = unwrapped

        vocabulary[collectionName] = data

def LoadManuals(path='.'):
    manRegex = '{}/**/*.{}'.format(path, MAN_EXT)
    for f in glob.glob(manRegex, recursive=True):
        manName = os.path.splitext(os.path.basename(f))[0]
        with io.open(f, encoding='utf-8') as f:
            data = f.read()
            mans[manName] = data

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
            help = data[3] if len(data) >= 4 else None

            if type == ExcerciseType.phrases:
                voc = data[2].strip()
                return ExcerciseDesc.MakePhrasesEx(name, voc, help, parent, number)
            else:
                funcNames = data[2].split()
                return ExcerciseDesc.MakeCustomEx(name, funcNames, help, parent, number)
    
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
