function addMessage(type, message) {
    const container = document.querySelector('#messages');
    const elem = document.createElement('div');
    elem.setAttribute('class', 'flash');
    elem.textContent = message;
    if ( type == 'success' ) {
        elem.classList.add('success');
    } else if ( type == 'error' ) {
        elem.classList.add('error');
    }
    container.appendChild(elem);
    setTimeout(() => {
        elem.remove();
    }, 5000);
}

function createBox(item, entry) {
    const box = document.createElement('div');
    box.setAttribute('class', 'result-box');

    const header = document.createElement('div');
    header.setAttribute('class', 'box-header');
    if ( entry ) {
        const span = document.createElement('span');
        const wikidataLink = document.createElement('a');
        wikidataLink.textContent = entry.id;
        wikidataLink.setAttribute('href', entry.url);
        span.appendChild(wikidataLink);
        header.appendChild(span);
        box.classList.add(entry.colorClass);
        box.setAttribute('title', entry.text);
        if ( entry.id.startsWith('Q') ) {
            const moreLink = document.createElement('a');
            moreLink.textContent = '🔍';
            moreLink.setAttribute('href', 'more-images' + location.search + '&item=' + entry.id);
            span.appendChild(moreLink);

        }
    }
    if ( item && item.facet ) {
        const facet = document.createElement('span');
        facet.setAttribute('class', 'facet');
        facet.textContent = item.facet;
        header.appendChild(facet);
    }

    box.appendChild(header);

    return box;
}

function createImageBox(item, entry) {
    const [width, height] = item.size;
    const box = createBox(item, entry);
    box.classList.add('imagebox');

    const img = document.createElement('img');
    const a = document.createElement('a');
    a.href = item.url;
    img.setAttribute('src', item.thumb);
    img.setAttribute('width', 320);
    img.setAttribute('height', 320 * (height/Math.max(width, 1)));
    a.appendChild(img);

    const footer = document.createElement('div');
    footer.setAttribute('class', 'box-footer');

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

    footer.appendChild(code);

    if ( navigator.clipboard ) {
        footer.appendChild(copyButton);
    }

    box.appendChild(a);
    box.appendChild(footer);

    return box;

}

function createLinkBox(item, entry) {

    const box = createBox(item, entry);
    box.classList.add('result-link');

    const img = document.createElement('img');
    const a = document.createElement('a');
    a.setAttribute('class', 'box-content');
    a.setAttribute('href', item.url);
    img.setAttribute('src', '/static/Commons-logo.svg');
    img.setAttribute('width', 100);
    img.setAttribute('height', 100);
    const label = document.createElement('label');
    label.textContent = item.name;
    a.appendChild(img);
    a.appendChild(label);

    box.appendChild(a);

    return box;
}

function createNoImagesBox(entry) {

    const box = createBox(null, entry);
    box.classList.add('result-no-images');

    const img = document.createElement('img');
    const div = document.createElement('div');
    div.setAttribute('class', 'box-content');
    img.setAttribute('src', '/static/No_Image_(2879926)_-_The_Noun_Project.svg');
    img.setAttribute('width', 100);
    img.setAttribute('height', 100);
    const label = document.createElement('label');
    label.textContent = "No images";
    div.appendChild(img);
    div.appendChild(label);

    box.appendChild(div);

    return box;
}

function createResultBox(item, entry) {
    if ( item.type === 'image' ) {
        return createImageBox(item, entry);
    } else if ( item.type === 'link' ) {
        return createLinkBox(item, entry);
    } else if ( item.type === 'no-images' ) {
        return createNoImagesBox(entry);
    } else {
        throw new Error(`Unknown type: ${item.type}`);
    }
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
        for ( const [item, entry] of imageDatas ) {
            const box = createResultBox(item, entry);
            const columnIndex = argmin(columnHeights);
            columns[columnIndex].appendChild(box);
            columnHeights[columnIndex] = columns[columnIndex].clientHeight;
        }
    }

    return distributeImages;
})();
