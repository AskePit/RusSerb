from enum import Enum
import copy
import random

class SpeechPart(Enum):
    noun      = 0 # существительное
    pronoun   = 1 # местоимение
    tobe      = 2 # быть
    verb      = 3 # глагол
    adjective = 4 # прилагательное
    adverb    = 5 # наречие
    particle  = 6 # частица

class ExclusiveForm(Enum):
    inf = 0 # infinitive

class Gender(Enum):
    male   = 0 # male
    fem    = 1 # feminitive
    neu    = 2 # neutral
    unisex = 3 # all genders

class RuGender(Enum):
    ru_male   = 0 # male
    ru_fem    = 1 # feminitive
    ru_neu    = 2 # neutral
    
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

class Person(Enum):
    first  = 0 # первое лицо
    second = 1 # второе лицо
    third  = 2 # третье лицо

    def getOpposite(self):
        if self.value == 0:
            return Person.second
        if self.value == 1:
            return Person.first
        return Person.third

class Time(Enum):
    present   = 0
    perfect   = 1
    imperfect = 2
    aorist    = 3
    futur     = 4

    def isPresent(self):
        return self.value == 0
    
    def isPast(self):
        return self.value == 1 or self.value == 2 or self.value == 3

    def isFuture(self):
        return self.value == 4

class Distance(Enum):
    close = 0 # этот
    far   = 1 # тот
    off   = 2 # тот очень далекий

class VerbConjugation(Enum):
    a = 0
    i = 1
    e = 2

DeclinationAttributesMap = {
    'person': Person,
    'gender': Gender,
    'ruGender': RuGender,
    'number': Number,
    'case': Case,
    'distance': Distance,
    'exclusive': ExclusiveForm,
    'time': Time,
    'verbConjugation': VerbConjugation
}

class Declination:
    # possible fields:
    # any key from `DeclinationAttributesMap`

    def __eq__(self, other: object) -> bool:
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
    
    def mirrorPerson(self):
        if hasattr(self, 'person') and self.person != None:
            self.person = self.person.getOpposite()
        return self

    # male|fem & first|second|third & sing|plur & nom
    # & is for combination
    # | is for random probability
    def Make(form: str): # Declination
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

        return res

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
    def MakeList(form: str): # list[Declination]
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
            res.append(decl)
            
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

    def isInfinitive(self) -> bool:
        return hasattr(self, 'exclusive') and self.exclusive == ExclusiveForm.inf
    
    def toString(self):
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
    metaDeclination: Declination
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

    def get(self, declination: Declination) -> DeclinedWord:
        for word in self.forms:
            if word.declination == declination:
                return word
        return None

    def toString(self):
        res = '{} {}\n'.format(self.speechPart.name, self.title)
        res += '{}\n'.format(self.metaDeclination.toString())
        for word in self.forms:
            res += '{}: {}|{}\n'.format(word.declination.toString(), word.rus, word.serb)
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

        self.forms += new_forms

class WordList:
    words: list[Word]

    def __init__(self):
        self.words = []
    
    def toString(self):
        res = ""
        for word in self.words:
            res += word.toString() + '\n'
        
        return res
    
    def getWordByKey(self, key: str):
        for w in self.words:
            if w.title == key:
                return w
        return None

    def getWord(self, declination: Declination) -> Word:
        for word in self.words:
            if word.metaDeclination == declination:
                return word
        return None

    def getWordForm(self, declination: Declination) -> DeclinedWord:
        for word in self.words:
            if word.metaDeclination == declination:
                return word.get(declination)
        return None

    def tryUnwrap(self) -> Word:
        if len(self.words) == 1:
            return self.words[0]
        else:
            return None

class Phrase:
    rus: str
    serb: str
    aux: str

    def __init__(self, rus, serb, aux=None):
        self.rus = rus
        self.serb = serb
        if not aux is None:
            self.aux = aux

    def toString(self):
        res = self.rus + '|' + self.serb
        if hasattr(self, 'aux'):
            res += '|' + self.aux
        return res

class PhrasesList:    
    title: str = ''
    phrases: list[Phrase] = []

    def __init__(self):
        self.title = ""
        self.phrases = []

    def toString(self):
        res = ''
        for phrase in self.phrases:
            res += phrase.toString() + '\n'
        return res
    
    def Merge(lists): # PhrasesList
        res = PhrasesList()
        for l in lists:
            res.phrases.extend(l.phrases)
        return res

vocabulary = {}

def GetVocabulary(name: str):
    return vocabulary[name]
