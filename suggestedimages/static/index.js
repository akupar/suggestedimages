document.addEventListener("DOMContentLoaded", (event) => {
    const textbox = document.getElementById('title');
    if ( textbox.value !== "" ) {
        document.getElementById('title').select();
    }
});

document.querySelector('#wikt').addEventListener("change", (event) => {
    console.log("changed");
    document.querySelector('form').submit();
});
