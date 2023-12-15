function createImageBox(item) {
    const [width, height] = item.size;

    const box = document.createElement('div');
    box.setAttribute('class', 'imagebox');

    const header = document.createElement('div');
    header.setAttribute('class', 'box-header');

    const img = document.createElement('img');
    const a = document.createElement('a');
    a.href = item.url;
    img.setAttribute('src', item.thumb);
    img.setAttribute('width', 320);
    img.setAttribute('height', 320 * (height/Math.max(width, 1)));
    a.appendChild(img);

    const source = document.createElement('div');
    source.setAttribute('class', 'image-source');

    const code = document.createElement('code');
    code.textContent = IMAGE_TEMPLATE.replace('$FILE', item.name);

    const copyButton = document.createElement('button');
    copyButton.setAttribute('title', 'Copy to clipboard');
    copyButton.addEventListener('click', () => {
        navigator.clipboard.writeText(code.textContent).then(function() {
            addMessage('success', 'Copied!');
        }, function(err) {
            addMessage('error', 'Couldn’t copy text: ' + err.toString());
        });
    });

    const copyIcon = document.createElement('img');
    copyIcon.setAttribute('src', '/static/copy.svg');

    copyButton.appendChild(copyIcon);

    source.appendChild(code);

    if ( navigator.clipboard ) {
        source.appendChild(copyButton);
    }

    box.appendChild(header);
    box.appendChild(a);
    box.appendChild(source);

    return box;

}

function argmin(arr) {
    const min = Math.min(...arr);
    return arr.indexOf(min);
}

const distributeImages = (() => {
    const columnHeights = [0, 0, 0];
    const columns = [
        document.querySelector('.column-1'),
        document.querySelector('.column-2'),
        document.querySelector('.column-3')
    ];

    function distributeImages(imageDatas) {
        console.log("Distribute images");
        for ( const item of imageDatas ) {
            const box = createImageBox(item);
            const image = box.querySelector('img');
            const columnIndex = argmin(columnHeights);
            columns[columnIndex].appendChild(box);
            columnHeights[columnIndex] = columns[columnIndex].clientHeight;
            console.log("  Add", item.name, "to", columnIndex);
            console.log("    heights:", ...columnHeights);
        }

    }

    return distributeImages;
})();
