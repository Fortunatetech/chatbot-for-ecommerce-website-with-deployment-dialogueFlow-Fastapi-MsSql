import pyodbc

# Set your connection parameters
server = 'DESKTOP-PBU1VUC\\SQLEXPRESS'
database = 'pandeyji_eatery'
username = 'root'
password = 'root'

# Create a connection
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes'
connection = pyodbc.connect(connection_string)

# Function to call the SQL Server stored procedure and insert an order item


def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = connection.cursor()

        # Calling the stored procedure
        cursor.execute("{CALL insert_order_item (?, ?, ?)}",
                       (food_item, quantity, order_id))

        # Committing the changes
        connection.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except pyodbc.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        connection.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        connection.rollback()

        return -1

 # Function to insert a record into the order_tracking table


def insert_order_tracking(order_id, status):
    cursor = connection.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (?, ?)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    connection.commit()

    # Closing the cursor
    cursor.close()


def get_total_order_price(order_id):
    cursor = connection.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result

# Function to get the next available order_id


def get_next_order_id():
    cursor = connection.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1

# Function to fetch the order status from the order_tracking table


def get_order_status(order_id):
    cursor = connection.cursor()

    # Executing the SQL query to fetch the order status
    query = "SELECT status FROM order_tracking WHERE order_id = ? "
    cursor.execute(query, order_id)

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result:
        return result[0]
    else:
        return None


if __name__ == "__main__":
    # Example usage
    # insert_order_item('Samosa', 3, get_next_order_id())
    # insert_order_tracking(get_next_order_id(), "in progress")
    print(get_next_order_id())

 # Close the connection
# connection.close()
