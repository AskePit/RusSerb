from code.load import *
from code.excercise_types import *
from code.cutom_excercises import *

def TryExit(anykey):
    term = anykey == 'x' or anykey == 'X' or anykey == 'ч' or anykey == 'Ч'
    if term:
        quit()
    return anykey == 'q' or anykey == 'Q' or anykey == 'й' or anykey == 'Й'

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
        print('\n{}.........................\n'.format(PAD))
        print('{}{}:\n'.format(PAD, exYield.title))

        if type(exYield.question) is list:
            print('\n')
            for q in exYield.question:
                print('{}{}'.format(PAD, q))
        else:
            print('{}{}'.format(PAD, exYield.question), end='')

        ans = input()

        if TryExit(ans):
            break
        else:
            if type(exYield.answer) is list:
                print('\n')
                for a in exYield.answer:
                    print('{}{}'.format(PAD, a))
            else:
                print('{}{}'.format(PAD, exYield.answer))
            print('\n{}.........................\n'.format(PAD))
            ans = input()
            if TryExit(ans):
                break

def main():
    LoadVocabulary()
    excercises = LoadExcercises()

    currentDir = excercises

    while True:
        ClrScr()

        print('\n{}.........................\n'.format(PAD))
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

