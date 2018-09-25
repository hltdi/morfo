function ingresar() {
    form = document.getElementById("form");
    form.action = "login";
    form.submit();
}
function idioma(abbrev) {
    cargando();
    form = document.getElementById("form");
    form.labrev.value = abbrev;
/*    form.action = "anal"; */
    form.submit();
}
function analizar() {
    cargando();
    form = document.getElementById("form");
    form.action = "anal";
    form.submit();
}
function acerca() {
    form = document.getElementById("form");
    form.action = "acerca";
    form.submit();
}
function contacto() {
    form = document.getElementById("form");
    form.action = "contacto";
    form.submit();
}
function cargando() {
    document.getElementById("cargando").innerHTML = "<p></p><span class='cargando'>Cargando base de datos (podría tardarse)...</span><p></p>";
}
/* When the user clicks on the button, toggle between hiding and showing the dropdown content */
function mostrarDespleg() {
    menu = document.getElementById("menudespleg");
    list = menu.classList;
    list.toggle("show");
}
// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.despleg')) {
    var dropdowns = document.getElementsByClassName("contenido-despleg");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
