'use strict'

document.addEventListener("DOMContentLoaded", function() {
    
    if (window.matchMedia("(max-width: 575.99px)").matches) {

        const container = document.getElementsByClassName('add-points')[0];
        const target = container.querySelectorAll("[data-switch-target]");
        const array = ['one', 'two', 'three', 'four', 'five', 'six'];

        target[0].addEventListener('click', switchContainer);
        target[2].addEventListener('click', switchContainer);
        target[4].addEventListener('click', switchContainer);

        function switchContainer() {
            const x = this;
            const dataNumber = x.getAttributeNode("data-switch-target").value;
            const targetNumber = array.indexOf(dataNumber);            

            target[targetNumber].style.display = "none";
            target[targetNumber + 1].style.display = "flex";

            for (let i = 0; i < array.length; i++) {

                if (i !== targetNumber && i !== targetNumber + 1) {
                    target[i].style.display = "flex";
                    target[++i].style.display = "none";
                }
            }
        }
    }
});
