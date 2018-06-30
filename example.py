from utils.sql import query

# Good idea to assign columns names to variables,
# to avoid typos and make it easier to search code
NAME = 'name'
ID = 'id'
QUANTITY = 'quantity'
GOOD_ID = 'good_id'
CLIENT_NAME = 'client_name'
STOCK = 'stock'
TOTAL_SALES_QUANTITY = 'total_sales_quantity'

# Initialize schema:
query('goods/__init__.sql')
query('sales/__init__.sql')

# Create goods:
[good1] = query('goods/create.sql', {
    NAME: 'A red good',
    STOCK: 10
})
[good2] = query('goods/create.sql', {
    NAME: 'A green good',
    STOCK: 10
})
assert(good1[NAME] == 'A red good')
assert(good1[ID] > 0)
assert(good2[NAME] == 'A green good')
assert(good2[ID] > 0)

# Find goods:
goods = query('goods/by_name.sql', {NAME: r'%green%'})
assert(goods[0] == good2)

# Create sales:
query('sales/create.sql', {
    GOOD_ID: good1[ID],
    QUANTITY: 1,
    CLIENT_NAME: 'Client1'
})
query('sales/create.sql', {
    GOOD_ID: good1[ID],
    QUANTITY: 2,
    CLIENT_NAME: 'Client2'
})
query('sales/create.sql', {
    GOOD_ID: good1[ID],
    QUANTITY: 3,
    CLIENT_NAME: 'Client3'
})

# Quantity on sale should have been updated automatically by trigger:
[good1] = query('goods/by_id.sql', good1)
assert(good1[STOCK] == 4)


totals = query('sales/total_sales_per_good.sql')
assert(totals == [
    {ID: good2[ID], NAME: 'A green good', TOTAL_SALES_QUANTITY: None},
    {ID: good1[ID], NAME: 'A red good', TOTAL_SALES_QUANTITY: 6},
])