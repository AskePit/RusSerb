from code.core_types import *
import random

class LangMode(Enum):
    rusSerb = 0,
    serbRus = 1,
    random = 2

    def GetLangBit():
        if LANG_MODE == LangMode.rusSerb:
            return 0
        elif LANG_MODE == LangMode.serbRus:
            return 1
        else:
            return random.randint(0, 1)

LANG_MODE = LangMode.rusSerb

# NOTE: each excercise should return `ExcerciseYield` object

class ExcerciseYield:
    title: str
    question: str
    answer: str

    def __init__(self, title, q, a):
        self.title = title
        self.question = q
        self.answer = a

class ExcerciseType(Enum):
    phrases = 0
    custom = 1

class ExcerciseDesc:
    name: str
    parent = None # ExcercisesDir
    serialNumber: int
    type: ExcerciseType

    def __init__(self):
        self.name = ''
        self.parent = None
    
    def MakePhrasesEx(name: str, voc: str, parent, number: int):
        ex = ExcerciseDesc()
        ex.name = name
        ex.parent = parent
        ex.serialNumber = number
        ex.type = ExcerciseType.phrases
        ex.phrasesVoc = voc
        return ex

    def MakeCustomEx(name: str, funcNames: list[str], parent, number: int):
        ex = ExcerciseDesc()
        ex.name = name
        ex.parent = parent
        ex.serialNumber = number
        ex.type = ExcerciseType.custom
        ex.customFunctions = funcNames
        return ex

    def toString(self):
        res = 'parent: ' + (self.parent.name if self.parent != None else '<None>') + '\n'
        res = self.name
        if self.type == ExcerciseType.phrases:
            res += ' <-> ' + self.phrasesVoc
        elif self.type == ExcerciseType.custom:
            res += ' <-> ' + self.customFunctions
        return res

class ExcerciseDescsDir:
    name: str
    parent = None # ExcercisesDir
    serialNumber: int
    children = [] # list[ExcercisesDir]
    excercises = [] # list[Excercise]

    def __init__(self, parent, number: int):
        self.name = ''
        self.parent = parent
        self.serialNumber = number
        self.children = []
        self.excercises = []
    
    def toString(self):
        res = self.name + '\n'
        res += 'parent: ' + (self.parent.name if self.parent != None else '<None>') + '\n'
        for ex in self.excercises:
            res += '\n  ' + ex.toString()
        for ch in self.children:
            res += '\n' + ch.toString()
        return res

class RandomPool:
    origList: list
    pool: list[int]
    lastIndex: int = None

    def __init__(self, origList):
        self.origList = origList
        self.refill()
    
    def refill(self):
        self.pool = list(range(0, len(self.origList)))
        random.shuffle(self.pool)
        if self.lastIndex and self.pool[-1] == self.lastIndex:
            self.pool[-1], self.pool[0] = self.pool[0], self.pool[-1]

    def yieldElem(self):
        if len(self.pool) == 0:
            self.refill()
        
        self.lastIndex = self.pool.pop()
        return self.origList[self.lastIndex]

class Excercise:
    def __call__(self) -> ExcerciseYield:
        return ExcerciseYield()

# generic for every phrases vocabulary
class PhrasesEx(Excercise):
    phrases: list[Phrase]
    randomPool: RandomPool

    def __init__(self, vocabularyTopic: str):
        super().__init__()

        lists: list[PhrasesList] = []
        vocs = vocabularyTopic.split(' ')

        for voc in vocs:
            lists.append(GetVocabulary(voc.strip()))
        
        self.phrases = PhrasesList.Merge(lists).phrases
        self.randomPool = RandomPool(self.phrases)

    def yieldRandomPhrase(self):
        phraseIndex = self.randomPool.yieldIndex()
        return self.phrases[phraseIndex]

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Доброе утро
        # answer:   Dobro jutro

        # title:    Переведите на русский:
        # question: Vrlo dobro
        # answer:   Очень хорошо

        lang = LangMode.GetLangBit()
        phrase = self.randomPool.yieldElem()

        rus = phrase.rus.capitalize()
        serb = phrase.serb.capitalize()

        title = ['Переведите на сербский', 'Переведите на русский'][lang]
        question = [rus, serb][lang]
        answer = [serb, rus][lang]

        return ExcerciseYield(title, question, answer)
