from code.load import *
import random

LoadVocabulary()

# shortcuts
occupations       = vocabulary['occupations']
personal_pronouns = vocabulary['personal_pronouns']
tobe              = vocabulary['tobe']
positive_tobe     = vocabulary['positive_tobe']
negative_tobe     = vocabulary['negative_tobe']
question_tobe     = vocabulary['question_tobe']

def IsExit(anykey):
    return anykey == 'q' or anykey == 'Q' or anykey == 'й' or anykey == 'Й'

def ClrScr():
    os.system('clear')

class ExcerciseYield:
    title: str
    question: str
    answer: str

    def __init__(self, title, q, a):
        self.title = title
        self.question = q
        self.answer = a

def ToBeEx():
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
    occupation = random.choice(occupations.words)
    negative = random.randint(0, 1)

    decl = Declination()\
        .setCase(Case.nom)\
        .setPerson(person)\
        .setGender(gender)\
        .setNumber(number)

    #print(decl.toString())

    pronoun = personal_pronouns.get(decl)
    tb = [tobe, negative_tobe][negative].get(decl)
    occ = occupation.get(decl)

    title = 'Переведите на сербский'
    rusNoParticle = [' ', ' не '][negative] 
    question = pronoun.rus.title() + rusNoParticle + occ.rus + ' (' + occ.serb + ').'
    answer = pronoun.serb.title() + ' ' + tb.serb + ' ' + occ.serb + '.'

    return ExcerciseYield(title, question, answer)

def ToBeEx2():
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
    occupation = random.choice(occupations.words)
    form = random.randint(0, 1)

    decl = Declination()\
        .setCase(Case.nom)\
        .setPerson(person)\
        .setGender(gender)\
        .setNumber(number)

    #print(decl.toString())

    pronoun = personal_pronouns.get(decl)
    tb = [tobe, question_tobe][form].get(decl)
    occ = occupation.get(decl)

    title = [
        'Переведите на сербский в форме `Da li ...?`',
        'Переведите на сербский в форме `Je.. li ...?`'
    ][form]
    question = pronoun.rus.title() + ' ' + occ.rus + ' (' + occ.serb + ')?'

    if form == 0:
        answer = 'Da li ' + tb.serb + ' ' + pronoun.serb + ' ' + occ.serb + '?'
    else:
        answer = tb.serb.title() + ' li ' + pronoun.serb + ' ' + occ.serb + '?'

    return ExcerciseYield(title, question, answer)

def ToBeEx3():
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
    occupation = random.choice(occupations.words)
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

    qPronoun = personal_pronouns.get(qDecl)
    aPronoun = personal_pronouns.get(aDecl)
    aTb = [positive_tobe, tobe][form].get(aDecl)
    occ = occupation.get(aDecl)

    title = [
        'Ответьте на вопрос в короткой форме',
        'Ответьте на вопрос в полной форме'
    ][form]
    question = qPronoun.rus.title() + ' ' + occ.rus + ' (' + occ.serb + ')?'

    if form == 0:
        answer = aTb.serb.title() + '.'
    else:
        answer = aPronoun.serb.title() + ' ' + aTb.serb + ' ' + occ.serb + '.'

    return ExcerciseYield(title, question, answer)

PAD = '  '

def ExecuteExcercise(exFunc):
    while True:
        exYield: ExcerciseYield = exFunc()

        ClrScr()
        print('\n' + PAD + '.........................\n')
        print(PAD + exYield.title + ':\n')
        print(PAD + exYield.question, end='')

        ans = input()

        if IsExit(ans):
            break
        else:
            print(PAD + exYield.answer)
            print('\n' + PAD + '.........................\n')
            ans = input()
            if IsExit(ans):
                break

def main():
    while True:
        ClrScr()
        print('\n' + PAD + '.........................\n')
        print(PAD + 'Выберите упражнение:')
        print(PAD + '1. To be')
        print(PAD + '2. To be вопросы')
        print(PAD + '3. To be ответы')
        print(PAD + 'q. Выход')
        
        ans = input()
        if IsExit(ans):
            break
        elif ans == '1':
            ExecuteExcercise(ToBeEx)
        elif ans == '2':
            ExecuteExcercise(ToBeEx2)
        elif ans == '3':
            ExecuteExcercise(ToBeEx3)
        else:
            continue

if __name__ == "__main__":
    main()