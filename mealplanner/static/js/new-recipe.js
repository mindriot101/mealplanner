'use strict';

window.addEventListener("load", (e) => {
  window.fetch("/api/ingredients").then((res) => {
    return res.json();
  }).then((data) => {
    const form = document.getElementById("form");
    const builder = new FormBuilder(form, data.ingredients);
    addButtonHandler(builder);
  });
});

class FormBuilder {
  constructor(form, ingredients) {
    this.form = form;
    this.ingredients = ingredients;
    this.numMemberships = 0;
    this.addInput("name", "Name");
    this.addMembership();
    this.submit = this.addSubmit();
  }

  addMembership() {
    this.addSelector(`ingredient-name-${this.numMemberships}`);
    this.addInput(`ingredient-count-${this.numMemberships}`, "Count", "number");
    this.numMemberships++;
  }

  addSelector(id) {
    const ip = document.createElement("select");
    ip.id = id;
    ip.name = id;

    this.ingredients.forEach((i) => {
      const option = document.createElement("option");
      option.value = i.name;
      option.text = i.name;
      ip.appendChild(option);
    });

    this.form.insertBefore(ip, this.submit);
  }

  addInput(key, label, type) {
    const ip = document.createElement("input");
    ip.id = key;
    ip.name = key;
    if (type) {
      ip.type = type;
    }
    const l = document.createElement("label");
    l.innerHTML = label;
    l.htmlFor = key;
    this.form.insertBefore(l, this.submit);
    this.form.insertBefore(ip, this.submit);
  }

  addSubmit() {
    const ip = document.createElement("input");
    ip.type = "submit";
    this.form.appendChild(ip);
    return ip;
  }

};

const addButtonHandler = (form) => {
  const button = document.getElementById("add-ingredient");
  button.addEventListener("click", (e) => {
    e.preventDefault();
    form.addMembership();
  });
};
