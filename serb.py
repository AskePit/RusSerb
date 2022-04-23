from code.load import *
from code.excercise_types import *
from code.cutom_excercises import *

def IsExit(anykey):
    return anykey == 'q' or anykey == 'Q' or anykey == 'й' or anykey == 'Й'

def ClrScr():
    os.system('clear')

PAD = '  '

def ExecuteExcercise(exc: Excercise):
    excCall = ''

    if exc.type == ExcerciseType.phrases:
        excCall = 'PhrasesEx(\'{}\')'.format(exc.phrasesVoc)
    elif exc.type == ExcerciseType.custom:
        excCall = '{}()'.format(exc.customFunction)

    while True:
        exYield: ExcerciseYield = eval(excCall)

        ClrScr()
        print('\n{}.........................\n'.format(PAD))
        print('{}{}:\n'.format(PAD, exYield.title))
        print('{}{}'.format(PAD, exYield.question), end='')

        ans = input()

        if IsExit(ans):
            break
        else:
            print('{}{}'.format(PAD, exYield.answer))
            print('\n{}.........................\n'.format(PAD))
            ans = input()
            if IsExit(ans):
                break

def main():
    LoadVocabulary()
    excercises = LoadExcercises()

    currentDir = excercises

    while True:
        ClrScr()

        print('\n{}.........................\n'.format(PAD))
        print('{}Выберите упражнение:'.format(PAD))

        i = 0

        #[num, exc]
        dirKeys: dict[str, ExcercisesDir] = {}
        excKeys: dict[str, Excercise] = {}

        for d in currentDir.children:
            num = str(i+1)
            print('{}{}. {}'.format(PAD, num, d.name))

            dirKeys[num] = d

            i += 1

        for e in currentDir.excercises:
            num = str(i+1)
            print('{}{}. {}'.format(PAD, num, e.name))

            excKeys[num] = e

            i += 1

        print('\n{}q. Выход'.format(PAD))

        ans = input()
        if IsExit(ans):
            if (not hasattr(currentDir, 'parent')) or currentDir.parent == None:
                break
            else:
                currentDir = currentDir.parent
        elif ans in dirKeys:
            currentDir = dirKeys[ans]
        elif ans in excKeys:
            ExecuteExcercise(excKeys[ans])
        else:
            continue

if __name__ == "__main__":
    main()
