from code.core_types import *
import random

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

class Excercise:
    name: str
    parent = None # ExcercisesDir
    type: ExcerciseType

    def __init__(self):
        self.name = ''
        self.parent = None
    
    def MakePhrasesEx(name: str, voc: str, parent):
        ex = Excercise()
        ex.name = name
        ex.parent = parent
        ex.type = ExcerciseType.phrases
        ex.phrasesVoc = voc
        return ex

    def MakeCustomEx(name: str, funcName, parent):
        ex = Excercise()
        ex.name = name
        ex.parent = parent
        ex.type = ExcerciseType.custom
        ex.customFunction = funcName
        return ex

    def toString(self):
        res = 'parent: ' + (self.parent.name if self.parent != None else '<None>') + '\n'
        res = self.name
        if self.type == ExcerciseType.phrases:
            res = res + ' <-> ' + self.phrasesVoc
        elif self.type == ExcerciseType.custom:
            res = res + ' <-> ' + self.customFunction
        return res

class ExcercisesDir:
    name: str
    parent = None # ExcercisesDir
    children = [] # list[ExcercisesDir]
    excercises = [] # list[Excercise]

    def __init__(self, parent):
        self.name = ''
        self.parent = parent
        self.children = []
        self.excercises = []
    
    def toString(self):
        res = self.name + '\n'
        res = res + 'parent: ' + (self.parent.name if self.parent != None else '<None>') + '\n'
        for ex in self.excercises:
            res = res + '\n  ' + ex.toString()
        for ch in self.children:
            res = res + '\n' + ch.toString()
        return res

# generic for every phrases vocabulary
def PhrasesEx(vocabularyTopic: str) -> ExcerciseYield:
    # title:    Переведите на сербский:
    # question: Доброе утро
    # answer:   Dobro jutro

    # title:    Переведите на русский:
    # question: Vrlo dobro
    # answer:   Очень хорошо

    lang = random.randint(0, 1)
    phrases = GetVocabulary(vocabularyTopic).phrases
    greetingIndex = random.randint(0, len(phrases)-1)
    greeting = phrases[greetingIndex]

    rus = greeting.rus.capitalize()
    serb = greeting.serb.capitalize()

    title = ['Переведите на сербский', 'Переведите на русский'][lang]
    question = [rus, serb][lang]
    answer = [serb, rus][lang]

    return ExcerciseYield(title, question, answer)
    