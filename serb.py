import io
import sys
#import re
from code.core_types import *

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

SEPARATORS_REGEXP: str = '\n'

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

def loadHeadered(data: list[str], speechPart: SpeechPart, theWords: list[Word]):        
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
        firstTitle = data[0].split('/')[0]
    
    theWord = Word.MakeTitled(speechPart, firstTitle)

    for wordPair in data:
        words = wordPair.split('/')
        rus = words[0]
        serb = words[1]

        form = header.yieldDeclination()
        if form == None:
            theWords.append(theWord)

            # new theWord
            theWord = Word.MakeTitled(speechPart, rus)

            header.resetYield()
            form = header.yieldDeclination()
        
        theWord.forms.append(DeclinedWord.Make(form, rus, serb))
        
    theWords.append(theWord)
    theWord = Word()
    theWord.forms = {}
    
    for occ in theWords:
        print(occ.toString())

def loadFixed(data: list[str], theWord: Word):
    # read data
    data = ConvertLinesToTokens(data)

    title = ""
    if len(data):
        p = data[0].split('/')
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

            words = w.split('/')
            rus = words[0]
            serb = words[1]
            continue
    
    theWord.normalize()

def loadFile(filename: str):
    with io.open(filename, encoding='utf-8') as f:
        data = f.readlines()
        if not len(data):
            return
        
        headerP = data[0].strip().split(' ')
        headerType = headerP[0]
        speechPart = SpeechPart[headerP[1]]

        data = data[2:]

        if headerType == 'header':
            theWords: list[Word] = []
            loadHeadered(data, speechPart, theWords)
            return theWords
        elif headerType == 'fixed':
            theWord = Word.Make(speechPart)
            loadFixed(data, theWord)
            return theWord

occupations = loadFile('data/occupations.txt')
pronoun = loadFile('data/pronouns.txt')
tobe = loadFile('data/tobe/tobe.txt')
positive_tobe = loadFile('data/tobe/positive_tobe.txt')
negative_tobe = loadFile('data/tobe/negative_tobe.txt')
question_tobe = loadFile('data/tobe/question_tobe.txt')

for occ in occupations:
    print(occ.toString())

print(pronoun.toString())
print(tobe.toString())
print(positive_tobe.toString())
print(negative_tobe.toString())
print(question_tobe.toString())