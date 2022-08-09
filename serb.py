from code.load import *
from code.excercise_types import *
from code.cutom_excercises import *

def TryExit(anykey):
    term = anykey == 'x' or anykey == 'X' or anykey == 'ч' or anykey == 'Ч'
    if term:
        quit()
    return anykey == 'q' or anykey == 'Q' or anykey == 'й' or anykey == 'Й'

def TryHelp(anykey, manName, screen: list[str]):
    help = anykey == 'h' or anykey == 'H' or anykey == 'р' or anykey == 'Р'
    if help:
        def yieldText(text: str):
            ClrScr()
            print(text)
            input()
            ClrScr()
            print(''.join(screen))

        if manName == None or manName == '':
            yieldText('\n    NO HELP')
        else:
            yieldText(GetMan(manName))
        return True
    else:
        return False

def ClrScr():
    os.system('cls')
    os.system('clear')

PAD = '  '

def BuildScreenTop(excOrDir: ExcerciseDesc|ExcerciseDescsDir, title: str) -> list[str]:
    screen: list[str] = []
    screen.append('\n  {}\n\n'.format(str(excOrDir)))
    screen.append('\n{}.........................\n\n'.format(PAD))
    screen.append('{}{}:\n\n'.format(PAD, title))

    return screen

def ExecuteExcercise(exc: ExcerciseDesc):
    excObjects = []

    if exc.type == ExcerciseType.phrases:
        excObjects.append(PhrasesEx(exc.phrasesVoc))
    elif exc.type == ExcerciseType.custom:
        for f in exc.customFunctions:
            excercise = eval('{}()'.format(f))
            excObjects.append(excercise)

    while True:
        excercise = random.choice(excObjects)
        exYield: ExcerciseYield = excercise()

        ClrScr()

        screen = BuildScreenTop(exc, exYield.title)

        if type(exYield.question) is list:
            screen.append('\n\n')
            for q in exYield.question:
                screen.append('{}{}\n'.format(PAD, q))
        else:
            screen.append('{}{}\n'.format(PAD, exYield.question))

        print(''.join(screen))

        ans = input()
        while TryHelp(ans, exc.help, screen):
            ans = input()

        if TryExit(ans):
            break
        else:
            if type(exYield.answer) is list:
                screen += '\n\n'
                for a in exYield.answer:
                    screen.append('{}{}\n'.format(PAD, a))
            else:
                screen.append('{}{}\n'.format(PAD, exYield.answer))
            screen.append('\n{}.........................\n\n'.format(PAD))

            ClrScr()
            print(''.join(screen))

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

    while True:
        ClrScr()

        screen = BuildScreenTop(currentDir, 'Выберите упражнение')

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
            screen.append('{}{}. {}\n'.format(PAD, num, f.name))

            numToEx[num] = f

            i += 1

        screen.append('\n{}q. Назад'.format(PAD))
        screen.append('\n{}x. Выход\n'.format(PAD))

        print(''.join(screen))

        ans = input()

        if TryExit(ans):
            if (not hasattr(currentDir, 'parent')) or currentDir.parent == None:
                break
            else:
                currentDir = currentDir.parent
        elif ans in numToEx:
            exc = numToEx[ans]
            if isinstance(exc, ExcerciseDescsDir):
                currentDir = exc
            elif isinstance(exc, ExcerciseDesc):
                ExecuteExcercise(exc)
            else:
                continue

if __name__ == "__main__":
    main()

