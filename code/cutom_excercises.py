from code.excercise_types import *

class ToBeEx(Excercise):
    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Я студент (student)
        # answer:   Ja sam student

        # title:    Переведите на сербский:
        # question: Вы не пенсионерки (penzionerke)
        # answer:   Vi niste penzionerke

        decl = Declination.Make('male|fem & first|second|third & sing|plur & nom')

        occupation = random.choice(GetVocabulary('occupations').words)
        negative = random.randint(0, 1)
        pronoun = GetVocabulary('personal_pronouns').getWordForm(decl)
        tb = [GetVocabulary('tobe'), GetVocabulary('negative_tobe')][negative].get(decl)
        occ = occupation.get(decl)

        title = 'Переведите на сербский'
        rusNoParticle = [' ', ' не '][negative]
        question = '{}{}{} ({}).'.format(pronoun.rus.capitalize(), rusNoParticle, occ.rus, occ.serb)
        answer = '{} {} {}.'.format(pronoun.serb.capitalize(), tb.serb, occ.serb)

        return ExcerciseYield(title, question, answer)

class ToBeEx2(Excercise):
    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский в форме `Da li ...?`
        # question: Ты студент (student)?
        # answer:   Da li si ti student?

        # title:    Переведите на сербский в форме `Je.. li ...?`
        # question: Вы врачи (lekari)?
        # answer:   Jeste li vi lekari?

        decl = Declination.Make('male|fem & first|second|third & sing|plur & nom')

        occupation = random.choice(GetVocabulary('occupations').words)
        form = random.randint(0, 1)
        pronoun = GetVocabulary('personal_pronouns').getWordForm(decl)
        tb = [GetVocabulary('tobe'), GetVocabulary('question_tobe')][form].get(decl)
        occ = occupation.get(decl)

        title = [
            'Переведите на сербский в форме `Da li ...?`',
            'Переведите на сербский в форме `Je.. li ...?`'
        ][form]
        question = '{} {} ({})?'.format(pronoun.rus.capitalize(), occ.rus, occ.serb)

        if form == 0:
            answer = 'Da li {} {} {}?'.format(tb.serb, pronoun.serb, occ.serb)
        else:
            answer = '{} li {} {}?'.format(tb.serb.capitalize(), pronoun.serb, occ.serb)

        return ExcerciseYield(title, question, answer)

class ToBeEx3(Excercise):
    def __call__(self) -> ExcerciseYield:
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
        qPronoun = GetVocabulary('personal_pronouns').getWordForm(qDecl)
        aPronoun = GetVocabulary('personal_pronouns').getWordForm(aDecl)
        aTb = [GetVocabulary('positive_tobe'), GetVocabulary('tobe')][form].get(aDecl)
        occ = occupation.get(aDecl)

        title = [
            'Ответьте на вопрос в короткой форме',
            'Ответьте на вопрос в полной форме'
        ][form]
        question = '{} {} ({})?'.format(qPronoun.rus.capitalize(), occ.rus, occ.serb)

        if form == 0:
            answer = aTb.serb.capitalize() + '.'
        else:
            answer = '{} {} {}.'.format(aPronoun.serb.capitalize(), aTb.serb, occ.serb)

        return ExcerciseYield(title, question, answer)

class NumbersGeneratorEx(Excercise):
    def __call__(self) -> ExcerciseYield:
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

        # 11 12 13 14 15 16 17 18 19 are special
        # and have their own word for both 10 and 1 ranks
        if num10 == 10:
            num10 += num1
            num1 = 0

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
                        answer += ' '
                    else:
                        nonFirstWord = True
                    answer += numDict[n]

        return ExcerciseYield(title, question, answer)

class PointingEx(Excercise):
    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Эта умная кошка моя
        # answer:   Ta pametna mačka je moja

        # title:    Переведите на русский:
        # question: To crveno vino je tvoje 
        # answer:   То красное вино твое

        lang = random.randint(0, 1)

        num = random.choice(list(Number))
        distance = random.choice(list(Distance))

        nounGen = random.choice(GetVocabulary('random_nouns').words)
        gender = nounGen.metaDeclination.gender

        decl = Declination.Make('{} & {} & {} & {} & {}'.format(gender.name, Case.nom.name, num.name, distance.name, Person.third.name))
        noun = nounGen.get(decl)
        adj = random.choice(GetVocabulary('random_adjectives').words).get(decl)

        point = GetVocabulary('pointing_pronouns').getWordForm(decl)

        tobe = GetVocabulary('tobe').get(decl)

        possessDecl = copy.deepcopy(decl)
        possessDecl.number = random.choice(list(Number))
        possessDecl.gender = random.choice(list(Gender))
        possess = GetVocabulary('possessive_pronouns').getWord(possessDecl).get(decl)

        distClarif = ''
        if distance == Distance.far:
            distClarif = '(близ.)'
        elif distance == Distance.off:
            distClarif = '(дальн.)'

        title = ['Переведите на сербский', 'Переведите на русский'][lang]
        question = '{}{} {} {} - {}.'.format(point.rus.capitalize(), distClarif, adj.rus, noun.rus, possess.rus)
        answer = '{} {} {} {} {}.'.format(point.serb.capitalize(), adj.serb, noun.serb, tobe.serb, possess.serb)

        if lang:
            question, answer = answer, question

        return ExcerciseYield(title, question, answer)