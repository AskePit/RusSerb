window.addEventListener('pywebviewready', function() {
    loadExcercisesTree()
})

const NO_TASK = 0
const TASK_GIVEN = 1
const TASK_ANSWERED = 2

cardState = NO_TASK

window.onkeydown = (event) => {
    if(event.code === "Space" || event.code === "Enter" || event.code === "ArrowRight") {
        event.stopPropagation()
        event.preventDefault()

        if(cardState === TASK_GIVEN) {
            showAnswer()
        } else if (cardState === TASK_ANSWERED) {
            pywebview.api.onNextClicked()
        }
    }
};

function loadExcercisesTree() {
    pywebview.api.getExcercisesTree().then(onExcercisesTreeReady)
}

function onExcercisesTreeReady(treeString) {
    let tree = JSON.parse(treeString)

    var navContainer = document.getElementById('nav-container')
    navContainer.innerHTML = getRootFolderHtml(tree)

    const folders = document.getElementsByClassName("nav-folder");
    const files = document.getElementsByClassName("nav-file");

    for (let folder of folders) {
        folder.addEventListener("click", e => {
            e.currentTarget.classList.toggle('is-collapsed')
            e.stopPropagation()
        });
    }

    for (let file of files) {
        file.addEventListener("click", e => {
            e.stopPropagation()
            
            if (e.currentTarget.classList.contains('active')) {
                return
            }

            for (let file of files) {
                file.classList.remove('active')
            }
            e.currentTarget.classList.add('active')

            hidePhrasesCounter()
            pywebview.api.onExcClicked(e.currentTarget.id).then(onExcerciseReady)
        });
    }
}

function onExcerciseReady(phrasesCount) {
    if (phrasesCount < 0) {
        return
    }

    showPhrasesCounter(phrasesCount)
}

function getRootFolderHtml(folder) {
    return getFolderContentHtml(folder)
}

function getFolderHtml(folder) {
    return `
    <div class="nav-folder is-collapsed" id="${folder.id}">
        <div class="nav-folder-title">
            <div class="collapse-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="svg-icon"><path d="M3 8L12 17L21 8"/></svg></div>
            <div class="nav-folder-title-content">${folder.name}</div>
        </div>
        <div class="nav-folder-children">
            ${getFolderContentHtml(folder)}
        </div>
    </div>
    `
}

function getFolderContentHtml(folder) {
    return `
        ${getChildFoldersHtml(folder)}
        ${getExcercisesHtml(folder)}
    `
}

function getChildFoldersHtml(folder) {
    let childFolders = ''
    for(let i = 0; i<folder.children.length; ++i) {
        let childFolder = folder.children[i]
        childFolders += getFolderHtml(childFolder) + '\n'
    }

    return childFolders
}

function getExcercisesHtml(folder) {
    let excercises = ''
    for(let i = 0; i<folder.excercises.length; ++i) {
        let exc = folder.excercises[i]
        excercises += getExcerciseHtml(exc) + '\n'
    }

    return excercises
}

function getExcerciseHtml(exc) {
    return `
        <div class="nav-file" id="${exc.id}">
            <div class="nav-file-title">
                <div class="nav-file-title-content">${exc.name}</div>
            </div>
        </div>
    `
}

function updateCard(title, task, question, answer) {
    cardState = TASK_GIVEN
    document.getElementById('card').style.display = 'flex'
    document.getElementById('excercise-title').innerText = title
    document.getElementById('card-task').innerText = task
    document.getElementById('card-question').innerText = question
    document.getElementById('card-answer').innerText = answer
    showAnswerButton()

    incPhrasesCounter()
}

function showAnswerButton() {
    document.getElementById('card-button').removeAttribute('hidden')
    document.getElementById('card-answer').setAttribute('hidden', '')
}

function showAnswer() {
    document.getElementById('card-answer').removeAttribute('hidden')
    document.getElementById('card-button').setAttribute('hidden', '')
    cardState = TASK_ANSWERED
}

var currPhraseIndex = 1
var phrasesCount = 0

function hidePhrasesCounter() {
    phrasesCount = -1
    currPhraseIndex = 0
    document.getElementById('cards-counter').style.display = 'none'
}

function showPhrasesCounter(count) {
    phrasesCount = count
    document.getElementById('cards-counter').style.display = 'flex'
    document.getElementById('counter').innerText = `1/${phrasesCount}`
}

function incPhrasesCounter() {
    if (phrasesCount < 0) {
        return
    }
    currPhraseIndex += 1
    if (currPhraseIndex > phrasesCount) {
        currPhraseIndex = 1
    }
    document.getElementById('counter').innerText = `${currPhraseIndex}/${phrasesCount}`
}