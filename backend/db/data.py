# Dict that simulates the database
store = {
    "stock": {
        "last_updated": "2024-09-10 12:00:00",
        "beers": [
            {
                "name": "Corona",
                "price": 115,
                "quantity": 2
            },
            {
                "name": "Quilmes",
                "price": 120,
                "quantity": 0
            },
            {
                "name": "Club Colombia",
                "price": 110,
                "quantity": 3
            }
        ]
    },
    "orders": []
}

# global counter to keep track of order id
order_counter = 0