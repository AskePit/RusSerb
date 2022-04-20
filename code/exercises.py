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

ExcerciseName = str
excercises_old: list[(str, ExcerciseName)] = []

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

def RegExcercise(funcName: str, name: ExcerciseName):
    excercises_old.append((funcName, name))

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

def ToBeEx() -> ExcerciseYield:
    # title:    Переведите на сербский:
    # question: Я студент (student)
    # answer:   Ja sam student

    # title:    Переведите на сербский:
    # question: Вы не пенсионерки (penzionerke)
    # answer:   Vi niste penzionerke

    gendersMaleFemale = list(Gender)
    gendersMaleFemale.remove(Gender.unisex)
    gendersMaleFemale.remove(Gender.neu)

    person = random.choice(list(Person))
    gender = random.choice(gendersMaleFemale)
    number = random.choice(list(Number))
    occupation = random.choice(GetVocabulary('occupations').words)
    negative = random.randint(0, 1)

    decl = Declination()\
        .setCase(Case.nom)\
        .setPerson(person)\
        .setGender(gender)\
        .setNumber(number)

    #print(decl.toString())

    pronoun = GetVocabulary('personal_pronouns').get(decl)
    tb = [GetVocabulary('tobe'), GetVocabulary('negative_tobe')][negative].get(decl)
    occ = occupation.get(decl)

    title = 'Переведите на сербский'
    rusNoParticle = [' ', ' не '][negative] 
    question = pronoun.rus.capitalize() + rusNoParticle + occ.rus + ' (' + occ.serb + ').'
    answer = pronoun.serb.capitalize() + ' ' + tb.serb + ' ' + occ.serb + '.'

    return ExcerciseYield(title, question, answer)
RegExcercise('ToBeEx', 'To be')

def ToBeEx2() -> ExcerciseYield:
    # title:    Переведите на сербский в форме `Da li ...?`
    # question: Ты студент (student)?
    # answer:   Da li si ti student?

    # title:    Переведите на сербский в форме `Je.. li ...?`
    # question: Вы врачи (lekari)?
    # answer:   Jeste li vi lekari?

    gendersMaleFemale = list(Gender)
    gendersMaleFemale.remove(Gender.unisex)
    gendersMaleFemale.remove(Gender.neu)

    person = random.choice(list(Person))
    gender = random.choice(gendersMaleFemale)
    number = random.choice(list(Number))
    occupation = random.choice(GetVocabulary('occupations').words)
    form = random.randint(0, 1)

    decl = Declination()\
        .setCase(Case.nom)\
        .setPerson(person)\
        .setGender(gender)\
        .setNumber(number)

    #print(decl.toString())

    pronoun = GetVocabulary('personal_pronouns').get(decl)
    tb = [GetVocabulary('tobe'), GetVocabulary('question_tobe')][form].get(decl)
    occ = occupation.get(decl)

    title = [
        'Переведите на сербский в форме `Da li ...?`',
        'Переведите на сербский в форме `Je.. li ...?`'
    ][form]
    question = pronoun.rus.capitalize() + ' ' + occ.rus + ' (' + occ.serb + ')?'

    if form == 0:
        answer = 'Da li ' + tb.serb + ' ' + pronoun.serb + ' ' + occ.serb + '?'
    else:
        answer = tb.serb.capitalize() + ' li ' + pronoun.serb + ' ' + occ.serb + '?'

    return ExcerciseYield(title, question, answer)
RegExcercise('ToBeEx2', 'To be вопросы')

def ToBeEx3() -> ExcerciseYield:
    # title:    Ответьте на вопрос в короткой форме:
    # question: Ты студент (student)?
    # answer:   Jesam

    # title:    Ответьте на вопрос в полной форме:
    # question: Вы врачи (lekari)?
    # answer:   Mi smo lekari

    gendersMaleFemale = list(Gender)
    gendersMaleFemale.remove(Gender.unisex)
    gendersMaleFemale.remove(Gender.neu)

    qPerson = random.choice(list(Person))
    aPerson = qPerson.getOpposite()
    gender = random.choice(gendersMaleFemale)
    number = random.choice(list(Number))
    occupation = random.choice(GetVocabulary('occupations').words)
    form = random.randint(0, 1)

    qDecl = Declination()\
        .setCase(Case.nom)\
        .setPerson(qPerson)\
        .setGender(gender)\
        .setNumber(number)

    aDecl = Declination()\
        .setCase(Case.nom)\
        .setPerson(aPerson)\
        .setGender(gender)\
        .setNumber(number)

    #print(decl.toString())

    qPronoun = GetVocabulary('personal_pronouns').get(qDecl)
    aPronoun = GetVocabulary('personal_pronouns').get(aDecl)
    aTb = [GetVocabulary('positive_tobe'), GetVocabulary('tobe')][form].get(aDecl)
    occ = occupation.get(aDecl)

    title = [
        'Ответьте на вопрос в короткой форме',
        'Ответьте на вопрос в полной форме'
    ][form]
    question = qPronoun.rus.capitalize() + ' ' + occ.rus + ' (' + occ.serb + ')?'

    if form == 0:
        answer = aTb.serb.capitalize() + '.'
    else:
        answer = aPronoun.serb.capitalize() + ' ' + aTb.serb + ' ' + occ.serb + '.'

    return ExcerciseYield(title, question, answer)
RegExcercise('ToBeEx3', 'To be ответы')

def GreetingsEx() -> ExcerciseYield:
    return PhrasesEx('greetings')
RegExcercise('GreetingsEx', 'Фразы приветствия')

def CafeEx() -> ExcerciseYield:
    return PhrasesEx('cafe')
RegExcercise('CafeEx', 'Кафе')

def TimeEx() -> ExcerciseYield:
    return PhrasesEx('time')
RegExcercise('TimeEx', 'Время')

def NumbersEx() -> ExcerciseYield:
    return PhrasesEx('numbers')
RegExcercise('NumbersEx', 'Числа')

def NumbersGeneratorEx() -> ExcerciseYield:
    # title:    Напишите число на сербском:
    # question: 2 804
    # answer:   dve hiljade osamsto četiri

    # title:    Напишите число на сербском:
    # question: 61
    # answer:   šezdeset jedan

    numDict: dict[int, str] = {}
    for n in GetVocabulary('numbers').phrases:
        numDict[int(n.aux)] = n.serb
    
    be1000 = random.randint(0, 1)
    be100 = random.randint(0, 1)
    be10 = random.randint(0, 1)
    be1 = random.randint(0, 1)

    num1000 = (random.randint(1, 9) if be1000 else 0)*1000
    num100 = (random.randint(1, 9) if be100 else 0)*100
    num10 = (random.randint(1, 9) if be10 else 0)*10
    num1 = random.randint(1, 9) if be1 else 0

    number = num1000 + num100 + num10 + num1

    title = 'Напишите число на сербском'
    question = str(number)

    answer = ''
    if number == 0:
        answer = numDict[number]
    else:
        nonFirstWord = False

        for n in [num1000, num100, num10, num1]:
            if n > 0:
                if nonFirstWord:
                    answer = answer + ' '
                else:
                    nonFirstWord = True
                answer = answer + numDict[n]

    return ExcerciseYield(title, question, answer)
RegExcercise('NumbersGeneratorEx', 'Генератор чисел')