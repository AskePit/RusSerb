from dataclasses import dataclass
from enum import Enum
import copy
import random

class SpeechPart(Enum):
    noun        = 0 # существительное
    pronoun     = 1 # местоимение
    tobe        = 2 # быть
    verb        = 3 # глагол
    adjective   = 4 # прилагательное
    preposition = 5 # предлог
    conjunction = 6 # союз
    adverb      = 7 # наречие
    particle    = 8 # частица

class ExclusiveForm(Enum):
    inf    = 0 # infinitive
    unique = 1 # единственная/уникальная форма

class Gender(Enum):
    male   = 0 # male
    fem    = 1 # feminitive
    neu    = 2 # neutral
    unisex = 3 # all genders

    def toRuGender(self):
        return RuGender(self.value)

class RuGender(Enum):
    ru_male   = 0 # male
    ru_fem    = 1 # feminitive
    ru_neu    = 2 # neutral
    ru_unisex = 3 # all genders

    def toGender(self) -> Gender:
        return Gender(self.value)
    
class Number(Enum):
    sing = 0 # singular / ед.ч.
    plur = 1 # plural   / мн.ч.
    
class Case(Enum):
    nom  = 0 # nominative   / именительный
    gen  = 1 # genitive     / родительный
    dat  = 2 # dative       / дательный
    aku  = 3 # akuzative    / винительный
    vok  = 4 # vokative     / ---
    inst = 5 # instrumental / творительный
    lok  = 6 # lokative     / предложный

    def __str__(self):
        return self.name.capitalize()

class Person(Enum):
    first  = 0 # первое лицо
    second = 1 # второе лицо
    third  = 2 # третье лицо

    def getOpposite(self):
        if self == Person.first:
            return Person.second
        if self == Person.second:
            return Person.first
        return Person.third

class Time(Enum):
    present   = 0
    perfect   = 1
    imperfect = 2
    aorist    = 3
    futur     = 4

    def isPresent(self):
        return self == Time.present
    
    def isPast(self):
        return self == Time.perfect or self == Time.imperfectmperf or self == Time.aorist

    def isFuture(self):
        return self.value == Time.futur

class Distance(Enum):
    close = 0 # этот
    far   = 1 # тот
    off   = 2 # тот очень далекий

class VerbConjugation(Enum):
    a = 0
    i = 1
    e = 2

class Reflexiveness(Enum):
    no_se = 0
    opt_se = 1
    se = 2

class Definition(Enum):
    indef = 0
    defined = 1
    comp = 2
    super = 3

class Animality(Enum):
    anim = 0
    inanim = 1

DeclinationAttributesMap = {
    'person': Person,
    'gender': Gender,
    'ruGender': RuGender,
    'number': Number,
    'case': Case,
    'distance': Distance,
    'exclusive': ExclusiveForm,
    'time': Time,
    'conjugation': VerbConjugation,
    'reflexiveness': Reflexiveness,
    'definition': Definition,
    'animality': Animality,
}

class Declination:
    # possible fields:
    # any key from `DeclinationAttributesMap`
    
    def getAttrs(self):
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    # male|fem & first|second|third & sing|plur & nom
    # & is for combination
    # | is for random probability
    def Parse(form: str) -> 'Declination':
        res = Declination()

        components = form.split('&')

        for component in components:
            variants = component.split('|')
            choice = random.choice(variants).strip()

            got = False
            for attrName, E in DeclinationAttributesMap.items():
                try:
                    setattr(res, attrName, E[choice])
                except:
                    pass
                else:
                    got = True
                    break
        
            if not got:
                raise Exception("Could not parse Declination {}!".format(form))

        return res.normalize()

    # male|fem & first & sing|plur & nom
    # & is for combination
    # | is for variability
    # result list:
    #     male & first & sing & nom
    #     fem  & first & sing & nom
    #     male & first & plur & nom
    #     fem  & first & plur & nom
    #
    # unisex expands to male|fem|neu
    def ParseList(form: str) -> 'list[Declination]':
        res: list[Declination] = []

        attrs = {} # <AttrName, list[AttrEnum]>
        components = form.split('&')

        for component in components:
            variants = component.split('|')
            
            for variant in variants:
                variant = variant.strip()
                got = False

                for attrName, E in DeclinationAttributesMap.items():
                    try:
                        val = E[variant]
                        attrs.setdefault(attrName, [])
                        attrs[attrName].append(val)
                    except:
                        pass
                    else:
                        got = True
                        break
                    pass

                if not got:
                    raise Exception("Could not parse Declination {}!".format(form))
        
        if 'gender' in attrs:
            genders = attrs['gender']
            if Gender.unisex in genders:
                genders.remove(Gender.unisex)
                genders.append(Gender.male)
                genders.append(Gender.fem)
                genders.append(Gender.neu)
        
        comb_list: list[int] = []
        for a in attrs:
            comb_list.append(0)
        
        while True:
            # form declination
            decl: Declination = Declination()

            i = 0
            for a, vals in attrs.items():
                val = DeclinationAttributesMap[a](vals[comb_list[i]])
                setattr(decl, a, val)
                
                i += 1
            
            # append declination
            res.append(decl.normalize())
            
            # yield another combination
            i = 0
            for a, vals in attrs.items():
                exit = True

                if comb_list[i] == len(vals) - 1:
                    comb_list[i] = 0
                    exit = False
                else:
                    comb_list[i] = comb_list[i] + 1

                if exit:
                    break

                i += 1
            
            if i == len(comb_list):
                break

        return res
    
    def Make(*argv) -> 'Declination':
        res = Declination()

        for arg in argv:
            got = False
            for attrName, E in DeclinationAttributesMap.items():
                if isinstance(arg, E):
                    setattr(res, attrName, arg)
                    got = True
                    break
        
            if not got:
                raise Exception("Could not set variable {}!".format(arg))
        return res.normalize()

    def clone(self):
        return copy.deepcopy(self)

    def overrideByDelc(self, overrideDecl):
        for a in DeclinationAttributesMap:
            if hasattr(overrideDecl, a):
                setattr(self, a, getattr(overrideDecl, a))
        return self.normalize()
    
    def override(self, *overrideArgs):
        declOverride = Declination.Make(*overrideArgs)
        return self.overrideByDelc(declOverride)

    def parseOverride(self, overrideForm: str):
        declOverride = Declination.Parse(overrideForm)
        return self.overrideByDelc(declOverride)

    def isInfinitive(self) -> bool:
        return hasattr(self, 'exclusive') and self.exclusive == ExclusiveForm.inf

    def isSimilarTo(self, other: object) -> bool:
        for attrName in DeclinationAttributesMap:
            if hasattr(self, attrName) != hasattr(other, attrName):
                return False
        return True
    
    def isEqualTo(self, other: object) -> bool:
        if not self.isSimilarTo(other):
            return False
        
        for attr in self.getAttrs():
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def intersects(self, other: object) -> bool:
        for a in DeclinationAttributesMap:
            if hasattr(other, a) and hasattr(self, a):
                if getattr(self, a) != getattr(other, a):
                    if a == 'gender' and (getattr(self, a) == Gender.unisex or getattr(other, a) == Gender.unisex):
                        pass
                    else:
                        return False

        if hasattr(self, 'exclusive'):
            if not hasattr(other, 'exclusive'):
                return False
            elif getattr(self, 'exclusive') != getattr(other, 'exclusive'):
                return False

        return True
    
    def includes(self, other) -> bool:
        for attr in self.getAttrs():
            if not hasattr(other, attr):
                return False

            if getattr(self, attr) != getattr(other, attr):
                return False
        return True
    
    def isIncludedIn(self, other) -> bool:
        return other.includes(self)
    
    def normalize(self):
        #return self

        # cleanup None
        for a in DeclinationAttributesMap:
            if hasattr(self, a) and getattr(self, a) == None:
                delattr(self, a)
        
        # exclusive case
        if hasattr(self, 'exclusive'):
            for a in DeclinationAttributesMap:
                if a == 'exclusive':
                    continue
                if hasattr(self, a):
                    delattr(self, a)
        
        # gender and ruGender case
        if hasattr(self, 'ruGender') and not hasattr(self, 'gender'):
            setattr(self, 'gender', getattr(self, 'ruGender').toGender())
        return self
    
    def mirrorPerson(self):
        if hasattr(self, 'person') and self.person != None:
            self.person = self.person.getOpposite()
        return self

    def humanizeNeutral(self, gender=None):
        hasPerson = hasattr(self, 'person') and self.person != None
        hasGender = hasattr(self, 'gender') and self.gender != None

        if hasPerson and hasGender:
            if self.person != Person.third:
                if gender == None:
                    self.gender = random.choice([Gender.male, Gender.fem])
                else:
                    self.gender = gender

        return self
    
    def __str__(self) -> str:
        first = True
        res = ""

        for a in DeclinationAttributesMap:
            if hasattr(self, a):
                if first:
                    first = False
                else:
                    res += ' & '
                res += getattr(self, a).name
        return res

Infinitive = Declination.Parse('inf')

def GetRusReflexive(rusWord: str, decl: Declination):
    if rusWord.endswith('сь') or rusWord.endswith('ся'):
        return rusWord
    
    if hasattr(decl, 'number') and hasattr(decl, 'person'):
        firstSing  = decl.person == Person.first  and decl.number == Number.sing
        secondPlur = decl.person == Person.second and decl.number == Number.plur

        if firstSing or secondPlur:
            return rusWord + 'сь'

    return rusWord + 'ся'

def GetSerbReflexive(decl: Declination):
    if hasattr(decl, 'reflexiveness'):
        if decl.reflexiveness == Reflexiveness.no_se:
            return ''
        
        return 'se'
    
    return ''

# exact declination of `Word` in both languages
@dataclass
class WordForm:
    meta: 'Word'
    declination: Declination
    rus: str
    serb: str

    def getRusReflexive(self, reflection: bool):
        if not reflection:
            return self.rus

        if self.getSerbReflexive(reflection) == '':
            return self.rus
        return GetRusReflexive(self.rus, self.declination)
    
    def getSerbReflexive(self, reflection: bool):
        return GetSerbReflexive(self.meta.metaDeclination) if reflection else ''

# pair of serb and rus words in two different declinations
# stores deep copies of declinations and strings, so you can play
# with it as you like
class WordBiForm:
    word: 'Word'

    commonDecl: Declination
    serbOnlyDecl: Declination
    rusOnlyDecl: Declination

    rusCache: str = None
    serbCache: str = None

    def MakeFromNoun(noun: 'Word', commonDecl: Declination) -> 'WordBiForm':
        if noun.speechPart != SpeechPart.noun:
            return None
        
        if not hasattr(noun.metaDeclination, 'gender'):
            return None

        res = WordBiForm()

        res.word = noun
        res.commonDecl = commonDecl

        nounMeta = res.word.metaDeclination

        if not hasattr(nounMeta, 'ruGender'):
            nounMeta.ruGender = nounMeta.gender.toRuGender()

        res.serbOnlyDecl = Declination.Make(nounMeta.gender)
        res.rusOnlyDecl = Declination.Make(nounMeta.ruGender.toGender())

        return res
    
    def clone(self):
        return copy.deepcopy(self)
    
    def setWord(self, word: 'Word') -> 'WordBiForm':
        self.word = word
        self.invalidateCache()
        return self
    
    def rus(self) -> str:
        if self.rusCache == None:
            rusDecl = self.commonDecl.clone().overrideByDelc(self.rusOnlyDecl)
            self.rusCache = self.word.get(rusDecl).rus
        return self.rusCache
    
    def serb(self) -> str:
        if self.serbCache == None:
            serbDecl = self.commonDecl.clone().overrideByDelc(self.serbOnlyDecl)
            self.serbCache = self.word.get(serbDecl).serb
        return self.serbCache
    
    def invalidateCache(self):
        self.rusCache = None
        self.serbCache = None

class Word:
    speechPart: SpeechPart
    title: str
    metaDeclination: Declination
    forms: list[WordForm]
    
    def __init__(self, speechPart: SpeechPart):
        self.speechPart = speechPart
        self.forms = []
        self.title = ""

    def get(self, declination: Declination) -> WordForm:
        for word in self.forms:
            if word.declination.intersects(declination):
                return word
        return None

    def __str__(self):
        res = '{} {}\n'.format(self.speechPart.name, self.title)
        res += '{}\n'.format(self.metaDeclination)
        for word in self.forms:
            res += '{}: {}|{}\n'.format(word.declination, word.serb, word.rus)
        return res
    
    def normalize(self):
        # unwrap Gender.unisex to 3 genders

        new_forms: list[WordForm] = []

        for f in self.forms:
            if hasattr(f.declination, 'gender') and f.declination.gender == Gender.unisex:
                for gender in [Gender.male, Gender.fem, Gender.neu]:
                    new_form = copy.deepcopy(f)
                    new_form.declination.gender = gender
                    new_forms.append(new_form)

        self.forms += new_forms
    
class WordList:
    words: list[Word]

    def __init__(self):
        self.words = []
    
    def __str__(self):
        res = ""
        for word in self.words:
            res += str(word) + '\n'
        
        return res
    
    def getWordByKey(self, key: str):
        for w in self.words:
            if w.title == key:
                return w
        return None

    def getWord(self, declination: Declination) -> Word:
        for word in self.words:
            if word.metaDeclination.intersects(declination):
                return word
        return None

    def getWordForm(self, declination: Declination) -> WordForm:
        for word in self.words:
            if word.metaDeclination.intersects(declination):
                return word.get(declination)
        return None
    
    def tryUnwrap(self) -> Word:
        if len(self.words) == 1:
            return self.words[0]
        else:
            return None

class Phrase:
    rus: str|list[str]
    serb: str|list[str]
    aux: str

    def __init__(self, rus='', serb='', aux=None):
        self.rus = rus
        self.serb = serb
        if not aux is None:
            self.aux = aux

    def __str__(self):
        res = self.serb + '|' + self.rus
        if hasattr(self, 'aux'):
            res += '|' + self.aux
        return 
    
    def normalize(self):
        if type(self.rus) is list and len(self.rus) == 1:
            self.rus = self.rus[0]
        if type(self.serb) is list and len(self.serb) == 1:
            self.serb = self.serb[0]

class PhrasesList:    
    title: str = ''
    phrases: list[Phrase] = []

    def __init__(self):
        self.title = ""
        self.phrases = []

    def __str__(self):
        res = ''
        for phrase in self.phrases:
            res += str(phrase) + '\n'
        return res
    
    def Merge(lists) -> 'PhrasesList':
        res = PhrasesList()
        for l in lists:
            res.phrases.extend(l.phrases)
        return res

vocabulary = {}

def GetVocabulary(name: str):
    return vocabulary[name]
