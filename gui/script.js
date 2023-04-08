window.addEventListener('pywebviewready', function() {
    loadExcercisesTree()
})

// Create event listener
document.addEventListener('click', (e) =>
    {
        let elementId = e.target.id;
        //console.log(e)
        if (elementId !== '') {
            pywebview.api.onExcClicked(parseInt(elementId, 10))
        }
        else {
            //console.log("An element without an id was clicked.");
        }

        let folders = document.getElementsByClassName('nav-folder')

        for(let i = 0; i<folders.length; ++i) {
            let folder = folders[i]
            if (folder.offsetHeight == 0 && folder.offsetWidth == 0) {
                continue;
            }

            let title = folder.getElementsByClassName('nav-folder-title')[0]
            if (e.x >= title.offsetLeft && e.x <= title.offsetLeft + title.offsetWidth && e.y >= title.offsetTop && e.y <= title.offsetTop + title.offsetHeight) {
                folder.classList.toggle('is-collapsed')
                break
            }
        }
    }
);

function loadExcercisesTree() {
    pywebview.api.getExcercisesTree().then(onExcercisesTreeReady)
}

function onExcercisesTreeReady(treeString) {
    let tree = JSON.parse(treeString)

    var navContainer = document.getElementById('nav-container')
    navContainer.innerHTML = getRootFolderHtml(tree)
}

function getRootFolderHtml(folder) {
    return getFolderContentHtml(folder)
}

function getFolderHtml(folder) {
    return `
    <div class="nav-folder is-collapsed">
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
        <div class="nav-file">
            <div class="nav-file-title">
                <div class="nav-file-title-content">${exc.name}</div>
            </div>
        </div>
    `
}
