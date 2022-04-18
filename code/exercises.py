from code.core_types import *
import random

class ExcerciseYield:
    title: str
    question: str
    answer: str

    def __init__(self, title, q, a):
        self.title = title
        self.question = q
        self.answer = a

def ToBeEx() -> ExcerciseYield:
    # Переведите на сербский:
    # Я студент (student)
    # Ja sam student

    # Переведите на сербский:
    # Вы не пенсионерки (penzionerke)
    # Vi niste penzionerke

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

def ToBeEx2() -> ExcerciseYield:
    # Переведите на сербский в форме `Da li ...?`
    # Ты студент (student)?
    # Da li si ti student?

    # Переведите на сербский в форме `Je.. li ...?`
    # Вы врачи (lekari)?
    # Jeste li vi lekari?

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

def ToBeEx3() -> ExcerciseYield:
    # Ответьте на вопрос в короткой форме:
    # Ты студент (student)?
    # Jesam

    # Ответьте на вопрос в полной форме:
    # Вы врачи (lekari)?
    # Mi smo lekari

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

def GreetingsEx() -> ExcerciseYield:
    # Переведите на сербский:
    # доброе утро
    # dobro jutro

    # Переведите на русский:
    # vrlo dobro
    # очень хорошо

    lang = random.randint(0, 1)
    greeting = GetVocabulary('greetings').phrases[random.randint(0, len(GetVocabulary('greetings').phrases)-1)]

    rus = greeting.rus.capitalize()
    serb = greeting.serb.capitalize()

    title = ['Переведите на сербский', 'Переведите на русский'][lang]
    question = [rus, serb][lang]
    answer = [serb, rus][lang]

    return ExcerciseYield(title, question, answer)
