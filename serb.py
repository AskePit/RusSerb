from code.load import *
from code.excercise_types import *
from code.cutom_excercises import *

def TryExit(anykey):
    term = anykey == 'x' or anykey == 'X' or anykey == 'ч' or anykey == 'Ч'
    if term:
        quit()
    return anykey == 'q' or anykey == 'Q' or anykey == 'й' or anykey == 'Й'

def TryHelp(anykey, manName, screen):
    help = anykey == 'h' or anykey == 'H' or anykey == 'р' or anykey == 'Р'
    if help:
        def yieldText(text: str):
            ClrScr()
            print(text)
            input()
            ClrScr()
            print(screen)

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

        screen = ''
        screen += '\n  {}\n\n'.format(str(exc))
        screen += '\n{}.........................\n\n'.format(PAD)
        screen += '{}{}:\n\n'.format(PAD, exYield.title)

        if type(exYield.question) is list:
            screen += '\n\n'
            for q in exYield.question:
                screen += '{}{}\n'.format(PAD, q)
        else:
            screen += '{}{}\n'.format(PAD, exYield.question)

        print(screen)

        ans = input()
        while TryHelp(ans, exc.help, screen):
            ans = input()

        if TryExit(ans):
            break
        else:
            if type(exYield.answer) is list:
                screen += '\n\n'
                for a in exYield.answer:
                    screen += '{}{}\n'.format(PAD, a)
            else:
                screen += '{}{}\n'.format(PAD, exYield.answer)
            screen += '\n{}.........................\n\n'.format(PAD)

            ClrScr()
            print(screen)

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

        print('\n  {}\n\n'.format(str(currentDir)))
        print('{}.........................\n'.format(PAD))
        print('{}Выберите упражнение:'.format(PAD))

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
            print('{}{}. {}'.format(PAD, num, f.name))

            numToEx[num] = f

            i += 1

        print('\n{}q. Назад'.format(PAD), end='')
        print('\n{}x. Выход'.format(PAD))

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

