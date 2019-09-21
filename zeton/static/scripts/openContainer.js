'use strict'

document.addEventListener("DOMContentLoaded", function () {

    const viewport = window.matchMedia('(max-width: 575.99px)');
    const container = document.getElementsByClassName('add-points')[0];
    const target = container.querySelectorAll("[data-switch-target]");
    const array = ['one', 'two', 'three', 'four', 'five', 'six'];

    function switcher() {
        target[0].addEventListener('click', switchContainer);
        target[2].addEventListener('click', switchContainer);
        target[4].addEventListener('click', switchContainer);

        function switchContainer() {
            const x = this;
            const dataNumber = x.getAttributeNode("data-switch-target").value;
            const targetNumber = array.indexOf(dataNumber);

            if (viewport.matches) {
                //console.log("mały ekran2");
                target[targetNumber].style.display = "none";
                target[targetNumber + 1].style.display = "flex";

                for (let i = 0; i < array.length; i++) {

                    if (i !== targetNumber && i !== targetNumber + 1) {
                        target[i].style.display = "flex";
                        target[++i].style.display = "none";
                    }
                }

            } else {
                //console.log("duży ekran2");
                freshLarge();
            }
        }
    }

    function freshLarge() {
        for (let i = 0; i < array.length; i++) {
            target[i].style.display = "flex";
        }
    }

    function freshSmall() {
        for (let i = 0; i < array.length; i++) {
            target[i].style.display = "flex";
            target[++i].style.display = "none";
        }
    }

    function screenTest(viewport) {
        if (viewport.matches) {
            //console.log("mały ekran");
            freshSmall();
            switcher();            

        } else {
            //console.log("duży ekran");
            freshLarge();
        }
    }

    screenTest(viewport);

    viewport.addListener(screenTest);

});

/*
if (viewport.matches) {
        console.log('jest mały');
        switcher();
    }

    
*/