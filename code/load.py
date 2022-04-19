from code.core_types import *
import io
import sys
#import re
import glob
import os

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

SEPARATORS_REGEXP: str = '\n'
INLINE_SEPARATOR: str = '|'

def ConvertLinesToTokens(lines: list[str]) -> list[str]:
    megaLine = ''.join(lines)
    #res = re.split(SEPARATORS_REGEXP, megaLine)
    res = megaLine.split(SEPARATORS_REGEXP)
    res[:] = [x for x in res if x]
    return res
    
class Header:
    speechPart = SpeechPart.noun
    formsSequence: list[Declination] = []
    cursor = 0
            
    def parseHeader(self, speechPart: SpeechPart, lines: list[str]):
        self.speechPart = speechPart
        
        parseSequence = ConvertLinesToTokens(lines)
        for seq in parseSequence:
            self.formsSequence.append(Declination.Make(speechPart, seq))
        
    def yieldDeclination(self) -> Declination:
        if len(self.formsSequence) == 0:
            return None

        if self.cursor >= len(self.formsSequence):
            return None
        
        res = self.formsSequence[self.cursor]
        self.cursor = self.cursor + 1
        return res
    
    def resetYield(self):
        self.cursor = 0
    
    def toString(self):
        res = ""
        for decl in self.formsSequence:
            res = res + decl.toString() + '\n'
        return res

def LoadHeadered(data: list[str], speechPart: SpeechPart, theWords: WordList): 
    headerLines = 0
    headerRed = False
    
    header = Header()
    
    #header read
    for l in data:
        if l.startswith('-'):
            headerRed = True
            continue
        
        if not headerRed:
            headerLines = headerLines + 1
            continue
    
    header.parseHeader(speechPart, data[:headerLines])
    
    # read data
    data = data[headerLines+1:]
    data = ConvertLinesToTokens(data)

    firstTitle = ""
    if len(data):
        firstTitle = data[0].split(INLINE_SEPARATOR)[0]
    
    theWord = Word.MakeTitled(speechPart, firstTitle)

    for wordPair in data:
        words = wordPair.split(INLINE_SEPARATOR)
        rus = words[0]
        serb = words[1]

        form = header.yieldDeclination()
        if form is None:
            theWords.words.append(theWord)

            # new theWord
            theWord = Word.MakeTitled(speechPart, rus)

            header.resetYield()
            form = header.yieldDeclination()

        theWord.forms.append(DeclinedWord.Make(form, rus, serb))
    
    theWord.normalize()
    theWords.words.append(theWord)

def LoadFixed(data: list[str], theWord: Word):
    # read data
    data = ConvertLinesToTokens(data)

    title = ""
    if len(data):
        p = data[0].split(INLINE_SEPARATOR)
        title = p[0] if len(p[0]) else p[1]
    
    theWord.title = title
    
    declinationTime = False
    rus = ""
    serb = ""

    for w in data:
        if declinationTime:
            declinationTime = False
            declinedWord = DeclinedWord.Make(Declination.Make(SpeechPart.tobe, w), rus, serb)
            theWord.forms.append(declinedWord)
        else:
            declinationTime = True

            words = w.split(INLINE_SEPARATOR)
            rus = words[0]
            serb = words[1]
            continue
    
    theWord.normalize()

def LoadPhrases(title: str, data: list[str], thePhrases: PhrasesList):
    # read data
    data = ConvertLinesToTokens(data)
    
    thePhrases.title = title
    
    for w in data:
        words = w.split(INLINE_SEPARATOR)
        thePhrases.phrases.append(Phrase(words[0], words[1], words[2] if len(words) > 2 else None))

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

        if headerType == 'header':
            theWords = WordList()
            LoadHeadered(data, speechPart, theWords)
            return theWords
        elif headerType == 'fixed':
            theWord = Word.Make(speechPart)
            LoadFixed(data, theWord)
            return theWord
        elif headerType == 'phrases':
            thePhrases = PhrasesList()
            LoadPhrases(title, data, thePhrases)
            return thePhrases

VOCABULARY_EXT = 'voc'
EXCERCISE_EXT = 'exc'

def LoadVocabulary():
    vocRegex = '**/*.%s' % (VOCABULARY_EXT)
    for f in glob.glob(vocRegex, recursive=True):
        collectionName = os.path.splitext(os.path.basename(f))[0]
        data = LoadFile(f, collectionName)
        vocabulary[collectionName] = data
