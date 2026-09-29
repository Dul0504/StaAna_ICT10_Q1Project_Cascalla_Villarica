"""Logic for both pages: the shelf tag maker and the coffee counter."""

import random
import string

from pyscript import document

# ---------------------------------------------------------------
# Tag Maker (index.html)
# ---------------------------------------------------------------

# Two-letter shorthand for each stock category.
CATEGORY_CODES = {
    "Fresh Goods": "FG",
    "Drinks": "DR",
    "Single-Use": "SU",
    "Packing": "PK",
    "Supplies": "SP",
}


def letters_from_name(product_name):
    """Pull three letters out of the product name for the tag code."""
    letters = [char for char in product_name.upper() if char.isalpha()]
    while len(letters) < 3:
        letters.append("X")
    return "".join(letters[:3])


def digits_from_quantity(quantity_text):
    """Turn the stock count into a two-digit code, capped at 99."""
    try:
        quantity = int(quantity_text)
    except ValueError:
        quantity = 0
    quantity = max(0, min(quantity, 99))
    return f"{quantity:02d}"


def check_letter(seed_text):
    """Add one letter so two similar tags rarely land on the same code."""
    seed = sum(ord(char) for char in seed_text) + random.randint(0, 9)
    return string.ascii_uppercase[seed % 26]


def generate_tag(event):
    """Read the form and print a tag code below the perforation line."""
    category = document.getElementById("category").value
    product_name = document.getElementById("product_name").value.strip()
    quantity_text = document.getElementById("quantity").value

    output = document.getElementById("tag_output")

    if not product_name:
        output.innerHTML = "<p class='hint'>Type a product name first.</p>"
        return

    category_code = CATEGORY_CODES.get(category, "GN")
    name_code = letters_from_name(product_name)
    quantity_code = digits_from_quantity(quantity_text)
    tail = check_letter(category_code + name_code + quantity_code)

    tag_code = category_code + name_code + quantity_code + tail
    quantity_shown = quantity_text if quantity_text else "0"

    output.innerHTML = (
        f"<p class='tag-label'>{product_name}</p>"
        f"<p class='tag-code'>{tag_code}</p>"
        f"<p class='tag-meta'>{category}, {quantity_shown} on the shelf</p>"
    )


# ---------------------------------------------------------------
# Counter Receipt (receipt_generator.html)
# ---------------------------------------------------------------

# Prices in Philippine pesos, keyed by the checkbox id in the HTML.
PRICES = {
    "item1": 85,
    "item2": 135,
    "item3": 145,
    "item4": 95,
    "item5": 150,
}

NAMES = {
    "item1": "Barako Brew",
    "item2": "Ube Latte",
    "item3": "Salted Caramel Cold Brew",
    "item4": "Turmeric Ginger Tea",
    "item5": "Matcha Horchata",
}

# Philippine VAT rate applied to the subtotal.
TAX_RATE = 0.12


def ring_it_up(event):
    """Add up every checked item and show the line-by-line total."""
    output = document.getElementById("receipt_output")

    chosen = []
    total = 0
    for item_id, price in PRICES.items():
        box = document.getElementById(item_id)
        if box.checked:
            chosen.append((NAMES[item_id], price))
            total += price

    if not chosen:
        output.innerHTML = "<p class='hint'>Pick at least one drink.</p>"
        return

    rows = ""
    for name, price in chosen:
        rows += (
            "<div class='receipt-line'>"
            f"<span>{name}</span><span>&#8369;{price}</span>"
            "</div>"
        )

    tax = round(total * TAX_RATE, 2)
    grand_total = total + tax

    rows += (
        "<div class='receipt-line'>"
        f"<span>Subtotal</span><span>&#8369;{total:.2f}</span>"
        "</div>"
        "<div class='receipt-line'>"
        f"<span>Tax (12%)</span><span>&#8369;{tax:.2f}</span>"
        "</div>"
        "<div class='receipt-line receipt-total'>"
        f"<span>Total</span><span>&#8369;{grand_total:.2f}</span>"
        "</div>"
    )

    output.innerHTML = rows
