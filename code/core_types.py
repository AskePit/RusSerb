from enum import Enum
import copy

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

    def getOpposite(self):
        if self.value == 0:
            return Person.second
        if self.value == 1:
            return Person.first
        return Person.third

class Declination:
    speechPart: SpeechPart
    
    person: Person
    gender: Gender
    number: Number
    case: Case

    def __eq__(self, other: object) -> bool:
        for a in ['person', 'gender', 'number', 'case']:
            if hasattr(other, a) and hasattr(self, a):
                if getattr(self, a) != getattr(other, a):
                    return False

        return True
    
    def setSpeechPart(self, speechPart):
        self.speechPart = speechPart
        return self

    def setPerson(self, person):
        self.person = person
        return self

    def setGender(self, gender):
        self.gender = gender
        return self

    def setNumber(self, number):
        self.number = number
        return self

    def setCase(self, case):
        self.case = case
        return self

    def Make(speechPart: SpeechPart, form: str):
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

class DeclinedWord:
    declination: Declination
    rus: str
    serb: str

    def Make(declination, rus, serb):
        res = Declination()
        res.declination = declination
        res.rus = rus
        res.serb = serb
        return res

class Word:
    speechPart: SpeechPart
    title: str
    forms: list[DeclinedWord]
    
    def Make(speechPart: SpeechPart):
        res = Word()
        res.speechPart = speechPart
        res.forms = []
        res.title = ""
        return res

    def MakeTitled(speechPart: SpeechPart, title: str):
        res = Word.Make(speechPart)
        res.title = title
        return res

    def get(self, declination: Declination):
        for word in self.forms:
            if word.declination == declination:
                return word
        return None

    def toString(self):
        res = self.speechPart.name + ' ' + self.title + '\n'
        for word in self.forms:
            res = res + word.declination.toString() + ': ' + word.rus + '/' + word.serb +'\n'
        return res
    
    def normalize(self):
        # unwrap Gender.unisex to 3 genders

        new_forms: list[DeclinedWord] = []

        for f in self.forms:
            if hasattr(f.declination, 'gender') and f.declination.gender == Gender.unisex:
                for gender in [Gender.male, Gender.fem, Gender.neu]:
                    new_form = copy.deepcopy(f)
                    new_form.declination.gender = gender
                    new_forms.append(new_form)

        self.forms = self.forms + new_forms

class WordList:
    words: list[Word]

    def __init__(self):
        self.words = []
    
    def toString(self):
        res = ""
        for word in self.words:
            res = res + word.toString() + '\n'
        
        return res

class Phrase:
    rus: str
    serb: str

    def __init__(self, rus, serb):
        self.rus = rus
        self.serb = serb

    def toString(self):
        return self.rus + '/' + self.serb

class PhrasesList:    
    title: str = ''
    phrases: list[Phrase] = []

    def toString(self):
        res = ''
        for phrase in self.phrases:
            res = res + phrase.toString() + '\n'
        return res