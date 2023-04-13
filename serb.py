from code.load import *
from code.excercise_types import *
from code.cutom_excercises import *

import webview
import json

class AppSession:
    excercisesTree: ExcerciseDescsDir
    currExcercises: list[ExcerciseDesc] = None
    currExcercise: ExcerciseDesc = None
    excerciseObjects: dict[ExcerciseDesc, list[Excercise]] = {}

    phrasesCount: int = -1

    def __init__(self, excercisesTree) -> None:
        self.excercisesTree = excercisesTree

    def isExcersiseActive(self) -> bool:
        return self.currExcercises != None

    def startNewExcercise(self, excerciseId: str):
        path = excerciseId.split('-')
        path = path[1:]
        
        exc = self.excercisesTree
        for num in path:
            int_num = int(num)

            found = False

            for ch in exc.children:
                if ch.serialNumber == int_num:
                    exc = ch
                    found = True
                    break
            
            if found:
                continue

            for ch in exc.excercises:
                if ch.serialNumber == int_num:
                    exc = ch
                    break
            
        self.currExcercises = [exc]

        allPhrases = True
        phrasesCount = 0

        for excDesc in self.currExcercises:
            excObjects = []

            if excDesc.type == ExcerciseType.phrases:
                phrasesEx = PhrasesEx(excDesc.phrasesVoc)
                phrasesCount += len(phrasesEx.phrases)
                excObjects.append(phrasesEx)
                
            elif excDesc.type == ExcerciseType.custom:
                for f in excDesc.customFunctions:
                    excercise = eval(f'{f}()')
                    excObjects.append(excercise)
                allPhrases = False
            
            self.excerciseObjects[excDesc] = excObjects
        
        if allPhrases:
            self.phrasesCount = phrasesCount
        else:
            self.phrasesCount = -1

    def yieldTask(self) -> ExcerciseYield:
        self.currExcercise = random.choice(self.currExcercises)
        excObjects = self.excerciseObjects[self.currExcercise]
        excercise = random.choice(excObjects)
        return excercise()
    
    def getHelp(self) -> str|None:
        return self.currExcercise.help


class Api:
    session: AppSession
    window: webview.Window

    def __init__(self, session) -> None:
        self.session = session
        self.numToEx = {}
    
    def setWindow(self, window):
        self.window = window

    def getExcercisesTree(self) -> str:
        return json.dumps(self.session.excercisesTree.toJSON())
    
    def onExcClicked(self, excId) -> int:
        self.session.startNewExcercise(excId)
        self.onNextClicked()
        return self.session.phrasesCount
    
    def onNextClicked(self):
        if self.session.isExcersiseActive():
            exYield = self.session.yieldTask()

            answer = ''
            if type(exYield.answer) is list:
                answer = '\\n'.join(exYield.answer)
            else:
                answer = exYield.answer
            
            self.window.evaluate_js(f"updateCard('{self.session.currExcercise.name}', '{exYield.title}', '{exYield.question}', '{answer}')")

def main():
    LoadVocabulary('./vocabulary')
    LoadManuals('./mans')
    excercises = LoadExcercises()
    session = AppSession(excercises)

    api = Api(session)
    window = webview.create_window('Serb', 'gui/index.html', js_api=api, width=1310, height=800)
    api.setWindow(window)
    webview.start(debug=False)

if __name__ == '__main__':
    main()
