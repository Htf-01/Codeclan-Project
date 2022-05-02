from flask import Flask, Blueprint, render_template, redirect, request, session
from repositories import transaction_repository
from repositories import merchant_repository
from repositories import category_repository

from models.transaction import Transaction
from models.merchant import Merchant
from models.category import Category

transaction_blueprint = Blueprint("transactions", __name__)

# Index

@transaction_blueprint.route("/transactions")
def transactions():
    
    date = Transaction.session_date_display(session)
    date_values = Transaction.session_sql_format(session)
    transactions = transaction_repository.select_all(date_values)
    
    
    
    # breakpoint()

    return render_template("transactions/index.html", all_transactions = transactions, date = date)


# Create
@transaction_blueprint.route("/transactions/new", methods = ['GET'])
def new_transaction():
    merchants = merchant_repository.select_all_activated()
    categories = category_repository.select_all_activated()
    transactions = transaction_repository.select_all()
    return render_template("transactions/new.html", all_transactions = transactions, all_merchants = merchants, all_categories = categories)


# POST '/tasks'
@transaction_blueprint.route("/transactions/new", methods = ['POST'])
def create_transaction():
    date = request.form['date']
    
    merchant = merchant_repository.select_by_name(request.form['merchant'])
    category = category_repository.select_by_name(request.form['category'])
    
    if merchant == False:
        merchant = merchant_repository.select(merchant_repository.save(Merchant(request.form['merchant'])))
    
    if category == False:
        category = category_repository.select(category_repository.save(Category(request.form['category'])))
        
    amount = (request.form['amount_pound']) + (request.form['amount_pence'])
    
    transaction = Transaction(date, merchant,amount,category)

    transaction_repository.save(transaction)
    return redirect('/transactions')

# Show

# Edit
@transaction_blueprint.route("/transactions/<id>/edit", methods = ['GET'])
def edit_transaction(id):
    transaction = transaction_repository.select(id)
    merchants = merchant_repository.select_all_activated()
    categories = category_repository.select_all_activated()
    transactions = transaction_repository.select_all()
    return render_template('transactions/edit.html', transaction = transaction, all_transactions = transactions, all_merchants = merchants, all_categories = categories)

# Update
@transaction_blueprint.route("/transactions/<id>", methods = ['POST'])
def update_transactions(id):
    date = request.form['date']
    
    merchant = merchant_repository.select_by_name(request.form['merchant'])
    category = category_repository.select_by_name(request.form['category'])
    
    if merchant == False:
        merchant = merchant_repository.select(merchant_repository.save(Merchant(request.form['merchant'])))
    
    if category == False:
        category = category_repository.select(category_repository.save(Category(request.form['category'])))
        
        
        
    budget_id = transaction_repository.select_budget((Transaction.string_to_date(date)))
    
    if request.form['amount_pence'] == '0':
        amount_pence = '00'
    else:
        amount_pence = request.form['amount_pence']  
    
    amount = (request.form['amount_pound']) + amount_pence
    
    transaction = Transaction(date, merchant,amount,category, budget_id, id)

    transaction_repository.update(transaction)
    return redirect('/transactions')



# Delete
@transaction_blueprint.route("/transactions/<id>/delete", methods = ['GET'])
def delete_confrim(id):
    transaction = transaction_repository.select(id)
    merchants = merchant_repository.select_all_activated()
    categories = category_repository.select_all_activated()
    transactions = transaction_repository.select_all()
    return render_template('transactions/delete.html', transaction = transaction, all_transactions = transactions, all_merchants = merchants, all_categories = categories)

@transaction_blueprint.route("/transactions/<id>/delete", methods = ['POST'])
def delete_transaction(id):

    transaction_repository.delete(id)
    return redirect('/transactions')


##################################################

# SESSION HANDING - SORT

@transaction_blueprint.route("/transactions/sort", methods = ['POST'])
def sort_transactions():
    
    # Which button was pressed
    sort = request.form['button']
    Transaction.session_sort(session,sort)
    
    return redirect('/transactions')

#  SESSION HANDLING - Month View

@transaction_blueprint.route("/transactions/nextmonth")
def transactions_next_month():
    
    Transaction.session_increment(session)
    
    return redirect('/transactions')

@transaction_blueprint.route("/transactions/previousmonth")
def transactions_previous_month():
    
    Transaction.session_decrement(session)
    
    return redirect('/transactions')

@transaction_blueprint.route("/transactions/currentmonth")
def transactions_current_month():
    
    Transaction.session_current(session)
    
    return redirect('/transactions')

@transaction_blueprint.route("/transactions/month", methods = ['POST'])
def transactions_select_month():
    
    date_string = request.form['date']
    
    Transaction.session_select(session,date_string)
    
    return redirect('/transactions')
