document.addEventListener("DOMContentLoaded", (event) => {
    const textbox = document.getElementById('title');
    if ( textbox.value !== "" ) {
        document.getElementById('title').select();
    }
});

document.querySelector('#wikt').addEventListener("change", (event) => {
    document.forms[0].submit();
});


document.forms[0].addEventListener("submit", (event) => {
    // Disable empty inputs, so it is not submitted as a parametre and clutter the url.
    if ( document.forms[0].lang.value === "" ) {
        document.forms[0].lang.setAttribute("disabled", true);
    }

    if ( document.forms[0].title.value === "" ) {
        document.forms[0].title.setAttribute("disabled", true);
    }

    document.querySelector('.gallery').style.display = 'none';
    document.querySelector('.loading-message').style.display = 'block';
});
