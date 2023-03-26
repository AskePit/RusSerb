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

    def appendHeader(self, excOrDir: ExcerciseDesc|ExcerciseDescsDir, title: str) -> list[str]:
        self.buffer.append(f'\n  {str(excOrDir)}\n\n')
        self.buffer.append(f'\n{PAD}.........................\n\n')
        self.buffer.append(f'{PAD}{title}:\n\n')
        return self

    def appendFooter(self) -> list[str]:
        self.buffer.append(f'\n{PAD}.........................\n\n')
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

class InputType(Enum):
    Quit = 0,
    Help = 1,
    Quiz = 2,
    Other = 3

class Input:
    input: str

    def getInput(self) -> InputType:
        self.input = input()
        if Input._isTerm(self.input):
            quit()
        elif Input._isQuit(self.input):
            return InputType.Quit
        elif Input._isHelp(self.input):
            return InputType.Help
        elif Input._isQuiz(self.input):
            return InputType.Quiz
        else:
            return InputType.Other
    
    def get(self) -> str:
        return self.input

    def _isTerm(key):
        return key == 'x' or key == 'X' or key == 'ч' or key == 'Ч'
    
    def _isQuit(key):
        return key == 'q' or key == 'Q' or key == 'й' or key == 'Й'

    def _isHelp(key):
        return key == 'h' or key == 'H' or key == 'р' or key == 'Р'
    
    def _isQuiz(key):
        return key == '0'

PAD = '  '

def Help(manName, screen: Screen, input: Input):
    text = '\n    NO HELP' if manName == None or manName == '' else GetMan(manName)

    screen.clrScr().stashBuffer().append(text).print()
    input.getInput()
    screen.clrScr().popBuffer().print()

def ExecuteExcercises(excs: list[ExcerciseDesc], screen: Screen, input: Input):
    excercisesCache: dict[ExcerciseDesc, list[Excercise]] = {}

    while True:
        exc = random.choice(excs)

        if exc in excercisesCache:
            excObjects = excercisesCache[exc]
        else:
            excObjects = []

            if exc.type == ExcerciseType.phrases:
                excObjects.append(PhrasesEx(exc.phrasesVoc))
            elif exc.type == ExcerciseType.custom:
                for f in exc.customFunctions:
                    excercise = eval(f'{f}()')
                    excObjects.append(excercise)
            
            excercisesCache[exc] = excObjects
        
        excercise = random.choice(excObjects)
        exYield: ExcerciseYield = excercise()

        screen.clear().clrScr().appendHeader(exc, exYield.title)

        if type(exYield.question) is list:
            screen.append('\n\n')
            for q in exYield.question:
                screen.append(f'{PAD}{q}\n')
        else:
            screen.append(f'{PAD}{exYield.question}\n')

        screen.print()

        def TryHelpOrQuit() -> bool: # true if quit
            ans = input.getInput()
            while ans == InputType.Help:
                Help(exc.help, screen, input)
                ans = input.getInput()
            return ans == InputType.Quit

        if TryHelpOrQuit():
            break

        if type(exYield.answer) is list:
            screen.append('\n\n')
            for a in exYield.answer:
                screen.append(f'{PAD}{a}\n')
        else:
            screen.append(f'{PAD}{exYield.answer}\n')

        screen.appendFooter().clrScr().print()

        if TryHelpOrQuit():
            break

def main():
    LoadVocabulary('./vocabulary')
    LoadManuals('./mans')
    excercises = LoadExcercises()

    currentDir = excercises

    screen = Screen()
    input = Input()

    while True:
        screen.clear().clrScr().appendHeader(currentDir, 'Выберите упражнение')

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

        ans = input.getInput()

        if ans == InputType.Quit:
            if (not hasattr(currentDir, 'parent')) or currentDir.parent == None:
                break
            else:
                currentDir = currentDir.parent
        elif ans == InputType.Quiz:
            ExecuteExcercises(currentDir.getExcercisesRecursive(), screen, input)
        elif input.get() in numToEx:
            exc = numToEx[input.get()]
            if isinstance(exc, ExcerciseDescsDir):
                currentDir = exc
            elif isinstance(exc, ExcerciseDesc):
                ExecuteExcercises([exc], screen, input)
            else:
                continue

if __name__ == "__main__":
    main()
