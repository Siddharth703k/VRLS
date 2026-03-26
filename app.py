from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import date

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tripathi@1",
    database="vrls"
)

def get_vehicle_age(year):
    return date.today().year - year

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.vehicle_id, v.registration_number, v.make, v.model, v.year,
               o.name AS owner_name, o.mobile AS owner_mobile
        FROM vehicle v
        JOIN owner o ON v.owner_id=o.owner_id
    """)
    vehicles = cursor.fetchall()
    cursor.close()
    return render_template('index.html', vehicles=vehicles, get_vehicle_age=get_vehicle_age, current_year=date.today().year)

@app.route('/add', methods=['POST'])
def add_data():
    owner_name = request.form['owner_name']
    mobile = request.form['mobile']
    registration_number = request.form['registration_number']
    make = request.form['make']
    model = request.form['model']
    year_val = int(request.form['year'])
    registration_date = request.form['registration_date']
    expiry_date = request.form['expiry_date']

    cursor = db.cursor()
    cursor.execute("SELECT owner_id FROM owner WHERE name=%s AND mobile=%s", (owner_name, mobile))
    owner = cursor.fetchone()
    if owner:
        owner_id = owner[0]
    else:
        cursor.execute("SELECT COALESCE(MAX(owner_id),0) FROM owner")
        owner_id = cursor.fetchone()[0] + 1
        cursor.execute("INSERT INTO owner(owner_id,name,mobile) VALUES(%s,%s,%s)", (owner_id, owner_name, mobile))

    cursor.execute("SELECT COALESCE(MAX(vehicle_id),0) FROM vehicle")
    vehicle_id = cursor.fetchone()[0] + 1
    cursor.execute("""
        INSERT INTO vehicle(vehicle_id, owner_id, registration_number, make, model, year)
        VALUES(%s,%s,%s,%s,%s,%s)
    """, (vehicle_id, owner_id, registration_number, make, model, year_val))

    cursor.execute("SELECT COALESCE(MAX(registration_id),0) FROM registration")
    registration_id = cursor.fetchone()[0] + 1
    cursor.execute("""
        INSERT INTO registration(registration_id, vehicle_id, registration_date, expiry_date)
        VALUES(%s,%s,%s,%s)
    """, (registration_id, vehicle_id, registration_date, expiry_date))

    db.commit()
    cursor.close()
    return redirect('/')

@app.route('/expired')
def expired():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.registration_number, v.make, v.model, v.year,
               o.name AS owner_name, o.mobile AS owner_mobile,
               r.registration_date, r.expiry_date
        FROM vehicle v
        JOIN registration r ON v.vehicle_id = r.vehicle_id
        JOIN owner o ON v.owner_id = o.owner_id
        WHERE r.expiry_date < CURDATE()
    """)
    expired_list = cursor.fetchall()
    cursor.close()
    return render_template('expired.html', expired_list=expired_list)

@app.route('/inspection/<int:vehicle_id>')
def inspection(vehicle_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inspection WHERE vehicle_id=%s ORDER BY inspection_date DESC", (vehicle_id,))
    inspections = cursor.fetchall()
    cursor.close()
    return render_template('inspection.html', vehicle_id=vehicle_id, inspections=inspections)

@app.route('/add_inspection/<int:vehicle_id>', methods=['POST'])
def add_inspection(vehicle_id):
    insp_date = request.form['inspection_date']
    result = request.form['result']

    cursor = db.cursor()
    cursor.execute("SELECT COALESCE(MAX(inspection_id),0) FROM inspection")
    inspection_id = cursor.fetchone()[0] + 1
    cursor.execute("""
        INSERT INTO inspection(inspection_id, vehicle_id, inspection_date, result)
        VALUES (%s, %s, %s, %s)
    """, (inspection_id, vehicle_id, insp_date, result))
    db.commit()
    cursor.close()
    return redirect(f'/inspection/{vehicle_id}')

@app.route('/insurance/<int:vehicle_id>')
def insurance(vehicle_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM insurance WHERE vehicle_id=%s ORDER BY start_date DESC", (vehicle_id,))
    insurances = cursor.fetchall()
    cursor.close()
    return render_template('insurance.html', vehicle_id=vehicle_id, insurances=insurances)

@app.route('/add_insurance/<int:vehicle_id>', methods=['POST'])
def add_insurance(vehicle_id):
    policy_number = request.form['policy_number']
    insurer_name = request.form['insurer_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    cursor = db.cursor()
    cursor.execute("SELECT COALESCE(MAX(insurance_id),0) FROM insurance")
    insurance_id = cursor.fetchone()[0] + 1
    cursor.execute("""
        INSERT INTO insurance(insurance_id, vehicle_id, policy_number, insurer_name, start_date, end_date)
        VALUES(%s,%s,%s,%s,%s,%s)
    """, (insurance_id, vehicle_id, policy_number, insurer_name, start_date, end_date))
    db.commit()
    cursor.close()
    return redirect(f'/insurance/{vehicle_id}')

@app.route('/history/<int:vehicle_id>')
def history(vehicle_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM history WHERE vehicle_id=%s ORDER BY event_date DESC", (vehicle_id,))
    history_list = cursor.fetchall()
    cursor.close()
    return render_template('history.html', vehicle_id=vehicle_id, history_list=history_list)

if __name__ == "__main__":
    app.run(debug=True)
