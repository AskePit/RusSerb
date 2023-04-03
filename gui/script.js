window.addEventListener('pywebviewready', function() {
    showCurrentDirContent()
})

// Create event listener
document.addEventListener('click', (e) =>
  {
    // Retrieve id from clicked element
    let elementId = e.target.id;
    // If element has id
    if (elementId !== '') {
        pywebview.api.onExcClicked(parseInt(elementId, 10))
    }
    // If element has no id
    else { 
        //console.log("An element without an id was clicked.");
    }
  }
);

var currentDir = {}

function showCurrentDirContent() {
    pywebview.api.getCurrentDirContent().then(onCurrentDirContentReady)
}

function onCurrentDirContentReady(content) {
    console.log("heyyyyyyy")
    console.log(JSON.parse(content))

    /*
    var catalogue = document.getElementById('catalogue')

    html = ''

    for(let i = 0; i<content.length; ++i) {
        let exc = content[i]
        //console.log(exc)
        html += `
            <div class="excercise_item" id="${i}">
            ${exc.isDir ? "〉" : ""}${exc.name}
            </div>
        `
    }

    catalogue.innerHTML = html
    */
}