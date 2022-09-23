#!pip install PyMySQL

# Database methods used by API to manage Contact

import pymysql
from models import *
import json

#Brazil States
STATES = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins'
    }

#Image formats, used to validate profileImage value.
IMAGE = ('.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm',
         '.tiff', '.rgb', '.pgm', '.png', '.pnm')

#Field allowed to be searched
FIELDS_SEARCH = ['phone', 'email', 'city', 'state', 'id', 'name']

#Return references for database Contacts - Hosted by AWS
def getDBCursor():
    db = pymysql.connect(host="databasecontacts.ccf8jotwvwtf.us-east-1.rds.amazonaws.com", user="admin",
                         password="12345678")
    cursor = db.cursor()

    sql = '''use ContactDB'''
    cursor.execute(sql)
    cursor.connection.commit()

    return cursor, db

#Used for test purposes. Reset data base ContactDB
def restartDB(cursor):
    sql = '''DROP DATABASE ContactDB'''
    cursor.execute(sql)
    cursor.connection.commit()

    sql = '''create database ContactDB'''
    cursor.execute(sql)
    cursor.connection.commit()


#Set cursor to use data base ContactDB
def setDatabase(cursor):

    sql = '''use ContactDB'''
    cursor.execute(sql)
    cursor.connection.commit()

#DB scheme. For more information check ERD available on GITHUB.
def createTables(cursor):

    sql = '''
        CREATE TABLE Country (
        id int NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL,
        PRIMARY KEY (id))'''
    cursor.execute(sql)

    sql = '''
        CREATE TABLE State (
        id int NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL,
        fkIdCountry int,
        PRIMARY KEY (id),
        FOREIGN KEY (fkIdCountry) REFERENCES Country(id))'''
    cursor.execute(sql)

    sql = '''
        CREATE TABLE City (
        id int NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL,
        fkIdState int,
        PRIMARY KEY (id),
        FOREIGN KEY (fkIdState) REFERENCES State(id))'''
    cursor.execute(sql)

    sql = '''
       CREATE TABLE Company (
        id int NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL,
        PRIMARY KEY (id))'''
    cursor.execute(sql)

    sql = '''
        CREATE TABLE Contact (
        id int NOT NULL AUTO_INCREMENT,
        firstName varchar(255) NOT NULL,
        lastName varchar(255) NOT NULL,
        dateOfBirth date,
        profileImage varchar(255),
        companyId int,
        PRIMARY KEY (id))'''
    cursor.execute(sql)

    sql = '''
        CREATE TABLE Address (
            id int NOT NULL AUTO_INCREMENT,
            address varchar(255) NOT NULL,
            postalCode varchar(10) NOT NULL,
            apartment varchar(10),
            fkIdCity int,
            fkIdContact int,
            PRIMARY KEY (id),
            FOREIGN KEY (fkIdCity) REFERENCES City(id),
            FOREIGN KEY (fkIdContact) REFERENCES Contact(id)
        )'''
    cursor.execute(sql)

    sql = '''
        CREATE TABLE TypeEmail (
            id int NOT NULL AUTO_INCREMENT,
            type varchar(255) NOT NULL,
            PRIMARY KEY (id)
        )'''
    cursor.execute(sql)

    sql = '''
        CREATE TABLE TypePhoneNumber (
            id int NOT NULL AUTO_INCREMENT,
            type varchar(255) NOT NULL,
            PRIMARY KEY (id)
        )'''
    cursor.execute(sql)

    sql = '''
        CREATE TABLE Email (
            id int NOT NULL AUTO_INCREMENT,
            value varchar(255) NOT NULL,
            fkIdContact int,
            fkIdType int,
            PRIMARY KEY (id),
            FOREIGN KEY (fkIdContact) REFERENCES Contact(id),
            FOREIGN KEY (fkIdType) REFERENCES TypeEmail(id)
        )'''
    cursor.execute(sql)

    sql = '''
        CREATE TABLE PhoneNumber (
            id int NOT NULL AUTO_INCREMENT,
            value varchar(255) NOT NULL,
            fkIdContact int,
            fkIdType int,
            PRIMARY KEY (id),
            FOREIGN KEY (fkIdContact) REFERENCES Contact(id),
            FOREIGN KEY (fkIdType) REFERENCES TypePhoneNumber(id)
        )'''
    cursor.execute(sql)

    sql = '''show tables'''
    cursor.execute(sql)
    print(cursor.fetchall())

#For test. Initial population.
def initialPopulation(cursor):

    sql = ''' insert into Country (name) values('BRAZIL')'''
    cursor.execute(sql)

    states = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins'
    }

    typePhone = ["Personal","Work"]
    typeEmail = ["Personal", "Work"]

    for i in states.keys():
        sql = ''' insert into State (name, fkIdCountry) values('%s', 1)''' % (i.upper())
        cursor.execute(sql)

    for i in typePhone:
        sql = ''' insert into TypePhoneNumber (type) values('%s')''' % (i.upper())
        cursor.execute(sql)

    for i in typeEmail:
        sql = ''' insert into TypeEmail (type) values('%s')''' % (i.upper())
        cursor.execute(sql)

    sql = ''' insert into City (name, fkIdState) values('CAMPINAS', 25)'''
    cursor.execute(sql)

    sql = ''' insert into City (name, fkIdState) values('SUMARÉ', 25)'''
    cursor.execute(sql)

    sql = ''' insert into Company (name) values('ELDORADO')'''
    cursor.execute(sql)

    sql = ''' insert into Company (name) values('BOSCH')'''
    cursor.execute(sql)

    sql = ''' insert into Company (name) values('GOOGLE')'''
    cursor.execute(sql)

    sql = ''' insert into Company (name) values('APPLE')'''
    cursor.execute(sql)

    sql = ''' insert into Contact (firstName, lastName, dateOfBirth, profileImage, companyId) values('PEDRO', 'VICENTE', '1993-09-21', 'https://4.bp.blogspot.com/-cebXJ9RB6r8/UPCCOoQHf0I/AAAAAAAAAyQ/fnM9_IbeW3U/s1600/pikachu_by_caridea-d3i4jd5.png', 1)'''
    cursor.execute(sql)

    sql = ''' insert into Contact (firstName, lastName, dateOfBirth, profileImage, companyId) values('AUGUSTO', 'PAULO', '1990-08-20', 'https://assets.b9.com.br/wp-content/uploads/2014/08/bulbasaur.png', 2)'''
    cursor.execute(sql)

    sql = ''' insert into Contact (firstName, lastName, dateOfBirth, profileImage, companyId) values('MARY', 'SUE', '1990-07-03', 'https://www.pngmart.com/files/13/Pokemon-Charmander-Transparent-PNG.png', 3)'''
    cursor.execute(sql)

    sql = ''' insert into Contact (firstName, lastName, dateOfBirth, profileImage, companyId) values('ANA', 'SANTOS', '1995-11-20', 'https://assets.stickpng.com/images/580b57fcd9996e24bc43c32a.png', 4)'''
    cursor.execute(sql)

    sql = ''' insert into Address (address, postalCode, apartment, fkIdCity, fkIdContact) values('Rua 1, 2', '13179213', '0', 2, 1)'''
    cursor.execute(sql)

    sql = ''' insert into Address (address, postalCode, apartment, fkIdCity, fkIdContact) values('Rua 1, 7', '13179213', '0', 2, 2)'''
    cursor.execute(sql)

    sql = ''' insert into Address (address, postalCode, apartment, fkIdCity, fkIdContact) values('Rua 1, 9', '13179213', '0', 2, 3)'''
    cursor.execute(sql)

    sql = ''' insert into Address (address, postalCode, apartment, fkIdCity, fkIdContact) values('Rua 2, 488', '13179200', '0', 1, 4)'''
    cursor.execute(sql)

    sql = ''' insert into Email (value, fkIdContact, fkIdType) values('PEDROV@HOTMAIL.COM', 1, 1)'''
    cursor.execute(sql)

    sql = ''' insert into Email (value, fkIdContact, fkIdType) values('PEDROV@LENOVO.COM', 1, 2)'''
    cursor.execute(sql)

    sql = ''' insert into Email (value, fkIdContact, fkIdType) values('AUGUSTO@HOTMAIL.COM', 2, 1)'''
    cursor.execute(sql)

    sql = ''' insert into Email (value, fkIdContact, fkIdType) values('AUGUSTO@LENOVO.COM', 2, 2)'''
    cursor.execute(sql)

    sql = ''' insert into Email (value, fkIdContact, fkIdType) values('MARY@HOTMAIL.COM', 3, 1)'''
    cursor.execute(sql)

    sql = ''' insert into Email (value, fkIdContact, fkIdType) values('ANA@APPLE.COM', 4, 2)'''
    cursor.execute(sql)


    sql = ''' insert into PhoneNumber (value, fkIdContact, fkIdType) values('989230310', 1, 1)'''
    cursor.execute(sql)

    sql = ''' insert into PhoneNumber (value, fkIdContact, fkIdType) values('38545858', 2, 2)'''
    cursor.execute(sql)

    sql = ''' insert into PhoneNumber (value, fkIdContact, fkIdType) values('12345678', 3, 1)'''
    cursor.execute(sql)

    sql = ''' insert into PhoneNumber (value, fkIdContact, fkIdType) values('87456123', 4, 2)'''
    cursor.execute(sql)


    sql = '''select * from Country'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)

    sql = '''select * from State'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)

    sql = '''select * from City'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)

    sql = '''select * from Company'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)

    sql = '''select * from TypePhoneNumber'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)

    sql = '''select * from TypeEmail'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)

    sql = '''select * from Address'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)

    sql = '''select * from Email'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)

    sql = '''select * from PhoneNumber'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)

    sql = '''select * from Contact'''
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)


def deleteContact(id):

    """
    deleteContact Remove Contact with informed id (if it exists).

    :param id: describe about parameter p1
    :return: String with operation result.
    """

    cursor, db = getDBCursor()

    results = searchBy(field='id', value=id)

    if results == []:
        return {'Item': 'Does not exist'}

    sql = '''delete from Email where fkIdContact = %i''' % id
    cursor.execute(sql)
    db.commit()

    sql = '''delete from PhoneNumber where fkIdContact = %i''' % id
    cursor.execute(sql)
    db.commit()

    sql = '''delete from Address where fkIdContact = %i''' % id
    cursor.execute(sql)
    db.commit()

    sql = '''delete from Contact where id = %i''' % id
    cursor.execute(sql)
    db.commit()

    return {'Message': 'Item deleted successfully'}


def addEmailPhone(db, cursor, elem, newId, table):
    """
    addEmailPhone Add a new email or phone number with the correct references.

    :param db: reference to DB
    :param cursor: sql cursor execute
    :param elem: elem to be added to table
    :param newId: Contact id to use as FK
    :param table: Table where elem should be added (Email/PhoneNumber)
    :return: None
    """

    # Check if Type already exists, if not add it.

    sql = '''select id from %s where type = '%s' ''' % ('Type' + table, elem.type.upper())
    cursor.execute(sql)
    res = cursor.fetchall()

    if len(res) == 0:
        sql = ''' insert into %s (type) values('%s')''' % ('Type' + table, elem.type.upper())
        cursor.execute(sql)
        db.commit()

        sql = '''select id from %s where type = '%s' ''' % ('Type' + table, elem.type.upper())
        cursor.execute(sql)
        res = cursor.fetchall()

    typeEmailId = res[0][0]

    sql = '''select id from %s where value = '%s' and fkIdContact = %i and fkIdType = %i'''\
          % (table, elem.value.upper(), newId, typeEmailId)
    cursor.execute(sql)
    res = cursor.fetchall()

    #Add new Email/Phone with the correct FK refs to contact and type

    if len(res) == 0:
        sql = ''' insert into %s (value, fkIdContact, fkIdType) 
              values('%s', %i, %i)''' % (table, elem.value.upper(), newId, typeEmailId)

        cursor.execute(sql)
        db.commit()


def addAddress(db, cursor, elem, newId):

    """
    addAddress Add a new address with the correct references.

    :param db: reference to DB
    :param cursor: sql cursor execute
    :param elem: elem to be added to table
    :param newId: Contact id to use as FK
    :return: None
    """

    #Get state id
    stateId = list(STATES.keys()).index(elem.state) + 1
    cityName = elem.city.upper()

    # Check if City already exists, if not add it.

    sql = '''select id from City where name = '%s' and fkIdState = %i''' \
          % (cityName, stateId)
    cursor.execute(sql)
    res = cursor.fetchall()

    if len(res) == 0:
        sql = ''' insert into City(name, fkIdState) values('%s', %i)''' % (cityName, stateId)
        cursor.execute(sql)
        db.commit()

        sql = '''select id from City where name = '%s' and fkIdState = %i''' \
              % (cityName, stateId)
        cursor.execute(sql)
        res = cursor.fetchall()

    cityId= res[0][0]

    address = elem.street.upper()
    postalCode = elem.postalCode.upper()
    apartment = elem.apartment.upper()

    # Add new Address with the correct FK refs to contact and state

    sql = ''' insert into Address (address, postalCode, apartment, fkIdCity, fkIdContact) 
          values('%s', '%s', '%s', %i, %i)''' % (address, postalCode, apartment, cityId, newId)


    cursor.execute(sql)
    db.commit()


def addContact(c, updating = False):

    """
    addContact Add a Contact and update support tables if necessary.

    :param c: Contact object with the info to be included/updated.
    :param updating: if True this is a update operation
    :return: added/updated contact
    """

    cursor, db = getDBCursor()

    #If informed company does not exists created it.

    sql = '''select id from Company where name = '%s' ''' % c.company.upper()
    cursor.execute(sql)
    res = cursor.fetchall()

    if len(res) == 0:
        sql = ''' insert into Company (name) values('%s')''' % c.company.upper()
        cursor.execute(sql)
        db.commit()

        sql = '''select id from Company where name = '%s' ''' % c.company.upper()
        cursor.execute(sql)
        res = cursor.fetchall()

    companyId = res[0][0]


    firstName = c.personDetails.firstName.upper()
    lastName = c.personDetails.lastName.upper()
    dateOfBirth = c.personDetails.dateOfBirth
    profileImage = c.profileImage

    # Create a new Contact if not updating.
    # If updating remove all registers of phone, email and address to be included again.

    if not updating:
        sql = ''' insert into Contact (firstName, lastName, dateOfBirth, profileImage, companyId) 
              values('%s', '%s', '%s', '%s', %i)''' % (firstName, lastName, dateOfBirth, profileImage, companyId)

        cursor.execute(sql)
        db.commit()

        res = searchBy(field = 'name', value = firstName + '_' + lastName)

        newId = res[0]['id']
    else:

        sql = '''update Contact set companyId = %i, dateOfBirth = '%s', profileImage = '%s' where id = %i''' % \
              (companyId,dateOfBirth, profileImage, int(c.id))
        cursor.execute(sql)
        db.commit()

        sql = '''delete from Email where fkIdContact = %i''' % int(c.id)
        cursor.execute(sql)
        db.commit()

        sql = '''delete from PhoneNumber where fkIdContact = %i''' % int(c.id)
        cursor.execute(sql)
        db.commit()

        sql = '''delete from Address where fkIdContact = %i''' % int(c.id)
        cursor.execute(sql)
        db.commit()

        newId = int(c.id)

    #Creating register of each phone, email and address

    for email in c.email.__root__:
        addEmailPhone(db, cursor, email, newId, 'Email')

    for phone in c.phoneNumber.__root__:
        addEmailPhone(db, cursor, phone, newId, 'PhoneNumber')

    for add in c.address.__root__:
        addAddress(db, cursor, add, newId)

    res = searchBy(field = 'name', value = firstName + '_' + lastName)

    #Return added/updated contact

    return res[0]

def searchBy(field, value):

    """
    searchBy Search a Contact considering a field and a value.

    :param field: Field to be used as search.
    :param value: Value to seach.
    :return: List of contacts found, [] if none.
    """

    if field is not None and field != 'id':
        value = value.upper()

    cursor, db = getDBCursor()

    #Define SQL query considering the field value

    if field == 'phone':
        field = 'PhoneNumber'
    elif field == 'email':
        field = 'Email'
    elif field == 'city':
        sql = '''
        select * from Contact where id in 
        (select fkIdContact from Address where fkIdCity in 
        (select id from City where name= '%s')) 
        ''' % (value)
    elif field == 'state':
        sql = '''
        select * from Contact where id in 
        (select fkIdContact from Address where fkIdCity in 
        (select id from City where fkIdState in 
        (select id from State where name ='%s')))
        ''' % (value)
    elif field is None:
        sql = '''
        select * from Contact
        '''
    elif field == 'name':
        names = value.split('_')

        sql = '''
        select * from Contact where 
        firstName = '%s' and
        lastName = '%s'
        ''' % (names[0], names[1])
    elif field == 'id':
        sql = '''
        select * from Contact where 
        id = %s 
        ''' % (value)


    if field == 'PhoneNumber' or field == 'Email':
        sql = '''
        select * from Contact where id in (select fkIdContact from %s where value = '%s')  
        ''' % (field, value)

    sql += " order by lastName"

    cursor.execute(sql)
    res = cursor.fetchall()

    elems = []

    for i in res:
        elems.append(toJson(cursor, i).dict())

    contacts = Contacts(__root__ = elems)

    obj = json.loads(contacts.json())
    json_formatted_str = json.dumps(obj, indent=4)

    return obj

def returnListAddress(cursor, id):

    """
    returnListAddress Return the list of Address related to a contact id.

    :param cursor: Cursor to execute SQL queries
    :param id: Contact id
    :return: List of AddressSingle
    """

    sql = '''
            select a.apartment, a.address, c.name, s.name, a.postalCode, co.name from Address a, City c, 
            State s, Country co 
            where a.fkIdContact = %s and 
            a.fkIdCity = c.id and 
            c.fkIdState = s.id and 
            s.fkIdCountry = co.id
            ''' % (id)


    cursor.execute(sql)
    res = cursor.fetchall()

    listElem = []

    for i in res:
        addressSingle = AddressSingle(apartment=i[0], street=i[1], city = i[2], state= i[3], postalCode = i[4],
                                      country = i[5])

        listElem.append(addressSingle.dict())

    return listElem

def returnListEmailPhone(cursor, field, id):

    """
    returnListEmailPhone Return the list of Phones/Emails related to a contact id.

    :param cursor: Cursor to execute SQL queries
    :param id: Contact id
    :return: List of EmailSingle or PhoneNumberSingle
    """

    if field == 'email':
        sql = '''
            select t.type, e.value from Email e, TypeEmail t 
            where e.fkIdContact = %s and 
            e.fkIdType = t.id  
            ''' % (id)
    elif field == 'phone':
        sql = '''
            select t.type, p.value from PhoneNumber p, TypePhoneNumber t 
            where p.fkIdContact = %s and 
            p.fkIdType = t.id  
            ''' % (id)

    cursor.execute(sql)
    res = cursor.fetchall()

    listElem = list()

    if field == 'email':
        for i in res:
            emailSingle = EmailSingle(type=i[0], value=i[1])
            listElem.append(emailSingle.dict())

    elif field == 'phone':
        for i in res:
            phoneSingle = PhoneNumberSingle(type=i[0], value=i[1])
            listElem.append(phoneSingle.dict())

    return listElem


def toJson(cursor, reg):

    """
    toJson Add a Contact and update support tables if necessary.

    :param cursor: cursor to execute sql commands.
    :param reg: SQL query reply of a Contact.
    :return: Contact object representing a json
    """

    id = reg[0]
    personDetails = PersonDetails(firstName= reg[1], lastName=reg[2],dateOfBirth = reg[3])
    profileImage = reg[4]

    sql = '''
        select name from Company where id =%s
        ''' % (reg[5])

    cursor.execute(sql)
    company = cursor.fetchall()[0][0]


    email = returnListEmailPhone(cursor, 'email', id)
    phoneNumber = returnListEmailPhone(cursor, 'phone', id)
    address = returnListAddress(cursor, id)

    contact = Contact(id=id, personDetails = personDetails, company= company, profileImage= profileImage,
                      email = email, phoneNumber = phoneNumber, address = address)

    return contact

def startDB():

    """
    addContact Reset DB Contact DB to default state (4 Contacts).
    :return: None
    """

    cursor, db = getDBCursor()
    restartDB(cursor)
    setDatabase(cursor)
    createTables(cursor)
    initialPopulation(cursor)
    db.commit()


if __name__ == '__main__':
    startDB()
