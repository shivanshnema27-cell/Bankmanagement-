import streamlit as st
from pathlib import Path
import json
import random
import string


class Bank:
    database = 'database.json'
    data = []

    # Load existing data
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
    except Exception as err:
        st.error(f"Error loading DB: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def __account():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        id = alpha + digits
        random.shuffle(id)
        return "".join(id)

    # Create Account
    def createaccount(self, name, email, phone, pin):
        if len(pin) != 4 or not pin.isdigit():
            return "PIN must be 4 digits"

        if len(phone) != 10 or not phone.isdigit():
            return "Phone must be 10 digits"

        d = {
            "name": name,
            "email": email,
            "phone_no": int(phone),
            "pin": int(pin),
            "Account_no": Bank.__account(),
            "money": 0
        }

        Bank.data.append(d)
        Bank.__update()
        return d["Account_no"]

    # Deposit Money
    def deposit(self, acc, pin, amt):
        user = [i for i in Bank.data if i["Account_no"] == acc and i["pin"] == pin]

        if not user:
            return "User not found"

        if amt <= 0:
            return "Invalid amount"

        user[0]["money"] += amt
        Bank.__update()
        return "Amount Deposited"

    # Withdraw
    def withdraw(self, acc, pin, amt):
        user = [i for i in Bank.data if i["Account_no"] == acc and i["pin"] == pin]

        if not user:
            return "User not found"

        if amt > user[0]["money"]:
            return "Low balance"

        user[0]["money"] -= amt
        Bank.__update()
        return "Amount Withdrawn"

    # Fetch User Details
    def details(self, acc, pin):
        user = [i for i in Bank.data if i["Account_no"] == acc and i["pin"] == pin]

        if not user:
            return None

        return user[0]

    # Delete Account
    def delete(self, acc, pin):
        for i in Bank.data:
            if i["Account_no"] == acc and i["pin"] == pin:
                Bank.data.remove(i)
                Bank.__update()
                return "Account deleted"

        return "User not found"


# -----------------------------------------
# STREAMLIT UI
# -----------------------------------------

st.set_page_config(page_title="Bank Management System", page_icon="🏦", layout="centered")
st.title("🏦 Bank Management System")

bank = Bank()

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "View User Details",
        "Delete Account",
        
    ]
)

# ---------------- CREATE ACCOUNT ------------------

if menu == "Create Account":
    st.header("Create New Account")

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    phone = st.text_input("Enter Phone Number")
    pin = st.text_input("Enter 4-Digit PIN", type="password")

    if st.button("Create Account"):
        acc = bank.createaccount(name, email, phone, pin)
        if "PIN" in acc or "Phone" in acc:
            st.error(acc)
        else:
            st.success(f"Account Created Successfully!")
            st.info(f"Your Account Number: **{acc}**")

# ---------------- DEPOSIT ------------------

if menu == "Deposit Money":
    st.header("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.number_input("PIN", step=1)
    amt = st.number_input("Amount", step=1)

    if st.button("Deposit"):
        result = bank.deposit(acc, pin, amt)
        st.success(result) if "Deposited" in result else st.error(result)

# ---------------- WITHDRAW ------------------

if menu == "Withdraw Money":
    st.header("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.number_input("PIN", step=1)
    amt = st.number_input("Amount", step=1)

    if st.button("Withdraw"):
        result = bank.withdraw(acc, pin, amt)
        st.success(result) if "Withdrawn" in result else st.error(result)

# ---------------- USER DETAILS ------------------

if menu == "View User Details":
    st.header("User Details")

    acc = st.text_input("Account Number")
    pin = st.number_input("PIN", step=1)

    if st.button("Get Details"):
        details = bank.details(acc, pin)
        if details:
            st.json(details)
        else:
            st.error("User not found")

# ---------------- DELETE ACCOUNT ------------------

if menu == "Delete Account":
    st.header("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.number_input("PIN", step=1)

    if st.button("Delete"):
        result = bank.delete(acc, pin)
        if result == "Account deleted":
            st.success(result)
        else:
            st.error(result)

