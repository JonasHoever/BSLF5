from flask import Flask, render_template, request, jsonify
from src import script

app = Flask(__name__)
dbsys = script.IinitDatabase("jonashoever.de","mika","password64534231","LF5")
deldatasys = script.DeleteUserData("jonashoever.de","mika","password64534231","LF5")
readdatasys = script.ReadUserData("jonashoever.de","mika","password64534231","LF5")

@app.route("/api/initdb", methods=["POST"])
def initdb():
    result = dbsys.InitDB()
    return jsonify(result)

@app.route("/api/read_customer_data_id", methods=["POST"])
def read_customer_data_id():
    data = request.get_json()
    CustomerID = data.get('CustomerID')
    result = readdatasys.read_customer_data_by_id(CustomerID)
    return jsonify(result)

@app.route("/api/read_customer_data_name", methods=["POST"])
def read_customer_data_name():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    street = data.get('street')
    postcode = data.get('postcode')
    residence = data.get('residence')
    result = readdatasys.read_customer_data_by_name(first_name, last_name, street, postcode, residence)
    return jsonify(result)

@app.route("/api/delete_user_by_id", methods=['DELETE'])
def delete_user_by_id():
    data = request.get_json()
    customerID_str = data.get('customerID')
    if not customerID_str:
        return {"error": "Kundennummer wurde nicht bereitgestellt."}, 400
    try:
        customerID = int(customerID_str)
    except ValueError:
        return {"error": "Ungültige Kundennummer. Bitte geben Sie eine numerische ID ein."}, 400

    result = deldatasys.delete_customer_by_id(customerID)
    return result, 200

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/read-by-id")
def id_data_page():
    return render_template("read_cust_id.html")

@app.route("/read-by-name")
def name_data_page():
    return render_template("read_cust_name.html")

@app.route("/delete-customer")
def delete_customer_page():
    return render_template("delete_cust.html")

@app.route("/init-database")
def init_db_page():
    return render_template("init_db.html")

app.run(host="0.0.0.0",port=3000,debug=True)