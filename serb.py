from code.load import *
from code.exercises import *

def IsExit(anykey):
    return anykey == 'q' or anykey == 'Q' or anykey == 'й' or anykey == 'Й'

def ClrScr():
    os.system('clear')

PAD = '  '

def ExecuteExcercise(exFunc):
    while True:
        exYield: ExcerciseYield = exFunc()

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

    while True:
        ClrScr()

        print('\n' + PAD + '.........................\n')
        print(PAD + 'Выберите упражнение:')

        i = 0

        exKeys: dict[str, ExcerciseFuncType] = {}

        for ex, name in excercises:
            num = str(i+1)
            print(PAD + num + '. ' + name)

            exKeys[num] = ex

            i = i + 1
        print('\n' + PAD + 'q. Выход')
        
        ans = input()
        if IsExit(ans):
            break
        elif ans in exKeys:
            ExecuteExcercise(exKeys[ans])
        else:
            continue

if __name__ == "__main__":
    main()
