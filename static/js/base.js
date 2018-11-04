"use strict";
/*
* Counts characters in post textarea
*
* See-Also:
* https://codepen.io/ogiansouza/pen/KdepVp
* https://stackoverflow.com/questions/19586137/addeventlistener-using-for-loop-and-passing-values
* */

// Define the divs containing input textareas
var elements = [document.getElementById("submit_post_sidebar"), document.getElementById("submit_post_center")];

// Counts characters in textarea, from: https://codepen.io/ogiansouza/pen/KdepVp
function calculateCharacters(textarea, counter) {
    var maxLength = textarea.getAttribute("maxlength");
    var characters = textarea.value.length;
    counter.innerHTML = maxLength - characters;
}

// For each element, attach an event listener for 'oninput' because 'onkeyup' doesn't work on android
// And use onbind, because I don't know what the best way to get around
// this problem is https://stackoverflow.com/questions/19586137/addeventlistener-using-for-loop-and-passing-values
elements.forEach(function (element) {
    var textarea = element.querySelector("textarea[name='post']");
    var counter = element.querySelector(".counter");
    textarea.addEventListener(
        "input",
        calculateCharacters.bind(this, textarea, counter)
    );
});
