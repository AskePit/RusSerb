from code.load import *
from code.excercise_types import *
from code.cutom_excercises import *

import webview
import json

class Api:
    def __init__(self, excercises) -> None:
        self.currentDir = excercises
        self.numToEx = {}
    
    def setWindow(self, window):
        self.window = window

    def getCurrentDirContent(self):
        return json.dumps(self.currentDir.toJSON())
        files = []

        for d in self.currentDir.children:
            files.append(d)

        for e in self.currentDir.excercises:
            files.append(e)
        
        files.sort(key=lambda x: x.serialNumber)

        i = 0
        self.numToEx = {}

        response = []

        for f in files:
            response.append({"isDir": isinstance(f, ExcerciseDescsDir), "name": f.name})

            self.numToEx[i] = f
            i += 1

        return response
    
    def onExcClicked(self, excIndex):
        if excIndex in self.numToEx:
            exc = self.numToEx[excIndex]
            if isinstance(exc, ExcerciseDescsDir):
                self.currentDir = exc
                self.window.evaluate_js("showCurrentDirContent()")
            elif isinstance(exc, ExcerciseDesc):
                #ExecuteExcercises([exc], screen, input)
                print(f"execute excercise {exc.name}")

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
