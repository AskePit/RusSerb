from code.excercise_types import *

class ToBeEx(Excercise):
    randomOccupationsPool: RandomPool

    def __init__(self):
        super().__init__()
        self.randomOccupationsPool = RandomPool(GetVocabulary('occupations').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Я студент (student)
        # answer:   Ja sam student

        # title:    Переведите на сербский:
        # question: Вы не пенсионерки (penzionerke)
        # answer:   Vi niste penzionerke

        decl = Declination.Parse('male|fem & first|second|third & sing|plur & nom')

        occupation = self.randomOccupationsPool.yieldElem()
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
    randomOccupationsPool: RandomPool

    def __init__(self):
        super().__init__()
        self.randomOccupationsPool = RandomPool(GetVocabulary('occupations').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский в форме `Da li ...?`
        # question: Ты студент (student)?
        # answer:   Da li si ti student?

        # title:    Переведите на сербский в форме `Je.. li ...?`
        # question: Вы врачи (lekari)?
        # answer:   Jeste li vi lekari?

        decl = Declination.Parse('male|fem & first|second|third & sing|plur & nom')

        occupation = self.randomOccupationsPool.yieldElem()
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
    randomOccupationsPool: RandomPool

    def __init__(self):
        super().__init__()
        self.randomOccupationsPool = RandomPool(GetVocabulary('occupations').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Ответьте на вопрос в короткой форме:
        # question: Ты студент (student)?
        # answer:   Jesam

        # title:    Ответьте на вопрос в полной форме:
        # question: Вы врачи (lekari)?
        # answer:   Mi smo lekari

        qDecl = Declination.Parse('male|fem & first|second|third & sing|plur & nom')
        aDecl = qDecl.clone().mirrorPerson()

        #print(qDecl.toString())
        #print(aDecl.toString())

        occupation = self.randomOccupationsPool.yieldElem()
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
    numDict: dict[int, str]
    usedPool: list[int]
    
    def __init__(self):
        super().__init__()

        self.usedPool = []
        self.numDict = {}

        for n in GetVocabulary('numbers').phrases:
            self.numDict[int(n.aux)] = n.serb

    def yieldNumber(self) -> tuple[int, str]:
        while True:
            be1000 = random.randint(0, 1)
            be100 = random.randint(0, 1)
            be10 = random.randint(0, 1)
            be1 = random.randint(0, 1)

            num1000 = (random.randint(1, 9) if be1000 else 0)*1000
            num100 = (random.randint(1, 9) if be100 else 0)*100
            num10 = (random.randint(1, 9) if be10 else 0)*10
            num1 = random.randint(1, 9) if be1 else 0

            number = num1000 + num100 + num10 + num1
            if number in self.usedPool:
                # interrupt and generate number again
                continue
            break

        # 11 12 13 14 15 16 17 18 19 are special
        # and have their own word for both 10 and 1 ranks
        if num10 == 10:
            num10 += num1
            num1 = 0

        if len(self.usedPool) >= 256:
            self.usedPool.clear()

        self.usedPool.append(number)

        numberStr = ''
        if number == 0:
            numberStr = self.numDict[number]
        else:
            nonFirstWord = False

            for n in [num1000, num100, num10, num1]:
                if n > 0:
                    if nonFirstWord:
                        numberStr += ' '
                    else:
                        nonFirstWord = True
                    numberStr += self.numDict[n]

        return (number, numberStr)

    def __call__(self) -> ExcerciseYield:
        # title:    Напишите число на сербском:
        # question: 2 804
        # answer:   dve hiljade osamsto četiri

        # title:    Напишите число на сербском:
        # question: 61
        # answer:   šezdeset jedan

        number, answer = self.yieldNumber()

        title = 'Напишите число на сербском'
        question = str(number)

        return ExcerciseYield(title, question, answer)

class PointingEx(Excercise):
    randomNounsPool: RandomPool

    def __init__(self):
        super().__init__()
        self.randomNounsPool = RandomPool(GetVocabulary('random_nouns').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Эта умная кошка моя
        # answer:   Ta pametna mačka je moja

        # title:    Переведите на русский:
        # question: Taj veliki kukuruz je njihov
        # answer:   Та большая кукуруза - их

        lang = LangMode.GetLangBit()

        num = random.choice(list(Number))
        distance = random.choice(list(Distance))

        nounGen = self.randomNounsPool.yieldElem()
        serbGender = nounGen.metaDeclination.gender
        rusGender = nounGen.metaDeclination.ruGender

        serbDecl = Declination.Make(serbGender, Case.nom, num, distance, Person.third)
        rusDecl = serbDecl.clone().override(rusGender.toGender())

        noun = nounGen.get(serbDecl)
        adj = random.choice(GetVocabulary('random_adjectives').words)
        serbAdj = adj.get(serbDecl)
        rusAdj = adj.get(rusDecl)

        point = GetVocabulary('pointing_pronouns')
        serbPoint = point.getWordForm(serbDecl)
        rusPoint = point.getWordForm(rusDecl)

        tobe = GetVocabulary('tobe').get(serbDecl)

        possessDecl = serbDecl.clone().override(random.choice(list(Number)), random.choice(list(Gender)))
        possess = GetVocabulary('possessive_pronouns').getWord(possessDecl).get(serbDecl)

        distClarif = ''
        if distance == Distance.far:
            distClarif = '(близ.)'
        elif distance == Distance.off:
            distClarif = '(дальн.)'

        title = ['Переведите на сербский', 'Переведите на русский'][lang]
        question = '{}{} {} {} - {}.'.format(rusPoint.rus.capitalize(), distClarif, rusAdj.rus, noun.rus, possess.rus)
        answer = '{} {} {} {} {}.'.format(serbPoint.serb.capitalize(), serbAdj.serb, noun.serb, tobe.serb, possess.serb)

        if lang:
            question, answer = answer, question

        return ExcerciseYield(title, question, answer)

class ImatiEx(Excercise):
    randomNounsPool: RandomPool
    imati: Word

    def __init__(self):
        super().__init__()
        self.imati = GetVocabulary('imati')
        self.randomNounsPool = RandomPool(GetVocabulary('random_nouns').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: У вас нет кошки
        # answer:   Nemate mačku

        # title:    Переведите на сербский:
        # question: У неё есть брат
        # answer:   Ima brata

        negative = random.randint(0, 1)

        rusPronounDecl = Declination.Parse('male|fem|neu & first|second|third & sing|plur & gen')
        serbImatiDecl = rusPronounDecl.clone().parseOverride('nom & present')

        serbNounDecl = Declination.Parse('sing|plur & aku')
        rusNounDecl = serbNounDecl.clone().override(Case.gen if negative else Case.nom)

        nounNonDeclined = self.randomNounsPool.yieldElem()

        rusPronoun = GetVocabulary('personal_pronouns').getWordForm(rusPronounDecl)
        rusNoun = nounNonDeclined.get(rusNounDecl)

        serbImati = self.imati.get(serbImatiDecl)
        serbNoun = nounNonDeclined.get(serbNounDecl)

        rusPronounCorrected = rusPronoun.rus
        if rusPronounCorrected == 'их' or rusPronounCorrected == 'его' or rusPronounCorrected == 'её':
            rusPronounCorrected = 'н' + rusPronounCorrected
        
        imatiCorrected = serbImati.serb
        if negative:
            imatiCorrected = imatiCorrected[1:]
            imatiCorrected = 'ne' + imatiCorrected

        title = 'Переведите на сербский'
        rusParticle = ['есть', 'нет'][negative]
        question = 'У {} {} {}.'.format(rusPronounCorrected, rusParticle, rusNoun.rus)
        answer = '{} {}.'.format(imatiCorrected.capitalize(), serbNoun.serb)

        return ExcerciseYield(title, question, answer)

class VerbsEx(Excercise):
    verbsList: list[Word]
    randomVerbsPool: RandomPool

    def __init__(self, verbTypes: str): # verbTypes: `a`, `i`, `e`, `a | e | i` etc
        super().__init__()

        conjDecls = Declination.ParseList(verbTypes)

        self.verbsList = []

        for verb in GetVocabulary('verbs').words:
            for conj in conjDecls:
                if verb.metaDeclination == conj:
                    self.verbsList.append(verb)

        self.randomVerbsPool = RandomPool(self.verbsList)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Я бегу
        # answer:   Ja trčim

        # title:    Переведите на сербский:
        # question: Они не читают
        # answer:   Oni ne čitaju

        negative = random.randint(0, 1)

        decl = Declination.Parse('present & male|fem|neu & first|second|third & sing|plur & nom')
        pronoun = GetVocabulary('personal_pronouns').getWordForm(decl)
        verb = self.randomVerbsPool.yieldElem().get(decl)

        title = 'Переведите на сербский'
        question = '{}{}{}.'.format(pronoun.rus.capitalize(), [' ', ' не '][negative], verb.rus)
        answer = '{}{}{}.'.format(pronoun.serb.capitalize(), [' ', ' ne '][negative], verb.serb)

        return ExcerciseYield(title, question, answer)

class AVerbsEx(VerbsEx):
    def __init__(self):
        super().__init__('a')

class IVerbsEx(VerbsEx):
    def __init__(self):
        super().__init__('i')

class EVerbsEx(VerbsEx):
    def __init__(self):
        super().__init__('e')

class AIEVerbsEx(VerbsEx):
    def __init__(self):
        super().__init__('a | i | e')

class ModalVerbsEx(Excercise):
    randomModalVerbsPool: RandomPool
    randomVerbsPool: RandomPool

    def __init__(self):
        super().__init__()
        self.randomModalVerbsPool = RandomPool(GetVocabulary('modal_verbs').words)
        self.randomVerbsPool = RandomPool(GetVocabulary('verbs').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Я должен читать
        # answer:   Ja moram da čitam

        negative = random.randint(0, 1)

        decl = Declination.Parse('present & male|fem|neu & first|second|third & sing|plur & nom')
        pronouns = GetVocabulary('personal_pronouns')
        modal = self.randomModalVerbsPool.yieldElem().get(decl)

        verb = self.randomVerbsPool.yieldElem()
        serbVerb = verb.get(decl)
        rusVerb = verb.get(Infinitive)

        if modal.serb == 'treba':
            dative = decl.clone().parseOverride('dat')
            rusPronoun = pronouns.getWordForm(dative)
        else:
            rusPronoun = pronouns.getWordForm(decl)

        title = 'Переведите на сербский'

        question = '{}{}{} {}.'.format(rusPronoun.rus.capitalize(), [' ', ' не '][negative], modal.rus, rusVerb.rus)
        answer = '{}{} da {}.'.format(['', 'Ne '][negative], [modal.serb.capitalize(), modal.serb][negative], serbVerb.serb)

        return ExcerciseYield(title, question, answer)