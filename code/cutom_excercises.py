from msilib.schema import IniFile
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
    randomAdjectivesPool: RandomPool

    def __init__(self):
        super().__init__()
        self.randomNounsPool = RandomPool(GetVocabulary('nouns').words)
        self.randomAdjectivesPool = RandomPool(GetVocabulary('random_adjectives').words)

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

        noun = self.randomNounsPool.yieldElem().makeNounGenderPair(Case.nom, num, distance, Person.third)
        adj = self.randomAdjectivesPool.yieldElem().makeSimilarPair(noun)
        point = GetVocabulary('pointing_pronouns').makeSimilarPair(noun)
        tobe = GetVocabulary('tobe').makeSimilarPair(noun)

        possessDecl = noun.serbDeclination.clone().override(random.choice(list(Number)), random.choice(list(Gender)))
        possess = GetVocabulary('possessive_pronouns').getWord(possessDecl).makeSimilarPair(noun)

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

class ImatiEx(Excercise):
    randomNounsPool: RandomPool
    imati: Word

    def __init__(self):
        super().__init__()
        self.imati = GetVocabulary('imati')
        self.randomNounsPool = RandomPool(GetVocabulary('nouns').words)

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
                if verb.metaDeclination.intersects(conj):
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

class PerfectPositiveEx(Excercise):
    randomVerbsPool: RandomPool
    randomOccupationsPool: RandomPool

    def __init__(self):
        super().__init__()

        # combine verbs and modal_verbs and exclude `treba`
        l = GetVocabulary('verbs').words + GetVocabulary('modal_verbs').words
        l = [w for w in l if w.title != 'treba']

        self.randomVerbsPool = RandomPool(l)
        self.randomOccupationsPool = RandomPool(GetVocabulary('occupations').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский с местоимением:
        # question: Я читал.
        # answer:   Ja sam čitao.

        # title:    Переведите на сербский без местоимения:
        # question: Я читал.
        # answer:   Čitao sam.

        form = random.randint(0, 1)
        negative = random.randint(0, 1)
        withOccupation = random.randint(0, 10) > 7

        decl = Declination.Parse('perfect & male|fem|neu & first|second|third & sing|plur & nom')

        if withOccupation:
            decl.parseOverride('male|fem & third')
            subject = self.randomOccupationsPool.yieldElem().get(decl)
        else:
            decl.humanizeNeutral()
            subject = GetVocabulary('personal_pronouns').getWordForm(decl)

        tb = [GetVocabulary('tobe'), GetVocabulary('negative_tobe')][negative].get(decl)
        verb = self.randomVerbsPool.yieldElem().get(decl)

        title = 'Переведите на сербский' if withOccupation else ['Переведите на сербский с местоимением', 'Переведите на сербский без местоимения'][form]

        needClarify = decl.number == Number.plur
        clarification = ''
        if needClarify:
            if decl.gender == Gender.male:
                clarification = '(муж.)'
            elif decl.gender == Gender.fem:
                clarification = '(жен.)'
            elif decl.gender == Gender.neu:
                clarification = '(ср.)'

        question = '{}{}{}{}.'.format(subject.rus.capitalize(), clarification,  [' ', ' не '][negative], verb.rus)
        if form == 0 or withOccupation:
            answer = '{} {} {}.'.format(subject.serb.capitalize(), tb.serb, verb.serb)
        else:
            if negative:
                answer = '{} {}.'.format(tb.serb.capitalize(), verb.serb)
            else:
                answer = '{} {}.'.format(verb.serb.capitalize(), tb.serb)

        return ExcerciseYield(title, question, answer)

class PerfectQuestionsEx(Excercise):
    randomVerbsPool: RandomPool
    randomOccupationsPool: RandomPool

    def __init__(self):
        super().__init__()

        # combine verbs and modal_verbs and exclude `treba`
        l = GetVocabulary('verbs').words + GetVocabulary('modal_verbs').words
        l = [w for w in l if w.title != 'treba']

        self.randomVerbsPool = RandomPool(l)
        self.randomOccupationsPool = RandomPool(GetVocabulary('occupations').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский в форме `Da li ...`:
        # question: Вы пришли?
        # answer:   Da li ste došli?

        # title:    Переведите на сербский в форме `Je.. li ...?`:
        # question: Вы пришли?
        # answer:   Jeste li došli?

        form = random.randint(0, 1)
        withOccupation = random.randint(0, 10) > 7

        decl = Declination.Parse('perfect & male|fem|neu & first|second|third & sing|plur & nom')

        if withOccupation:
            decl.parseOverride('male|fem & third')
            subject = self.randomOccupationsPool.yieldElem().get(decl)
        else:
            decl.humanizeNeutral()
            subject = GetVocabulary('personal_pronouns').getWordForm(decl)

        tb = GetVocabulary(['tobe', 'question_tobe'][form]).get(decl)
        verb = self.randomVerbsPool.yieldElem().get(decl)

        title = ['Переведите на сербский в форме `Da li ...?`', 'Переведите на сербский в форме `Je.. li ...?`'][form]

        needClarify = decl.number == Number.plur
        clarification = ''
        if needClarify:
            if decl.gender == Gender.male:
                clarification = '(муж.)'
            elif decl.gender == Gender.fem:
                clarification = '(жен.)'
            elif decl.gender == Gender.neu:
                clarification = '(ср.)'

        question = '{}{} {}?'.format(subject.rus.capitalize(), clarification, verb.rus)
        if form == 0:
            if withOccupation:
                answer = 'Da li {} {} {}?'.format(tb.serb, subject.serb, verb.serb)
            else:
                answer = 'Da li {} {}?'.format(tb.serb, verb.serb)
        else:
            if withOccupation:
                answer = '{} li {} {}?'.format(tb.serb.capitalize(), subject.serb, verb.serb)
            else:
                answer = '{} li {}?'.format(tb.serb.capitalize(), verb.serb)

        return ExcerciseYield(title, question, answer)

class FuturPositiveEx(Excercise):
    randomVerbsPool: RandomPool

    def __init__(self):
        super().__init__()

        # combine verbs and modal_verbs and exclude `treba`
        l = GetVocabulary('verbs').words + GetVocabulary('modal_verbs').words
        l = [w for w in l if w.title != 'treba']

        self.randomVerbsPool = RandomPool(l)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский в форме `[Местоимение] [ću] [глагол]`:
        # question: Я буду читать.
        # answer:   Ja ću čitati.

        # title:    Переведите на сербский в форме `[Глагол]`:
        # question: Я буду читать.
        # answer:   Čitaću.

        # title:    Переведите на сербский в форме `[Местоимение] [ću] da [глагол]`:
        # question: Я буду читать.
        # answer:   Ja ću da čitam.

        CU_INF = 0
        ONE_WORD = 1
        CU_DA = 2
        NEGATIVE = 3

        form = random.randint(0, 3)

        decl = Declination.Parse('present & male|fem|neu & first|second|third & sing|plur & nom')

        decl.humanizeNeutral()
        pronoun = GetVocabulary('personal_pronouns').getWordForm(decl)

        cu = GetVocabulary(['cu', 'necu'][form == NEGATIVE]).get(decl)
        verbWord = self.randomVerbsPool.yieldElem()

        title = [
            'Переведите на сербский в форме `[Местоимение] [ću] [глагол]`',
            'Переведите на сербский в форме `[Глагол]`',
            'Переведите на сербский в форме `[Местоимение] [ću] da [глагол]`',
            'Переведите на сербский'
        ][form]

        needClarify = decl.number == Number.plur
        clarification = ''
        if needClarify:
            if decl.gender == Gender.male:
                clarification = '(муж.)'
            elif decl.gender == Gender.fem:
                clarification = '(жен.)'
            elif decl.gender == Gender.neu:
                clarification = '(ср.)'

        question = '{}{} {} {}.'.format(pronoun.rus.capitalize(), clarification, cu.rus, verbWord.get(Infinitive).rus)

        if form == CU_INF or form == NEGATIVE:
            verb = verbWord.get(Infinitive)
            answer = '{} {} {}.'.format(pronoun.serb.capitalize(), cu.serb, verb.serb)
        elif form == ONE_WORD:
            verb = verbWord.get(decl.clone().override(Time.futur))
            answer = verb.serb.capitalize()
        elif form == CU_DA:
            verb = verbWord.get(decl)
            answer = '{} {} da {}.'.format(pronoun.serb.capitalize(), cu.serb, verb.serb)

        return ExcerciseYield(title, question, answer)

class FuturQuestionsEx(Excercise):
    randomVerbsPool: RandomPool
    hteti: Word

    def __init__(self):
        super().__init__()

        # combine verbs and modal_verbs and exclude `treba`
        l = GetVocabulary('verbs').words + GetVocabulary('modal_verbs').words
        l = [w for w in l if w.title != 'treba']

        self.randomVerbsPool = RandomPool(l)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский в форме `Da li [ću] ...`:
        # question: Ты придешь?
        # answer:   Da li ćeš doći?

        # title:    Переведите на сербский в форме `[Hoću] li ...?`:
        # question: Ты придешь?
        # answer:   Hoćeš li doći?

        form = random.randint(0, 1)

        decl = Declination.Parse('present & male|fem|neu & first|second|third & sing|plur & nom')

        decl.humanizeNeutral()
        pronoun = GetVocabulary('personal_pronouns').getWordForm(decl)

        cu = GetVocabulary(['cu', 'hocu'][form]).get(decl)
        verb = self.randomVerbsPool.yieldElem().get(Infinitive)

        title = [
            'Переведите на сербский в форме `Da li [ću] ...`',
            'Переведите на сербский в форме `[Hoću] li ...?`'
        ][form]

        question = '{} {} {}?'.format(pronoun.rus.capitalize(), cu.rus, verb.rus)
        if form == 0:
            answer = 'Da li {} {}?'.format(cu.serb, verb.serb)
        else:
            answer = '{} li {}?'.format(cu.serb.capitalize(), verb.serb)

        return ExcerciseYield(title, question, answer)
