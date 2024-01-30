from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask import Blueprint, render_template
from .models import Transaction, User
from . import db
import json
import re

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        transactionTitle = request.form.get("transactionTitle")
        transactionType = request.form.get("transactionType")
        transactionAmount = request.form.get("amount")

        if (
            transactionAmount is None
            or transactionAmount.strip() == ""
            or transactionTitle is None
            or transactionTitle.strip() == ""
        ):
            flash("No field can be left blank", category="error")
        elif transactionAmount == 0:
            flash("Amount can not be 0", category="error")
        elif contains_invalid_chars(transactionAmount):
            flash(
                "Please enter an amount using only the following characters: digits (0-9), dash (- (as first char)), dot (.), and comma (,). Any other characters are not allowed.",
                category="error",
            )
        elif transactionAmount[0] == "-" and len(transactionAmount) < 2:
            flash("Please enter valid value", category="error")
        else:
            if float(transactionAmount) < 0:
                transactionType = "expanse"
            new_transaction = Transaction(
                float(amount_parser(transactionAmount)),
                date=None,
                title=transactionTitle,
                type=transactionType,
                user_id=current_user.id,
            )
            db.session.add(new_transaction)
            db.session.commit()

    user_balance = round(balance(current_user.id), 2)
    return render_template("home.html", user=current_user, balance=user_balance)


@views.route("/delete-transaction", methods=["POST"])
def delete_transaction():
    transaction = json.loads(request.data)
    transactionId = transaction["transactionId"]
    transaction = Transaction.query.get(transactionId)
    if transaction:
        if transaction.user_id == current_user.id:
            db.session.delete(transaction)
            db.session.commit()

    return jsonify({})


def balance(user_id):
    user = User.query.get(user_id)
    transactions = Transaction.query.filter_by(user_id=user.id).all()
    balance = 0
    for transaction in transactions:
        if transaction.type == "income":
            balance += transaction.amount
        else:
            transaction.type == "expense"
            if transaction.amount < 0:
                balance += transaction.amount
            else:
                balance -= transaction.amount

    return balance


def amount_parser(input):
    clean_input = input.replace(",", ".")
    if float(clean_input) < 0:
        if clean_input[0] == "-" and len(clean_input) > 1:
            return clean_input[1:]
    else:
        return clean_input


def field_check(value):
    if value is None or value.strip() == "":
        flash("Field must not be empty", category="error")
    else:
        return value


def contains_invalid_chars(input):
    pattern = r"^-?\d*(?:[.,]\d*)?$"
    match = re.search(pattern, input)
    return match is None
