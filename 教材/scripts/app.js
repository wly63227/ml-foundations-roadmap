const menu=document.querySelector('.menu');
const narrow=window.matchMedia('(max-width:760px)');
function adapt(){if(menu)menu.open=!narrow.matches;}
adapt();narrow.addEventListener('change',adapt);
