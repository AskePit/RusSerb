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
        excCall = 'PhrasesEx(\'%s\')' % exc.phrasesVoc
    elif exc.type == ExcerciseType.custom:
        excCall = '%s()' % exc.customFunction

    while True:
        exYield: ExcerciseYield = eval(excCall)

        ClrScr()
        print('\n%s.........................\n' % PAD)
        print('%s%s:\n' % (PAD, exYield.title))
        print('%s%s' % (PAD, exYield.question), end='')

        ans = input()

        if IsExit(ans):
            break
        else:
            print('%s%s' % (PAD, exYield.answer))
            print('\n%s.........................\n' % PAD)
            ans = input()
            if IsExit(ans):
                break

def main():
    LoadVocabulary()
    excercises = LoadExcercises()

    currentDir = excercises

    while True:
        ClrScr()

        print('\n%s.........................\n' % PAD)
        print('%sВыберите упражнение:' % PAD)

        i = 0

        #[num, exc]
        dirKeys: dict[str, ExcercisesDir] = {}
        excKeys: dict[str, Excercise] = {}

        for d in currentDir.children:
            num = str(i+1)
            print('%s%s. %s' % (PAD, num, d.name))

            dirKeys[num] = d

            i += 1

        for e in currentDir.excercises:
            num = str(i+1)
            print('%s%s. %s' % (PAD, num, e.name))

            excKeys[num] = e

            i += 1

        print('\n%sq. Выход' % PAD)

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
