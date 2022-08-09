from ast import Num
from msilib.schema import IniFile
from typing import Callable
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
        question = '{}{}{} ({})'.format(pronoun.rus, rusNoParticle, occ.rus, occ.serb)

        answer = []
        if negative:
            answer = '({}) {} {}'.format(pronoun.serb, tb.serb, occ.serb)
        else:
            answer.append('{} {} {}'.format(pronoun.serb, tb.serb, occ.serb))
            answer.append('{} {}'.format(occ.serb, tb.serb))

        return ExcerciseYield(title, question, answer)

class ToBeEx2(Excercise):
    randomOccupationsPool: RandomPool

    def __init__(self):
        super().__init__()
        self.randomOccupationsPool = RandomPool(GetVocabulary('occupations').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Ты студент (student)?
        # answer:   Da li si (ti) student?
        # answer:   Jesi li (ti) student?

        decl = Declination.Parse('male|fem & first|second|third & sing|plur & nom')

        occupation = self.randomOccupationsPool.yieldElem()
        pronoun = GetVocabulary('personal_pronouns').getWordForm(decl)
        
        occ = occupation.get(decl)

        title = 'Переведите на сербский'
        question = '{} {} ({})?'.format(pronoun.rus, occ.rus, occ.serb)

        answer = []
        tb = GetVocabulary('tobe').get(decl)
        answer.append('Da li {} ({}) {}?'.format(tb.serb, pronoun.serb, occ.serb))

        tb = GetVocabulary('question_tobe').get(decl)
        answer.append('{} li ({}) {}?'.format(tb.serb, pronoun.serb, occ.serb))

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

        occupation = self.randomOccupationsPool.yieldElem()
        qPronoun = GetVocabulary('personal_pronouns').getWordForm(qDecl)
        aPronoun = GetVocabulary('personal_pronouns').getWordForm(aDecl)
        
        occ = occupation.get(aDecl)

        title = 'Ответьте на вопрос'
        question = '{} {} ({})?'.format(qPronoun.rus, occ.rus, occ.serb)

        answer = []
        aTb = GetVocabulary('positive_tobe').get(aDecl)
        answer.append(aTb.serb + '')
        aTb = GetVocabulary('tobe').get(aDecl)
        answer.append('{} {} {}'.format(aPronoun.serb, aTb.serb, occ.serb))

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
        self.randomAdjectivesPool = RandomPool(GetVocabulary('adjectives').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Эта умная кошка моя
        # answer:   Ta pametna mačka je moja

        # title:    Переведите на русский:
        # question: Taj veliki kukuruz je njihov
        # answer:   Та большая кукуруза - их

        lang = LangMode.GetLangBit()

        num = RandomEnum(Number)
        distance = RandomEnum(Distance)

        subjDecl = Declination.Make(Case.nom, num, distance, Person.third, Definition.defined)

        noun = WordBiForm.MakeFromNoun(self.randomNounsPool.yieldElem(), subjDecl)
        adj = noun.clone().setWord(self.randomAdjectivesPool.yieldElem())
        point = noun.clone().setWord(GetVocabulary('pointing_pronouns').getWord(Declination.Make(distance)))
        tobe = noun.clone().setWord(GetVocabulary('tobe'))

        possessDecl = Declination.Make(RandomEnum(Number), RandomEnum(Gender), RandomEnum(Person))
        possess = noun.clone().setWord(GetVocabulary('possessive_pronouns').getWord(possessDecl))

        distClarif = ''
        if distance == Distance.far:
            distClarif = '(близ.)'
        elif distance == Distance.off:
            distClarif = '(дальн.)'

        title = ['Переведите на сербский', 'Переведите на русский'][lang]
        question = '{}{} {} {} - {}'.format(point.rus(), distClarif, adj.rus(), noun.rus(), possess.rus())
        answer = '{} {} {} {} {}'.format(point.serb(), adj.serb(), noun.serb(), tobe.serb(), possess.serb())

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
        question = 'У {} {} {}'.format(rusPronounCorrected, rusParticle, rusNoun.rus)
        answer = '{} {}'.format(imatiCorrected, serbNoun.serb)

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
        question = '{}{}{}'.format(pronoun.rus, [' ', ' не '][negative], verb.rus)
        answer = '{}{}{}'.format(pronoun.serb, [' ', ' ne '][negative], verb.serb)

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

        question = '{}{}{} {}'.format(rusPronoun.rus, [' ', ' не '][negative], modal.rus, rusVerb.rus)
        answer = '{}{} da {}'.format(['', 'Ne '][negative], [modal.serb, modal.serb][negative], serbVerb.serb)

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
        #           Čitao sam.

        negative = random.randint(0, 1)
        withOccupation = RandomPercent(30)

        decl = Declination.Parse('perfect & male|fem|neu & first|second|third & sing|plur & nom')

        if withOccupation:
            decl.parseOverride('male|fem & third')
            subject = self.randomOccupationsPool.yieldElem().get(decl)
        else:
            decl.humanizeNeutral()
            subject = GetVocabulary('personal_pronouns').getWordForm(decl)

        tb = [GetVocabulary('tobe'), GetVocabulary('negative_tobe')][negative].get(decl)
        verb = self.randomVerbsPool.yieldElem().get(decl)

        title = 'Переведите на сербский'

        needClarify = decl.number == Number.plur
        clarification = ''
        if needClarify:
            if decl.gender == Gender.male:
                clarification = '(муж.)'
            elif decl.gender == Gender.fem:
                clarification = '(жен.)'
            elif decl.gender == Gender.neu:
                clarification = '(ср.)'

        question = '{}{}{}{}'.format(subject.rus, clarification,  [' ', ' не '][negative], verb.rus)

        if withOccupation:
            answer = '{} {} {}'.format(subject.serb, tb.serb, verb.serb)
        else:
            answer = []
            answer.append('{} {} {}'.format(subject.serb, tb.serb, verb.serb))
            if negative:
                answer.append('{} {}'.format(tb.serb, verb.serb))
            else:
                answer.append('{} {}'.format(verb.serb, tb.serb))

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
        #           Jeste li došli?

        withOccupation = RandomPercent(30)

        decl = Declination.Parse('perfect & male|fem|neu & first|second|third & sing|plur & nom')

        if withOccupation:
            decl.parseOverride('male|fem & third')
            subject = self.randomOccupationsPool.yieldElem().get(decl)
        else:
            decl.humanizeNeutral()
            subject = GetVocabulary('personal_pronouns').getWordForm(decl)

        
        verb = self.randomVerbsPool.yieldElem().get(decl)

        title = 'Переведите на сербский'

        needClarify = decl.number == Number.plur
        clarification = ''
        if needClarify:
            if decl.gender == Gender.male:
                clarification = '(муж.)'
            elif decl.gender == Gender.fem:
                clarification = '(жен.)'
            elif decl.gender == Gender.neu:
                clarification = '(ср.)'

        question = '{}{} {}?'.format(subject.rus, clarification, verb.rus)

        answer = []

        tb = GetVocabulary('tobe').get(decl)
        if withOccupation:
            answer.append('Da li {} {} {}?'.format(tb.serb, subject.serb, verb.serb))
        else:
            answer.append('Da li {} {}?'.format(tb.serb, verb.serb))

        tb = GetVocabulary('question_tobe').get(decl)
        if withOccupation:
            answer.append('{} li {} {}?'.format(tb.serb, subject.serb, verb.serb))
        else:
            answer.append('{} li {}?'.format(tb.serb, verb.serb))

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
        # title:    Переведите на сербский:
        # question: Я буду читать.
        # answer:   Čitaću.
        #           Ja ću čitati.
        #           Ja ću da čitam.

        # title:    Переведите на сербский:
        # question: Я не буду читать.
        # answer:   (Ja) neću čitati.
        #           (Ja) neću da čitam.

        negative = random.randint(0, 1)

        decl = Declination.Parse('present & male|fem|neu & first|second|third & sing|plur & nom')

        decl.humanizeNeutral()
        pronoun = GetVocabulary('personal_pronouns').getWordForm(decl)

        cu = GetVocabulary(['cu', 'necu'][negative]).get(decl)
        verbWord = self.randomVerbsPool.yieldElem()
        selfness = random.randint(0, 1)

        title = 'Переведите на сербский'

        needClarify = decl.number == Number.plur
        clarification = ''
        if needClarify:
            if decl.gender == Gender.male:
                clarification = '(муж.)'
            elif decl.gender == Gender.fem:
                clarification = '(жен.)'
            elif decl.gender == Gender.neu:
                clarification = '(ср.)'

        question = '{}{} {} {}'.format(pronoun.rus, clarification, cu.rus, verbWord.get(Infinitive).getRusReflexive(selfness))

        answer = []

        if not negative:
            verb = verbWord.get(decl.clone().override(Time.futur))
            answer.append('{} {}'.format(verb.serb, verb.getSerbReflexive(selfness)))

            verb = verbWord.get(Infinitive)
            answer.append('{} {} {} {}'.format(pronoun.serb, cu.serb, verb.getSerbReflexive(selfness), verb.serb))
            
            verb = verbWord.get(decl)
            answer.append('{} {} {} da {}'.format(pronoun.serb, cu.serb, verb.getSerbReflexive(selfness), verb.serb))
        else:
            verb = verbWord.get(Infinitive)
            answer.append('({}) {} {} {}'.format(pronoun.serb, cu.serb, verb.getSerbReflexive(selfness), verb.serb))

            verb = verbWord.get(decl)
            answer.append('({}) {} {} da {}'.format(pronoun.serb, cu.serb, verb.getSerbReflexive(selfness), verb.serb))

        return ExcerciseYield(title, question, answer)

class FuturQuestionsEx(Excercise):
    randomVerbsPool: RandomPool

    def __init__(self):
        super().__init__()

        # combine verbs and modal_verbs and exclude `treba`
        l = GetVocabulary('verbs').words + GetVocabulary('modal_verbs').words
        l = [w for w in l if w.title != 'treba']

        self.randomVerbsPool = RandomPool(l)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Ты придешь?
        # answer:   Da li ćeš doći?
        #           Hoćeš li doći?

        decl = Declination.Parse('present & male|fem|neu & first|second|third & sing|plur & nom')

        decl.humanizeNeutral()
        pronoun = GetVocabulary('personal_pronouns').getWordForm(decl)

        cu = GetVocabulary('cu').get(decl)
        verb = self.randomVerbsPool.yieldElem().get(Infinitive)
        selfness = random.randint(0, 1)

        title = 'Переведите на сербский'

        question = '{} {} {}?'.format(pronoun.rus, cu.rus, verb.getRusReflexive(selfness))
        answer = []

        answer.append('Da li {} {} {}?'.format(cu.serb, verb.getSerbReflexive(selfness), verb.serb))

        cu = GetVocabulary('hocu').get(decl)
        answer.append('{} li {} {}?'.format(cu.serb, verb.getSerbReflexive(selfness), verb.serb))

        return ExcerciseYield(title, question, answer)

class PrepositionsCasesEx(Excercise):
    case2PrepSerb: dict[Case, list[str]]
    prep2CaseRus: list[tuple[str, list[Case]]]
    serb2RusPrep: dict[str, str]

    def __init__(self):
        super().__init__()

        self.case2PrepSerb = {}
        self.prep2CaseRus = []

        self.serb2RusPrep = {}

        for c in [Case.gen, Case.aku, Case.dat, Case.inst, Case.lok]:
            self.case2PrepSerb[c] = []

        for prep in GetVocabulary('prepositions').phrases:
            langs = prep.aux.split(',')
            for lang in langs:
                splitted = lang.split(':')
                l = splitted[0].strip()
                cases = splitted[1].split()

                for c in cases:
                    case = Case[c.strip()]

                    if l == 'serb':
                        self.case2PrepSerb[case].append(prep.serb)
                    elif l == 'rus':
                        rusKey = next((tup for tup in self.prep2CaseRus if tup[0] == prep.rus), None)
                        if rusKey == None:
                            self.prep2CaseRus.append((prep.rus, [case]))
                        else:
                            rusKey[1].append(case)

            self.serb2RusPrep[prep.serb] = prep.rus
            self.prep2CaseRus = [(tup[0], list(set(tup[1]))) for tup in self.prep2CaseRus]

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Oko vas
        # answer:   Вокруг вас

        withNoun = random.randint(0, 1)
        number = RandomEnum(Number)

        serbCase = random.choice([Case.gen, Case.aku, Case.dat, Case.inst, Case.lok])

        serbPreposition = random.choice( self.case2PrepSerb[serbCase] )
        rusPreposition = self.serb2RusPrep[serbPreposition]

        rusPrepTup = next((tup for tup in self.prep2CaseRus if tup[0] == rusPreposition), None)
        if rusPrepTup != None:
            rusCase = random.choice(rusPrepTup[1])
        else:
            rusCase = Case.aku

        if withNoun:
            serbDecl = Declination.Make(serbCase, number)
            rusDecl = Declination.Make(rusCase, number)

            noun = random.choice( GetVocabulary('nouns').words )
            serbObject = noun.get(serbDecl)
            rusObject = noun.get(rusDecl)
        else:
            gender = RandomEnum(Gender)
            person = RandomEnum(Person)

            serbDecl = Declination.Make(serbCase, number, gender, person)
            rusDecl = Declination.Make(rusCase, number, gender, person)
            serbObject = GetVocabulary('personal_pronouns').getWordForm(serbDecl)
            rusObject = GetVocabulary('personal_pronouns').getWordForm(rusDecl)

        if ',' in rusPreposition:
            rusPreposition = '[{}]'.format(rusPreposition)

        title = 'Переведите на сербский'
        question = '{} {}'.format(rusPreposition, rusObject.rus)
        answer = '{} {} ({})'.format(serbPreposition, serbObject.serb, str(serbCase))

        return ExcerciseYield(title, question, answer)

class ComparativeEx(Excercise):
    randomNounsPool: RandomPool
    randomAdjectivesPool: RandomPool

    def __init__(self):
        super().__init__()
        self.randomNounsPool = RandomPool(GetVocabulary('nouns').words)
        self.randomAdjectivesPool = RandomPool(GetVocabulary('adjectives').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Эта умная кошка моя
        # answer:   Ta pametna mačka je moja

        # title:    Переведите на русский:
        # question: Taj veliki kukuruz je njihov
        # answer:   Та большая кукуруза - их

        lang = LangMode.GetLangBit()

        subjDecl = Declination.Make(Case.nom, RandomEnum(Number), Person.third, Definition.comp)

        noun = WordBiForm.MakeFromNoun(self.randomNounsPool.yieldElem(), subjDecl)
        adj = noun.clone().setWord(self.randomAdjectivesPool.yieldElem())
        tobe = noun.clone().setWord(GetVocabulary('tobe'))

        person = RandomEnum(Person)

        mojDecl = Declination.Make(person, RandomEnum(Number), RandomEnum(Gender))
        tvojDecl = Declination.Make(person.getOpposite(), RandomEnum(Number), RandomEnum(Gender))

        pronounsVoc = GetVocabulary('possessive_pronouns')

        moj = noun.clone().setWord(pronounsVoc.getWord(mojDecl))
        tvoj = noun.clone().setWord(pronounsVoc.getWord(tvojDecl))
        tvoj.commonDecl.override(Case.gen)

        title = ['Переведите на сербский', 'Переведите на русский'][lang]
        question = '{} {} {} {}'.format(moj.rus(), noun.rus(), adj.rus(), tvoj.rus())
        answer = '{} {} {} {} od {}'.format(moj.serb(), noun.serb(), tobe.serb(), adj.serb(), tvoj.serb())

        if lang:
            question, answer = answer, question

        return ExcerciseYield(title, question, answer)

class SuperlativeEx(Excercise):
    randomNounsPool: RandomPool
    randomAdjectivesPool: RandomPool

    def __init__(self):
        super().__init__()
        self.randomNounsPool = RandomPool(GetVocabulary('nouns').words)
        self.randomAdjectivesPool = RandomPool(GetVocabulary('adjectives').words)

    def __call__(self) -> ExcerciseYield:
        # title:    Переведите на сербский:
        # question: Эта умная кошка моя
        # answer:   Ta pametna mačka je moja

        # title:    Переведите на русский:
        # question: Taj veliki kukuruz je njihov
        # answer:   Та большая кукуруза - их

        lang = LangMode.GetLangBit()

        subjDecl = Declination.Make(Case.nom, RandomEnum(Number), Person.third, Definition.super)

        noun = WordBiForm.MakeFromNoun(self.randomNounsPool.yieldElem(), subjDecl)
        adj = noun.clone().setWord(self.randomAdjectivesPool.yieldElem())
        tobe = noun.clone().setWord(GetVocabulary('tobe'))

        person = RandomEnum(Person)

        mojDecl = Declination.Make(person, RandomEnum(Number), RandomEnum(Gender))
        pronounsVoc = GetVocabulary('possessive_pronouns')
        moj = noun.clone().setWord(pronounsVoc.getWord(mojDecl))

        title = ['Переведите на сербский', 'Переведите на русский'][lang]
        question = '{} {} {}'.format(moj.rus(), noun.rus(), adj.rus())
        answer = '{} {} {} {}'.format(moj.serb(), noun.serb(), tobe.serb(), adj.serb())

        if lang:
            question, answer = answer, question

        return ExcerciseYield(title, question, answer)

class ConjunctivePositiveEx(Excercise):
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
        # question: Я бы читал.
        # answer:   Ja bih čitao.

        negative = random.randint(0, 1)
        withOccupation = RandomPercent(30)

        decl = Declination.Parse('perfect & male|fem|neu & first|second|third & sing|plur & nom')

        if withOccupation:
            decl.parseOverride('male|fem & third')
            subject = self.randomOccupationsPool.yieldElem().get(decl)
        else:
            decl.humanizeNeutral()
            subject = GetVocabulary('personal_pronouns').getWordForm(decl)

        bih = GetVocabulary('bih').get(decl)
        verb = self.randomVerbsPool.yieldElem().get(decl)

        title = 'Переведите на сербский'

        needClarify = decl.number == Number.plur
        clarification = ''
        if needClarify:
            if decl.gender == Gender.male:
                clarification = '(муж.)'
            elif decl.gender == Gender.fem:
                clarification = '(жен.)'
            elif decl.gender == Gender.neu:
                clarification = '(ср.)'

        question = '{}{}{}{}'.format(subject.rus, clarification,  [' бы ', ' бы не '][negative], verb.rus)

        bihSerb = bih.serb
        if negative:
            bihSerb = 'ne ' + bihSerb

        canOmitPronoun = decl.person == Person.first or (decl.person == Person.second and decl.number == Number.plur)

        if withOccupation:
            answer = '{} {} {}'.format(subject.serb, bihSerb, verb.serb)
        else:
            answer = []
            answer.append('{} {} {}'.format(subject.serb, bihSerb, verb.serb))

            if canOmitPronoun:
                if negative:
                    answer.append('{} {}'.format(bihSerb, verb.serb))
                else:
                    answer.append('{} {}'.format(verb.serb, bihSerb))

        return ExcerciseYield(title, question, answer)

class ConjunctiveQuestionsEx(Excercise):
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
        # title:    Переведите на сербский:
        # question: Вы бы пришли?
        # answer:   Da li biste došli?

        withOccupation = RandomPercent(30)

        decl = Declination.Parse('perfect & male|fem|neu & first|second|third & sing|plur & nom')

        if withOccupation:
            decl.parseOverride('male|fem & third')
            subject = self.randomOccupationsPool.yieldElem().get(decl)
        else:
            decl.humanizeNeutral()
            subject = GetVocabulary('personal_pronouns').getWordForm(decl)

        
        verb = self.randomVerbsPool.yieldElem().get(decl)

        title = 'Переведите на сербский'

        needClarify = decl.number == Number.plur
        clarification = ''
        if needClarify:
            if decl.gender == Gender.male:
                clarification = '(муж.)'
            elif decl.gender == Gender.fem:
                clarification = '(жен.)'
            elif decl.gender == Gender.neu:
                clarification = '(ср.)'

        question = '{}{} бы {}?'.format(subject.rus, clarification, verb.rus)

        canOmitPronoun = decl.person == Person.first or (decl.person == Person.second and decl.number == Number.plur)

        tb = GetVocabulary('bih').get(decl)
        if withOccupation or not canOmitPronoun:
            answer = 'Da li {} {} {}?'.format(tb.serb, subject.serb, verb.serb)
        else:
            answer = 'Da li {} {}?'.format(tb.serb, verb.serb)

        return ExcerciseYield(title, question, answer)

@dataclass
class CaseEx(Excercise):
    case: Case
    serbPreposition: str
    rusPreposition: str
    verbVocabularies: list[str]
    verbFilter: Callable[[Word], bool]
    subjectVocabularies: list[str]
    subjectFilter: Callable[[Word], bool]

    def __post_init__(self):
        verbs = []
        for voc in self.verbVocabularies:
            verbs += GetVocabulary(voc).words
        if self.verbFilter:
            verbs = [w for w in verbs if self.verbFilter(w)]
        self.randomVerbsPool = RandomPool(verbs)
        
        subjects = []
        for voc in self.subjectVocabularies:
            subjects += GetVocabulary(voc).words
        if self.subjectFilter:
            subjects = [w for w in subjects if self.subjectFilter(w)]
        self.randomNounsPool = RandomPool(subjects)

    def __call__(self) -> ExcerciseYield:
        title = 'Переведите на сербский'
        number = Number.sing if RandomPercent(70) else Number.plur
        gender = Gender.male if RandomPercent(50) else Gender.fem

        noun = self.randomNounsPool.yieldElem().get(Declination.Make(gender, self.case, number))

        rusPrep = ''
        serbPrep = ''
        if len(self.serbPreposition) > 0:
            i = random.randint(0, len(self.serbPreposition)-1)
            serbPrep = self.serbPreposition[i] + ' '
            rusPrep = self.rusPreposition[i] + ' '

        verbsSupport = len(self.randomVerbsPool.origList) > 0

        if verbsSupport:
            verb = self.randomVerbsPool.yieldElem().get(Declination.Make(Time.present, Person.first, Number.sing))
            negative = RandomPercent(25)

            rusNe = 'не ' if negative else ''
            serbNe = 'ne ' if negative else ''

            question = '{} {} {}{}'.format(rusNe, verb.rus, rusPrep, noun.rus)
            answer = '{} {} {}{}'.format(serbNe, verb.serb, serbPrep, noun.serb)
        else:
            question = '{}{}'.format(rusPrep, noun.rus)
            answer = '{}{}'.format(serbPrep, noun.serb)

        return ExcerciseYield(title, question, answer)

class AkuzativEx(CaseEx):
    def __init__(self):
        allowed_verbs = [
            'imati',
            'hteti',
            'mrzeti',
            'obožavati',
            'voleti',
            'želeti',
            'crtati',
            'kupovati',
            'prodavati',
            'razumeti',
            'slikati',
            'slušati',
            'tražiti',
            'zvati',
            'čekati',
            'čuti',
        ]

        def verbFilter(w: Word) -> bool:
            return w.title in allowed_verbs
        
        super().__init__(
            case= Case.aku,
            serbPreposition= [],
            rusPreposition= [],
            verbVocabularies= ['verbs', 'modal_verbs'],
            verbFilter= verbFilter,
            subjectVocabularies= ['nouns'],
            subjectFilter= None 
        )

def AnimalityFilter(w: Word) -> bool:
    if hasattr(w.metaDeclination, 'animality'):
        return w.metaDeclination.animality == Animality.anim
    return True

class InstrumentalEx(CaseEx):
    def __init__(self):
        allowed_verbs = [
            'slikati',
            'doručkovati',
            'govoriti',
            'igrati',
            'jesti',
            'odmarati',
            'pevati',
            'plivati',
            'pričati',
            'psovati',
            'putovati',
            'razgovarati',
            'ručati',
            'trčati',
            'večerati',
            'čitati',
            'čekati',
            'živeti',
        ]

        def verbFilter(w: Word) -> bool:
            return w.title in allowed_verbs
        
        super().__init__(
            case= Case.inst,
            serbPreposition= ['sa'],
            rusPreposition= ['с'],
            verbVocabularies= ['verbs'],
            verbFilter= verbFilter,
            subjectVocabularies= ['occupations', 'nouns', 'personal_pronouns'],
            subjectFilter= AnimalityFilter
        )

class DativEx(CaseEx):
    def __init__(self):
        def verbFilter(w: Word) -> bool:
            return w.title not in ['treba', 'biti'] 
        
        super().__init__(
            case= Case.dat,
            serbPreposition= ['zahvaljujući'],
            rusPreposition= ['благодаря'],
            verbVocabularies= ['verbs', 'modal_verbs'],
            verbFilter= verbFilter,
            subjectVocabularies= ['occupations', 'nouns', 'personal_pronouns'],
            subjectFilter= AnimalityFilter
        )

class GenitivEx(CaseEx):
    def __init__(self):
        super().__init__(
            case= Case.gen,
            serbPreposition= ['nema', 'bez'],
            rusPreposition= ['нет', 'без'],
            verbVocabularies= [],
            verbFilter= None,
            subjectVocabularies= ['occupations', 'nouns', 'personal_pronouns'],
            subjectFilter= None
        )

class Futur2PositiveEx(Excercise):
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
        #           Čitao sam.

        flipParts = random.randint(0, 1)

        class PartType(Enum):
            Main = 0,
            Depend = 1

        class Part:
            def __init__(self, exc: Futur2PositiveEx, type: PartType):
                withOccupation = RandomPercent(30)
                decl = Declination.Parse('{} & male|fem|neu & first|second|third & sing|plur & nom'.format('futur' if type == PartType.Main else 'perfect'))

                if withOccupation:
                    decl.parseOverride('male|fem & third')
                    self.subject = exc.randomOccupationsPool.yieldElem().get(decl)
                else:
                    decl.humanizeNeutral()
                    self.subject = GetVocabulary('personal_pronouns').getWordForm(decl)
                
                self.cu = GetVocabulary('cu' if type == PartType.Main else 'budem').get(decl)
                self.verbWord = exc.randomVerbsPool.yieldElem()
                self.decl = decl
                self.type = type

                particles = [
                    ('ako', 'если'),
                    ('čim', 'как только'),
                    ('kad', 'когда'),
                    ('ukoliko', 'в случае если'),
                ]
                self.particle = random.choice(particles)
            
            def __call__(self, lang: Language) -> str:
                res = []

                def getVer(elem):
                    return elem.serb if lang == Language.serb else elem.rus

                if self.type == PartType.Depend:
                    res.append(self.particle[0] if lang == Language.serb else self.particle[1])
                
                res.append(' ')
                res.append(getVer(self.subject))
                res.append(' ')
                res.append(getVer(self.cu))
                res.append(' ')
                res.append(getVer(self.verbWord.get(self.decl if self.type == PartType.Depend and lang == Language.serb else Infinitive)))

                return ''.join(res)

        firstPart = Part(self, PartType.Main)
        secondPart = Part(self, PartType.Depend)

        if flipParts:
            firstPart, secondPart = secondPart, firstPart

        title = 'Переведите на сербский'

        question = '{}, {}'.format(firstPart(Language.rus), secondPart(Language.rus))
        answer = '{}, {}'.format(firstPart(Language.serb), secondPart(Language.serb))

        return ExcerciseYield(title, question, answer)