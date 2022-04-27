# Imports
from db.run_sql import run_sql
from models.merchant import Merchant

# CREATE
###############################################################
def save(merchant):
    sql = "INSERT INTO merchants(name,activated,filtered) VALUES ( %s,%s,%s ) RETURNING id"
    values = [merchant.name, merchant.activated, merchant.filtered]
    results = run_sql( sql, values )
    merchant.id = results[0]['id']

# READ
###############################################################
def select_all():
    merchants = []

    sql = "SELECT * FROM merchants"
    results = run_sql(sql)

    for row in results:
        merchant = Merchant(row['name'], row['activated'], row['filtered'], row['id'])
        merchants.append(merchant)
    return merchants

def select(id):
    merchant = None
    sql = "SELECT * FROM merchants WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        merchant = Merchant(result['name'], result['activated'], result['filtered'], result['id'])
    return merchant

# UPDATE
###############################################################
def update(merchant):
    sql = "UPDATE merchants SET (name,activated,filtered) = ( %s,%s,%s ) WHERE id = %s"
    values = [merchant.name, merchant.activated, merchant.filtered, merchant.id]
    run_sql(sql, values)
    
# DELETE
###############################################################
def delete_all():
    sql = "DELETE FROM merchants"
    run_sql(sql)