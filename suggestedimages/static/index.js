function setLanguageNameDisplay(text) {
    document.querySelector('#language-name').textContent = text;
}

function extractLanguageNameFromOptionLabel(optionValue) {
    // For example, 'Spanish [es]' –> 'Spanish'
    return optionValue.replace(/ \[.*\]/, '');
}

function handleChangedLanguage(languageInput) {
    const code = languageInput.value;
    const option = document.querySelector('#languages').querySelector('option[value="' + code + '"]');

    if ( option ) {
        setLanguageNameDisplay(extractLanguageNameFromOptionLabel(option.textContent));
        languageInput.setCustomValidity("");
    } else if ( code == "" ) {
        setLanguageNameDisplay("(same)");
        languageInput.setCustomValidity("");
    } else {
        setLanguageNameDisplay("");
        languageInput.setCustomValidity("Invalid language code");
    }
}

function focusTitleInputAndSelectText() {
    // The HTML autofocus attribute just focuses, but doesn't select the
    // text, so we have to do it ourselves.
    document.getElementById('title').select();
}

function titleInputIsEmpty() {
    return (document.getElementById('title').value.trim() === "");
}


function showLoadingIndicator() {
    document.querySelector('.gallery').style.display = 'block';
}

function hideGallery(isLoading) {
    document.querySelector('.loading-message').style.display = 'none';
}


document.addEventListener("DOMContentLoaded", (event) => {
    if ( ! titleInputIsEmpty() ) {
        focusTitleInputAndSelectText();
    }
    handleChangedLanguage(document.querySelector('#lang'));
});

document.forms[0].wikt.addEventListener("change", (event) => {
    document.forms[0].submit();
});

document.forms[0].addEventListener("submit", (event) => {
    // Disable empty inputs, so they are not submitted as parametres and clutter the url.
    if ( document.forms[0].lang.value === "" ) {
        document.forms[0].lang.setAttribute("disabled", true);
    }

    if ( document.forms[0].title.value === "" ) {
        document.forms[0].title.setAttribute("disabled", true);
    }

    showLoadingIndicator();
    // Hide the gallery temporarily to make the changing of results more visible.
    hideGallery();
});

document.forms[0].lang.addEventListener('input', (event) => handleChangedLanguage(event.target));
