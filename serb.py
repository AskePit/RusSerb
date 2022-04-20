from code.load import *

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
        print('\n' + PAD + '.........................\n')
        print(PAD + exYield.title + ':\n')
        print(PAD + exYield.question, end='')

        ans = input()

        if IsExit(ans):
            break
        else:
            print(PAD + exYield.answer)
            print('\n' + PAD + '.........................\n')
            ans = input()
            if IsExit(ans):
                break

def main():
    LoadVocabulary()
    excercises = LoadExcercises()

    currentDir = excercises

    while True:
        ClrScr()

        print('\n' + PAD + '.........................\n')
        print(PAD + 'Выберите упражнение:')

        i = 0

        #[num, exc]
        dirKeys: dict[str, ExcercisesDir] = {}
        excKeys: dict[str, Excercise] = {}

        for d in currentDir.children:
            num = str(i+1)
            print(PAD + num + '. ' + d.name)

            dirKeys[num] = d

            i = i + 1

        for e in currentDir.excercises:
            num = str(i+1)
            print(PAD + num + '. ' + e.name)

            excKeys[num] = e

            i = i + 1

        print('\n' + PAD + 'q. Выход')

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
