from flask import Flask, request, jsonify, render_template
import cx_Oracle
import os
from flask_cors import CORS

# Create the Flask app instance
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Initialize Oracle Client
try:
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient\19\instantclient_19_24")  # Update path
    print("Oracle Client is initialized")
except Exception as e:
    print("Failed to initialize Oracle Client:", e)

# Connect to Oracle DB
conn = cx_Oracle.connect("kshivaku/thadasha@artemis.vsnet.gmu.edu:1521/vse18c.vsnet.gmu.edu")
cursor = conn.cursor()

# Serve static files (index.html, script.js, style.css)
@app.route('/')
def serve_index():
    # Render the index.html template so that Jinja can process it
    return render_template('index.html')

# Example endpoint to fetch data from the selected table
@app.route('/get_table_data/<table_name>', methods=['GET'])
def get_table_data(table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries
        data = [dict(zip(columns, row)) for row in rows]
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_record_data/<table_name>/<record_id>', methods=['GET'])
def get_record_data(table_name, record_id):
    try:
        # Split the record_id into components for composite keys
        record_id_parts = record_id.split(',')
        
        if table_name == 'manufOrders' and len(record_id_parts) == 3:
            item, manuf = record_id_parts[0], record_id_parts[1]
            cursor.execute(f"SELECT * FROM manufOrders WHERE ITEM = :1 AND MANUF = :2", (item, manuf))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

        # Handle other cases similarly
        elif table_name == 'shipOrders' and len(record_id_parts) == 5:
            item = record_id_parts[0]        # First element: ITEM
            recipient = record_id_parts[2]   # Third element: RECIPIENT
            sender = record_id_parts[3]      # Fourth element: SENDER
            shipper = record_id_parts[4]     # Fifth element: SHIPPER

            cursor.execute(f"SELECT * FROM shipOrders WHERE ITEM = :1 AND SENDER = :2 AND RECIPIENT = :3 AND SHIPPER = :4", (item, sender, recipient, shipper))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

        elif table_name == 'supplyOrders' and len(record_id_parts) == 3:
            item, supplier = record_id_parts[0], record_id_parts[2]

            cursor.execute(f"SELECT * FROM supplyOrders WHERE ITEM = :1 AND SUPPLIER = :2", (item, supplier))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 
                
        elif table_name == 'customerDemand' and len(record_id_parts) == 3:
            customer,item, qty = record_id_parts[0],record_id_parts[1], record_id_parts[2]

            cursor.execute(f"SELECT * FROM customerDemand WHERE CUSTOMER = :1 AND ITEM = :2 AND QTY = :3", (customer,item, qty))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

        elif table_name == 'shippingPricing' and len(record_id_parts) == 9:
            shipper, fromLoc, toLoc = record_id_parts[7], record_id_parts[4], record_id_parts[8]

            cursor.execute(f"SELECT * FROM shippingPricing WHERE SHIPPER = :1 AND FROMLOC = :2 AND TOLOC = :3", (shipper, fromLoc,toLoc))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

        elif table_name == 'manufUnitPricing' and len(record_id_parts) == 4:
            manuf, prodItem = record_id_parts[0], record_id_parts[2]
            cursor.execute(f"SELECT * FROM manufUnitPricing WHERE MANUF = :1 AND PRODITEM = :2", (manuf, prodItem))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

        elif table_name == 'manufDiscounts' and len(record_id_parts) == 3:
            manuf = record_id_parts[2]
            cursor.execute(f"SELECT * FROM manufDiscounts WHERE MANUF = :1", (manuf,))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

        elif table_name == 'supplyUnitPricing' and len(record_id_parts) == 3:
            item, supplier = record_id_parts[0], record_id_parts[2]
            cursor.execute(f"SELECT * FROM supplyUnitPricing WHERE ITEM = :1 AND SUPPLIER = :2", (item,supplier))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

        # Default case if not matched (or for other tables with similar composite keys)

        elif table_name == 'supplierDiscounts' and len(record_id_parts) == 5:
            supplier = record_id_parts[4]
            cursor.execute(f"SELECT * FROM supplierDiscounts WHERE SUPPLIER = :1", (supplier,))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

        # Default case if not matched (or for other tables with similar composite keys)
        elif table_name == 'billOfMaterials' and len(record_id_parts) == 3:
            matItem,prodItem = record_id_parts[0],record_id_parts[1]
            cursor.execute(f"SELECT * FROM billOfMaterials WHERE matitem = :1 and PRODITEM = :2", (matItem,prodItem))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

         # Default case if not matched (or for other tables with similar composite keys)
        elif table_name == 'busEntities' and len(record_id_parts) == 6:
            entity = record_id_parts[2]
            cursor.execute(f"SELECT * FROM busEntities WHERE ENTITY = :1", (entity,))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404


         # Default case if not matched (or for other tables with similar composite keys)
        elif table_name == 'items' and len(record_id_parts) == 2:
            item = record_id_parts[0]
            cursor.execute(f"SELECT * FROM items WHERE item = :1", (item,))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return jsonify(dict(zip(columns, row)))
            else:
                return jsonify({"error": "Record not found"}), 404

        else:
            return jsonify({"error": "Table or record ID format is incorrect"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/create_record/<table_name>', methods=['POST'])
def create_record(table_name):
    try:
        data = request.json
        columns = ", ".join(data.keys())
        values = ", ".join([f"'{v}'" for v in data.values()])
        
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_record/<table_name>/<record_id>', methods=['POST'])
def update_record(table_name, record_id):
    try:
        # Split the record_id for composite keys
        record_id_parts = record_id.split(',')
        
        if table_name == 'manufOrders' and len(record_id_parts) == 3:
            item, manuf = record_id_parts[0], record_id_parts[1]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE manufOrders SET {set_clause} WHERE ITEM = :1 AND MANUF = :2", (item, manuf))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'shipOrders' and len(record_id_parts) == 5:
            item = record_id_parts[0]        # First element: ITEM
            recipient = record_id_parts[2]   # Third element: RECIPIENT
            sender = record_id_parts[3]      # Fourth element: SENDER
            shipper = record_id_parts[4]     # Fifth element: SHIPPER
            
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE shipOrders SET {set_clause} WHERE ITEM = :1 AND SENDER = :2 AND RECIPIENT = :3 AND SHIPPER = :4", (item, sender, recipient, shipper))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'supplyOrders' and len(record_id_parts) == 3:
            item, supplier = record_id_parts[0], record_id_parts[2]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE supplyOrders SET {set_clause} WHERE ITEM = :1 AND SUPPLIER = :2", (item, supplier))
            conn.commit()
            return jsonify({"success": True})

        # Handle other cases similarly
        elif table_name == 'customerDemand' and len(record_id_parts) == 3:
            customer, item, qty = record_id_parts[0], record_id_parts[1], record_id_parts[2]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE customerDemand SET {set_clause} WHERE CUSTOMER = :1 AND ITEM = :2 AND QTY = :3", (customer,item, qty))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'shippingPricing' and len(record_id_parts) == 9:
            shipper, fromLoc, toLoc = record_id_parts[7], record_id_parts[4], record_id_parts[8]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE shippingPricing SET {set_clause} WHERE SHIPPER = :1 AND FROMLOC = :2 AND TOLOC = :3", (shipper,fromLoc, toLoc))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'manufUnitPricing' and len(record_id_parts) == 4:
            manuf, prodItem = record_id_parts[0], record_id_parts[2]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE manufUnitPricing SET {set_clause} WHERE MANUF = :1 AND PRODITEM = :2", (manuf,prodItem))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'manufDiscounts' and len(record_id_parts) == 3:
            manuf = record_id_parts[2]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE manufDiscounts SET {set_clause} WHERE MANUF = :1", (manuf,))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'supplyUnitPricing' and len(record_id_parts) == 3:
            item, supplier = record_id_parts[0], record_id_parts[2]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE supplyUnitPricing SET {set_clause} WHERE ITEM = :1 AND SUPPLIER = :2", (item,supplier))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'supplierDiscounts' and len(record_id_parts) == 5:
            supplier = record_id_parts[4]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE supplierDiscounts SET {set_clause} WHERE supplier = :1", (supplier,))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'billOfMaterials' and len(record_id_parts) == 3:
            matItem,prodItem = record_id_parts[0],record_id_parts[1]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE billOfMaterials SET {set_clause} WHERE MATITEM = :1 AND PRODITEM = :2", (matItem,prodItem))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'busEntities' and len(record_id_parts) == 6:
            entity = record_id_parts[2]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE busEntities SET {set_clause} WHERE ENTITY = :1", (entity,))
            conn.commit()
            return jsonify({"success": True})

        elif table_name == 'items' and len(record_id_parts) == 2:
            item = record_id_parts[0]
            data = request.json
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
            cursor.execute(f"UPDATE items SET {set_clause} WHERE ITEM = :1", (item,))
            conn.commit()
            return jsonify({"success": True})

        
        # Default case if not matched (or for other tables with composite keys)
        else:
            return jsonify({"error": "Table or record ID format is incorrect"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_record/<table_name>/<record_id>', methods=['DELETE'])
def delete_record(table_name, record_id):
    try:
        print(f"Attempting to delete from table: {table_name} with record_id: {record_id}")  # Debugging line
        
        # Split the record_id into parts (assuming it's comma-separated for composite key)
        record_id_parts = record_id.split(',')
        
        # Debugging output to see the split result
        print(f"Parsed record_id_parts: {record_id_parts}")
        
        # Handle deletion for 'manufOrders' table with composite primary key (ITEM and MANUF)
        if table_name == 'manufOrders' and len(record_id_parts) >= 2:
            item, manuf = record_id_parts[0], record_id_parts[1]  # Extract ITEM and MANUF
            print(f"Deleting manufOrders record where ITEM = {item}, MANUF = {manuf}")  # Debugging line
            
            # Perform the deletion query using ITEM and MANUF as composite key
            cursor.execute("""DELETE FROM manufOrders WHERE ITEM = :1 AND MANUF = :2""", (item, manuf))
            conn.commit()
            
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404

        # Handle deletion for 'shipOrders' table
        elif table_name == 'shipOrders' and len(record_id_parts) == 5:
            item = record_id_parts[0]        # First element: ITEM
            recipient = record_id_parts[2]   # Third element: RECIPIENT
            sender = record_id_parts[3]      # Fourth element: SENDER
            shipper = record_id_parts[4]     # Fifth element: SHIPPER
            
            print(f"Deleting shipOrders record where ITEM = {item}, SENDER = {sender}, RECIPIENT = {recipient}, SHIPPER = {shipper}")
            
            cursor.execute("""DELETE FROM shipOrders WHERE ITEM = :1 AND SENDER = :2 AND RECIPIENT = :3 AND SHIPPER = :4""",
                           (item, sender, recipient, shipper))
            conn.commit()
            
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404

        # Handle deletion for 'supplyOrders' table
        elif table_name == 'supplyOrders' and len(record_id_parts) == 3:
            item, supplier = record_id_parts[0], record_id_parts[2]  # Extract ITEM and SUPPLIER
            print(f"Deleting supplyOrders record where ITEM = {item}, SUPPLIER = {supplier}")  # Debugging line
            
            cursor.execute("""DELETE FROM supplyOrders WHERE ITEM = :1 AND SUPPLIER = :2""", (item, supplier))
            conn.commit()
            
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404

        # If the format is incorrect for 'customerDemand' (if record_id_parts has 3 elements)
        elif table_name == 'customerDemand' and len(record_id_parts) == 3:
            customer, item, qty = record_id_parts[0], record_id_parts[1], record_id_parts[2]
            print(f"Deleting customerDemand record with CUSTOMER = {customer}, ITEM = {item}, QTY = {qty}")
    
            # You can now use 'customer' and 'item' for deletion, or handle the 'extra' part separately
            cursor.execute("""DELETE FROM customerDemand WHERE CUSTOMER = :1 AND ITEM = :2""", (customer, item))
            conn.commit()
    
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404
        

        elif table_name == 'shippingPricing' and len(record_id_parts) == 9:
            shipper, fromLoc, toLoc = record_id_parts[7], record_id_parts[4], record_id_parts[8]
            print(f"Deleting customerDemand record with SHIPPER = {shipper}, FROMLOC = {fromLoc}, TOLOC = {toLoc}")
    
            # You can now use 'customer' and 'item' for deletion, or handle the 'extra' part separately
            cursor.execute("""DELETE FROM shippingPricing WHERE SHIPPER = :1 AND FROMLOC = :2 AND TOLOC = :3""", (shipper, fromLoc,toLoc))
            conn.commit()
    
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404

        elif table_name == 'manufUnitPricing' and len(record_id_parts) == 4:
            manuf, prodItem = record_id_parts[0], record_id_parts[2]
            print(f"Deleting manufUnitPricing record with manufUnitPricing MANUF = {manuf}, PRODITEM = {prodItem}")
    
            # You can now use 'customer' and 'item' for deletion, or handle the 'extra' part separately
            cursor.execute("""DELETE FROM manufUnitPricing WHERE MANUF = :1 AND PRODITEM = :2""", (manuf, prodItem))
            conn.commit()
    
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404
        
        elif table_name == 'manufDiscounts' and len(record_id_parts) == 3:
            manuf = record_id_parts[2]
            print(f"Deleting manufDiscounts record with manufDiscounts MANUF = {manuf}")
    
            # You can now use 'customer' and 'item' for deletion, or handle the 'extra' part separately
            cursor.execute("""DELETE FROM manufDiscounts WHERE MANUF = :1""", (manuf,))
            conn.commit()
    
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404

        elif table_name == 'supplyUnitPricing' and len(record_id_parts) == 3:
            item, supplier = record_id_parts[0], record_id_parts[2]
            print(f"Deleting supplyUnitPricing record with supplyUnitPricing ITEM = {item}, SUPPLIER={supplier}")
    
            # You can now use 'customer' and 'item' for deletion, or handle the 'extra' part separately
            cursor.execute("""DELETE FROM supplyUnitPricing WHERE ITEM = :1 AND SUPPLIER = :2""", (item,supplier))
            conn.commit()
    
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404

        elif table_name == 'supplierDiscounts' and len(record_id_parts) == 5:
            supplier = record_id_parts[4]
            print(f"Deleting supplierDiscounts record with supplierDiscounts SUPPLIER={supplier}")
    
            # You can now use 'customer' and 'item' for deletion, or handle the 'extra' part separately
            cursor.execute("""DELETE FROM supplierDiscounts WHERE SUPPLIER = :1""", (supplier,))
            conn.commit()
    
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404

        elif table_name == 'billOfMaterials' and len(record_id_parts) == 3:
            matItem,prodItem = record_id_parts[0],record_id_parts[1]
            print(f"Deleting billOfMaterials record with billOfMaterials MATITEM={matItem},prodItem={prodItem}")
    
            # You can now use 'customer' and 'item' for deletion, or handle the 'extra' part separately
            cursor.execute("""DELETE FROM billOfMaterials WHERE MATITEM = :1 AND prodItem = :2""", (matItem,prodItem))
            conn.commit()
    
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404

        elif table_name == 'busEntities' and len(record_id_parts) == 6:
            entity = record_id_parts[2]
            print(f"Deleting busEntities record with busEntities ENTITY={entity}")
    
            # You can now use 'customer' and 'item' for deletion, or handle the 'extra' part separately
            cursor.execute("""DELETE FROM busEntities WHERE ENTITY = :1""", (entity,))
            conn.commit()
    
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404


        elif table_name == 'items' and len(record_id_parts) == 2:
            item = record_id_parts[0]
            print(f"Deleting items record with items ITEM={item}")
    
            # You can now use 'customer' and 'item' for deletion, or handle the 'extra' part separately
            cursor.execute("""DELETE FROM items WHERE ITEM = :1""", (item,))
            conn.commit()
    
            if cursor.rowcount > 0:
                return jsonify({"success": True})
            else:
                return jsonify({"error": "No matching record found to delete"}), 404

        else:
            print("Invalid format for record ID or unsupported table.")  # Debugging line
            return jsonify({"error": "Record ID format is incorrect. Expected format: CUSTOMER,ITEM for customerDemand."}), 400

    except Exception as e:
        print(f"Error deleting record: {str(e)}")  # Debugging line
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
