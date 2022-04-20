from code.excercise_types import *

def ToBeEx() -> ExcerciseYield:
    # title:    Переведите на сербский:
    # question: Я студент (student)
    # answer:   Ja sam student

    # title:    Переведите на сербский:
    # question: Вы не пенсионерки (penzionerke)
    # answer:   Vi niste penzionerke

    decl = Declination.Make('male|fem & first|second|third & sing|plur & nom')

    occupation = random.choice(GetVocabulary('occupations').words)
    negative = random.randint(0, 1)
    pronoun = GetVocabulary('personal_pronouns').get(decl)
    tb = [GetVocabulary('tobe'), GetVocabulary('negative_tobe')][negative].get(decl)
    occ = occupation.get(decl)

    title = 'Переведите на сербский'
    rusNoParticle = [' ', ' не '][negative] 
    question = pronoun.rus.capitalize() + rusNoParticle + occ.rus + ' (' + occ.serb + ').'
    answer = pronoun.serb.capitalize() + ' ' + tb.serb + ' ' + occ.serb + '.'

    return ExcerciseYield(title, question, answer)

def ToBeEx2() -> ExcerciseYield:
    # title:    Переведите на сербский в форме `Da li ...?`
    # question: Ты студент (student)?
    # answer:   Da li si ti student?

    # title:    Переведите на сербский в форме `Je.. li ...?`
    # question: Вы врачи (lekari)?
    # answer:   Jeste li vi lekari?

    decl = Declination.Make('male|fem & first|second|third & sing|plur & nom')

    occupation = random.choice(GetVocabulary('occupations').words)
    form = random.randint(0, 1)
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
    # title:    Ответьте на вопрос в короткой форме:
    # question: Ты студент (student)?
    # answer:   Jesam

    # title:    Ответьте на вопрос в полной форме:
    # question: Вы врачи (lekari)?
    # answer:   Mi smo lekari

    qDecl = Declination.Make('male|fem & first|second|third & sing|plur & nom')
    aDecl = copy.deepcopy(qDecl).mirrorPerson()

    #print(qDecl.toString())
    #print(aDecl.toString())

    occupation = random.choice(GetVocabulary('occupations').words)
    form = random.randint(0, 1)
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
