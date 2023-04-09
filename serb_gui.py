from code.load import *
from code.excercise_types import *
from code.cutom_excercises import *

import webview
import json

class Api:
    def __init__(self, excercises) -> None:
        self.excercises = excercises
        self.numToEx = {}
    
    def setWindow(self, window):
        self.window = window

    def getExcercisesTree(self):
        return json.dumps(self.excercises.toJSON())
    
    def onExcClicked(self, excId):
        print(excId)
        pass
        '''
        if excIndex in self.numToEx:
            exc = self.numToEx[excIndex]
            if isinstance(exc, ExcerciseDescsDir):
                self.excercises = exc
                self.window.evaluate_js("showCurrentDirContent()")
            elif isinstance(exc, ExcerciseDesc):
                #ExecuteExcercises([exc], screen, input)
                print(f"execute excercise {exc.name}")
        '''

def main():
    LoadVocabulary('./vocabulary')
    LoadManuals('./mans')
    excercises = LoadExcercises()

    api = Api(excercises)
    window = webview.create_window('Serb', 'gui/index.html', js_api=api, width=1310, height=800)
    api.setWindow(window)
    webview.start(debug=True)

if __name__ == '__main__':
    main()
