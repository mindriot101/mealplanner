#!/usr/bin/env python

from flask import Flask, render_template, request, redirect
import openfoodfacts
from itertools import islice

app = Flask(__name__)


class ProductPresenter:
    def __init__(self, raw):
        self.raw = raw

    def __str__(self):
        return f"{self.name} fat: {self.fat}, saturated fat: {self.saturated_fat}, protein: {self.protein}"

    @property
    def name(self):
        return self.raw.get("generic_name", "???")

    @property
    def fat(self):
        return self._nutrient("fat")

    @property
    def saturated_fat(self):
        return self._nutrient("saturated-fat")

    @property
    def protein(self):
        return self._nutrient("proteins")

    @property
    def nutrients(self):
        return self.raw["nutriments"]

    @property
    def image_url(self):
        return self.raw.get("image_url", "")

    def _nutrient(self, name):
        return self.nutrients.get(name, "???")
        # value = self.nutrients[f"{name}_value"]
        # unit = self.nutrients[f"{name}_unit"]
        # return "".join([value, unit])


def paginate(fn, params):
    seen = 0
    params["page"] = 1
    while True:
        res = fn(params)

        page_count = res["page_count"]

        yield from res["products"]

        seen += page_count
        params["page"] += 1
        if seen >= int(res["count"]):
            break


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    term = request.form["term"]
    search_params = {
        "search_terms": term,
        "sort_by": "popularity",
        "page_size": "10",
        "country": "united kingdom",
    }
    res = islice(paginate(openfoodfacts.products.advanced_search, search_params), 0, 10)
    products = (ProductPresenter(product) for product in res)
    return render_template("results.html", products=products)
