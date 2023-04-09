from code.load import *
from code.excercise_types import *
from code.cutom_excercises import *

import webview
import json

class AppSession:
    excercisesTree: ExcerciseDescsDir
    currExcercises: list[ExcerciseDesc] = None
    currExcercise: ExcerciseDesc = None
    excercisesCache: dict[ExcerciseDesc, list[Excercise]] = {}

    def __init__(self, excercisesTree) -> None:
        self.excercisesTree = excercisesTree

    def startNewExcercise(self, excerciseId: str):
        print(excerciseId)
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

    def yieldTask(self) -> ExcerciseYield:
        self.currExcercise = random.choice(self.currExcercises)

        if self.currExcercise in self.excercisesCache:
            excObjects = self.excercisesCache[self.currExcercise]
        else:
            excObjects = []

            if self.currExcercise.type == ExcerciseType.phrases:
                excObjects.append(PhrasesEx(self.currExcercise.phrasesVoc))
            elif self.currExcercise.type == ExcerciseType.custom:
                for f in self.currExcercise.customFunctions:
                    excercise = eval(f'{f}()')
                    excObjects.append(excercise)
            
            self.excercisesCache[self.currExcercise] = excObjects
        
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
    
    def onExcClicked(self, excId):
        self.session.startNewExcercise(excId)
        exYield = self.session.yieldTask()
        self.window.evaluate_js(f"updateCard('{exYield.title}', '{exYield.question}', '{exYield.answer}')")

def main():
    LoadVocabulary('./vocabulary')
    LoadManuals('./mans')
    excercises = LoadExcercises()
    session = AppSession(excercises)

    api = Api(session)
    window = webview.create_window('Serb', 'gui/index.html', js_api=api, width=1310, height=800)
    api.setWindow(window)
    webview.start(debug=True)

if __name__ == '__main__':
    main()
