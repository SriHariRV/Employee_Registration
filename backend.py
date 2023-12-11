from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mysql',
    'database': 'employee'
}

def connect_to_database():
    try:
        conn = mysql.connector.connect(**mysql_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/add_employee', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        if data:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()

                query = "INSERT INTO details (name, dob, gender, age, employeeID, address, designation, joiningDate, salary,phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                employee_values = (
                    data['name'], data['dob'], data['gender'],data['age'], data['address'],data['employeeID'], data['designation'],
                    data['joiningDate'], data['salary'], data['phone']
                )
                cursor.execute(query, employee_values)

                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({'message': 'Employee details added successfully'})
            else:
                return jsonify({'error': 'Failed to connect to the database'})
        else:
            return jsonify({'error': 'No data provided'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
