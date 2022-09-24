import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pss83307;PWD=Lab47l4rodOvB2WE",'','')
print(conn)
#ibm_db.execute('CREATE TABLE customers (FirstName TEXT ,LastName TEXT,Email TEXT,password TEXT,confirmpassword TEXT )')
#table_creation=ibm_db.exec_immediate(conn,'CREATE TABLE customers (FirstName VARCHAR(20) ,LastName VARCHAR(20),Email VARCHAR(20),password VARCHAR(20),confirmpassword VARCHAR(20))')
sql = "INSERT INTO customers (FirstName,LastName,Email,password,confirmpassword) VALUES(?,?,?,?,?);"
stmt = ibm_db.prepare(conn, sql)
fname='vikram'
lname='krishna'
email='vikikrish@gmail.com'
pwd = '123viki'
cpwd = '123viki'

ibm_db.bind_param(stmt, 1, fname)
ibm_db.bind_param(stmt, 2, lname)
ibm_db.bind_param(stmt, 3, email)
ibm_db.bind_param(stmt, 4, pwd)
ibm_db.bind_param(stmt, 5, cpwd)
ibm_db.execute(stmt)'''

sql = "SELECT * FROM CUSTOMERS WHERE Email = ? "
stmt = ibm_db.prepare(conn, sql)
email = "vikikrish@gmail.com"
# Explicitly bind parameters
ibm_db.bind_param(stmt, 1,email)
#ibm_db.bind_param(stmt, 2, max)
ibm_db.execute(stmt)
dictionary = ibm_db.fetch_assoc(stmt)
while dictionary != False:
    print("The Firstname is : ", dictionary["FIRSTNAME"])
    print("The lastname is : ", dictionary["LASTNAME"])
    dictionary = ibm_db.fetch_assoc(stmt)
print('table created successfully')
ibm_db.close(conn)
