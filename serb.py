import io
import sys
#import re
from enum import Enum

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

class SpeechPart(Enum):
    noun = 0,
    pronoun = 1
    tobe = 2
    verb = 3
    adjective = 4
    proverb = 5
    particle = 6

class Gender(Enum):
    male = 0
    fem = 1
    neu = 2
    unisex = 3
    
class Number(Enum):
    sing = 0
    plur = 1
    
class Case(Enum):
    nom = 0
    gen = 1
    dat = 2
    aku = 3
    vok = 4
    lok = 5
    inst = 6

class Person(Enum):
    first = 0
    second = 1
    third = 2

class Declination:
    speechPart: SpeechPart
    
    person: Person
    gender: Gender
    number: Number
    case: Case
    
    def make(speechPart: SpeechPart, form: str):
        res = Declination()
        res.speechPart = speechPart

        words = form.split('-')
        
        for word in words:
            try:
                res.person = Person[word]
            except:
                try:
                    res.number = Number[word]
                except:
                    try:
                        res.gender = Gender[word]
                    except:
                        try:
                            res.case = Case[word]
                        except:
                            raise Exception("Could not parse Declination!")
        return res
    
    def toString(self):
        first = True
        
        res = ""

        if hasattr(self, 'person'):
            if first:
                first = False
            else:
                res = res + '-'
            res = res + self.person.name
            
        if hasattr(self, 'gender'):
            if first:
                first = False
            else:
                res = res + '-'
            res = res + self.gender.name
            
        if hasattr(self, 'number'):
            if first:
                first = False
            else:
                res = res + '-'
            res = res + self.number.name

        if hasattr(self, 'case'):
            if first:
                first = False
            else:
                res = res + '-'
            res = res + self.case.name
        
        return res

class Word:
    declination: Declination
    rus: str
    serb: str

class Noun:
    title: str
    forms: list[Word]
    
    def toString(self):
        res = self.title + '\n'
        for word in self.forms:
            res = res + word.declination.toString() + ': ' + word.rus + '/' + word.serb +'\n'
        return res

class Pronoun:    
    title: str
    forms: list[Word]
    
    def toString(self):
        res = self.title + '\n'
        for word in self.forms:
            res = res + word.declination.toString() + ': ' + word.rus + '/' + word.serb +'\n'
        return res

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
            self.formsSequence.append(Declination.make(speechPart, seq))
        
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

occupations: list[Noun] = []

def loadOccupations():
    with io.open('data/occupations.txt', encoding='utf-8') as f:
        data = f.readlines()
        data = data[2:] # todo `header`
        
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
        
        header.parseHeader(SpeechPart.noun, data[:headerLines])
        
        # read data
        data = data[headerLines+1:]
        data = ConvertLinesToTokens(data)

        noun = Noun()
        noun.forms = []

        if len(data):
            noun.title = data[0].split('/')[0]

        for wordPair in data:
            words = wordPair.split('/')
            rus = words[0]
            serb = words[1]

            form = header.yieldDeclination()
            if form == None:
                occupations.append(noun)

                # new Noun
                noun = Noun()
                noun.forms = []
                noun.title = rus

                header.resetYield()
                form = header.yieldDeclination()
            
            word = Word()
            word.declination = form
            word.rus = rus
            word.serb = serb
            
            noun.forms.append(word)
         
        occupations.append(noun)
        noun = Noun()
        noun.forms = {}
        
        for occ in occupations:
            print(occ.toString())

'''         
pronoun = Pronoun()

def loadPronouns():
    with io.open('data/pronouns.txt', encoding='utf-8') as f:
        data = f.readlines()
        data = data[2:] # todo `fixed`
                
        # read data
        data = ConvertLinesToTokens(data)

        pronoun = Pronoun()
        
        for word in data:
            if pronoun.orig == None:
                pronoun.orig = word
                continue
                
         
        occupations.append(pronoun)
        pronoun = pronoun()
        pronoun.forms = {}
        
        for p in pronouns:
            print(p.toString())
'''
            
loadOccupations()
#loadPronouns()