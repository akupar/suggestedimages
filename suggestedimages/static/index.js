document.addEventListener("DOMContentLoaded", (event) => {
    const textbox = document.getElementById('title');
    if ( textbox.value !== "" ) {
        document.getElementById('title').select();
    }
});

document.querySelector('#wikt').addEventListener("change", (event) => {
    document.querySelector('form').submit();
});
