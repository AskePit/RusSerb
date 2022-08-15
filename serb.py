from code.load import *
from code.excercise_types import *
from code.cutom_excercises import *

class Screen:
    buffer: list[str]
    stashedBuffer: list[str]

    def clear(self):
        self.buffer = []
        return self

    def clrScr(self):
        os.system('cls')
        os.system('clear')
        return self
    
    def print(self):
        print(''.join(self.buffer))
        return self

    def createHeader(self, excOrDir: ExcerciseDesc|ExcerciseDescsDir, title: str) -> list[str]:
        self.clear()
        self.buffer.append(f'\n  {str(excOrDir)}\n\n')
        self.buffer.append(f'\n{PAD}.........................\n\n')
        self.buffer.append(f'{PAD}{title}:\n\n')
        return self
    
    def append(self, txt: str):
        self.buffer.append(txt)
        return self

    def stashBuffer(self):
        self.stashedBuffer = self.buffer
        self.buffer = []
        return self
    
    def popBuffer(self):
        self.buffer = self.stashedBuffer
        return self

def TryExit(anykey):
    term = anykey == 'x' or anykey == 'X' or anykey == 'ч' or anykey == 'Ч'
    if term:
        quit()
    return anykey == 'q' or anykey == 'Q' or anykey == 'й' or anykey == 'Й'

def TryHelp(anykey, manName, screen: Screen):
    help = anykey == 'h' or anykey == 'H' or anykey == 'р' or anykey == 'Р'
    if help:
        text = '\n    NO HELP' if manName == None or manName == '' else GetMan(manName)

        screen.clrScr().stashBuffer().append(text).print()
        input()
        screen.clrScr().popBuffer().print()
        return True
    else:
        return False

PAD = '  '

def ExecuteExcercise(exc: ExcerciseDesc, screen: Screen):
    excObjects = []

    if exc.type == ExcerciseType.phrases:
        excObjects.append(PhrasesEx(exc.phrasesVoc))
    elif exc.type == ExcerciseType.custom:
        for f in exc.customFunctions:
            excercise = eval(f'{f}()')
            excObjects.append(excercise)

    while True:
        excercise = random.choice(excObjects)
        exYield: ExcerciseYield = excercise()

        screen.clear().clrScr().createHeader(exc, exYield.title)

        if type(exYield.question) is list:
            screen.append('\n\n')
            for q in exYield.question:
                screen.append(f'{PAD}{q}\n')
        else:
            screen.append(f'{PAD}{exYield.question}\n')

        screen.print()

        ans = input()
        while TryHelp(ans, exc.help, screen):
            ans = input()

        if TryExit(ans):
            break
        else:
            if type(exYield.answer) is list:
                screen.append('\n\n')
                for a in exYield.answer:
                    screen.append(f'{PAD}{a}\n')
            else:
                screen.append(f'{PAD}{exYield.answer}\n')
            screen.append(f'\n{PAD}.........................\n\n')

            screen.clrScr().print()

            ans = input()
            while TryHelp(ans, exc.help, screen):
                ans = input()
            if TryExit(ans):
                break

def ExecuteQuiz(excs: list[ExcerciseDesc], screen: Screen):
    while True:
        exc = random.choice(excs)

        excObjects = []

        if exc.type == ExcerciseType.phrases:
            excObjects.append(PhrasesEx(exc.phrasesVoc))
        elif exc.type == ExcerciseType.custom:
            for f in exc.customFunctions:
                excercise = eval(f'{f}()')
                excObjects.append(excercise)
        
        excercise = random.choice(excObjects)
        exYield: ExcerciseYield = excercise()

        screen.clear().clrScr().createHeader(exc, exYield.title)

        if type(exYield.question) is list:
            screen.append('\n\n')
            for q in exYield.question:
                screen.append(f'{PAD}{q}\n')
        else:
            screen.append(f'{PAD}{exYield.question}\n')

        screen.print()

        ans = input()
        while TryHelp(ans, exc.help, screen):
            ans = input()

        if TryExit(ans):
            break
        else:
            if type(exYield.answer) is list:
                screen.append('\n\n')
                for a in exYield.answer:
                    screen.append(f'{PAD}{a}\n')
            else:
                screen.append(f'{PAD}{exYield.answer}\n')
            screen.append(f'\n{PAD}.........................\n\n')

            screen.clrScr().print()

            ans = input()
            while TryHelp(ans, exc.help, screen):
                ans = input()
            if TryExit(ans):
                break

def main():
    LoadVocabulary('./vocabulary')
    LoadManuals('./mans')
    excercises = LoadExcercises()

    currentDir = excercises

    screen = Screen()

    while True:
        screen.clear().clrScr().createHeader(currentDir, 'Выберите упражнение')

        files = []

        for d in currentDir.children:
            files.append(d)

        for e in currentDir.excercises:
            files.append(e)
        
        files.sort(key=lambda x: x.serialNumber)

        i = 0
        numToEx = {}

        for f in files:
            num = str(i+1)
            screen.append(f'{PAD}{num}. {f.name}\n')

            numToEx[num] = f

            i += 1

        screen.append(f'{PAD}0. Quiz\n')
        screen.append(f'\n{PAD}q. Назад')
        screen.append(f'\n{PAD}x. Выход\n')
        screen.print()

        ans = input()

        if TryExit(ans):
            if (not hasattr(currentDir, 'parent')) or currentDir.parent == None:
                break
            else:
                currentDir = currentDir.parent
        elif ans == '0':
            ExecuteQuiz(currentDir.getExcercisesRecursive(), screen)
        elif ans in numToEx:
            exc = numToEx[ans]
            if isinstance(exc, ExcerciseDescsDir):
                currentDir = exc
            elif isinstance(exc, ExcerciseDesc):
                ExecuteExcercise(exc, screen)
            else:
                continue

if __name__ == "__main__":
    main()

