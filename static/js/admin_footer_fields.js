document.addEventListener('DOMContentLoaded', function () {
    const sectionSelect = document.querySelector('#id_section');
    const libelle = document.querySelector('.field-libelle');
    const route = document.querySelector('.field-router');
    const description = document.querySelector('.field-description_email');
    const mode = document.querySelector('.field-mode_payement');

    if (sectionSelect) {
        const display = libelle.style.display
        sectionSelect.onchange = function() {
            const selectedText = this.options[this.selectedIndex].text;
             if(selectedText === 'presentation'){
                libelle.style.display = "none";
                route.style.display = "none";
                description.style.display = "none";
                mode.style.display = "none";
            }else if(selectedText === 'compagnie'){
                libelle.style.display = display;
                route.style.display = display;
                description.style.display = "none";
                mode.style.display = "none";
            }else if(selectedText === 'services'){
                libelle.style.display = display;
                route.style.display = "none";
                description.style.display = "none";
                mode.style.display = "none";
            }else if(selectedText === 'espace_client'){
                libelle.style.display = display;
                route.style.display = "none";
                description.style.display = "none";
                mode.style.display = "none";
            }else if(selectedText === 'mail'){
                libelle.style.display = display;
                route.style.display = "none";
                description.style.display = display;
                mode.style.display = display;
            }
        };
    }
});