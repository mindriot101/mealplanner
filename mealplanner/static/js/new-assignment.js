'use strict';

window.addEventListener("load", (e) => {
  window.fetch("/api/recipes").then((res) => {
    return res.json();
  }).then((data) => {
    const form = document.getElementById("form");
    const builder = new FormBuilder(form, data.recipes);
  });
});
