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
        print(PAD + '1. To be')
        print(PAD + '2. To be вопросы')
        print(PAD + '3. To be ответы')
        print(PAD + '4. Фразы приветствия')
        print('\n' + PAD + 'q. Выход')
        
        ans = input()
        if IsExit(ans):
            break
        elif ans == '1':
            ExecuteExcercise(ToBeEx)
        elif ans == '2':
            ExecuteExcercise(ToBeEx2)
        elif ans == '3':
            ExecuteExcercise(ToBeEx3)
        elif ans == '4':
            ExecuteExcercise(GreetingsEx)
        else:
            continue

if __name__ == "__main__":
    main()
