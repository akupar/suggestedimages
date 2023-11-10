document.addEventListener("DOMContentLoaded", (event) => {
    const textbox = document.getElementById('title');
    if ( textbox.value !== "" ) {
        document.getElementById('title').select();
    }
});
