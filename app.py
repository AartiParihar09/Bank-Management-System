from flask import Flask, render_template, request

import bank


app = Flask(__name__)


# ---------------- HOME ----------------

@app.route("/")
def home():

    return render_template(
        "index.html",
        message=None
    )


# ---------------- OPEN ACCOUNT ----------------

@app.route("/open-account", methods=["POST"])
def open_account():

    name = request.form.get(
        "name",
        ""
    )

    account_type = request.form.get(
        "account_type",
        ""
    )

    try:
        balance = float(
            request.form.get("balance", "")
        )

    except ValueError:

        return render_template(
            "index.html",
            message="Invalid initial deposit amount."
        )

    success, message, account_number = bank.create_account(
        name,
        account_type,
        balance
    )

    if success:

        message = (
            f"{message} "
            f"Account Number: {account_number}"
        )

    return render_template(
        "index.html",
        message=message
    )


# ---------------- VIEW ACCOUNT ----------------

@app.route("/view-account", methods=["POST"])
def view_account():

    try:
        account_number = int(
            request.form.get(
                "account_number",
                ""
            )
        )

    except ValueError:

        return render_template(
            "index.html",
            message="Invalid account number."
        )

    success, message, account = bank.get_account(
        account_number
    )

    if not success:

        return render_template(
            "index.html",
            message=message
        )

    return render_template(
        "index.html",
        message=message,
        account=account,
        account_number=account_number
    )


# ---------------- DEPOSIT ----------------

@app.route("/deposit", methods=["POST"])
def deposit():

    try:
        account_number = int(
            request.form.get(
                "account_number",
                ""
            )
        )

        amount = float(
            request.form.get(
                "amount",
                ""
            )
        )

    except ValueError:

        return render_template(
            "index.html",
            message="Please enter valid numeric values."
        )

    success, message = bank.deposit(
        account_number,
        amount
    )

    return render_template(
        "index.html",
        message=message
    )


# ---------------- WITHDRAW ----------------

@app.route("/withdraw", methods=["POST"])
def withdraw():

    try:
        account_number = int(
            request.form.get(
                "account_number",
                ""
            )
        )

        amount = float(
            request.form.get(
                "amount",
                ""
            )
        )

    except ValueError:

        return render_template(
            "index.html",
            message="Please enter valid numeric values."
        )

    success, message = bank.withdraw(
        account_number,
        amount
    )

    return render_template(
        "index.html",
        message=message
    )


# ---------------- TRANSFER ----------------

@app.route("/transfer", methods=["POST"])
def transfer():

    try:
        sender_number = int(
            request.form.get(
                "sender_account",
                ""
            )
        )

        receiver_number = int(
            request.form.get(
                "receiver_account",
                ""
            )
        )

        amount = float(
            request.form.get(
                "amount",
                ""
            )
        )

    except ValueError:

        return render_template(
            "index.html",
            message="Please enter valid numeric values."
        )

    success, message = bank.transfer(
        sender_number,
        receiver_number,
        amount
    )

    return render_template(
        "index.html",
        message=message
    )


# ---------------- TRANSACTION HISTORY ----------------

@app.route("/history", methods=["POST"])
def history():

    try:
        account_number = int(
            request.form.get(
                "account_number",
                ""
            )
        )

    except ValueError:

        return render_template(
            "index.html",
            message="Invalid account number."
        )

    success, message, transaction_history = (
        bank.get_transaction_history(
            account_number
        )
    )

    if not success:

        return render_template(
            "index.html",
            message=message
        )

    return render_template(
        "index.html",
        message=message,
        history=transaction_history,
        history_account_number=account_number
    )


# ---------------- ACCOUNT SUMMARY ----------------

@app.route("/summary", methods=["POST"])
def summary():

    try:
        account_number = int(
            request.form.get(
                "account_number",
                ""
            )
        )

    except ValueError:

        return render_template(
            "index.html",
            message="Invalid account number."
        )

    success, message, summary_data = (
        bank.get_account_summary(
            account_number
        )
    )

    if not success:

        return render_template(
            "index.html",
            message=message
        )

    return render_template(
        "index.html",
        message=message,
        summary=summary_data
    )


# ---------------- RUN FLASK ----------------

if __name__ == "__main__":

    app.run(debug=True)