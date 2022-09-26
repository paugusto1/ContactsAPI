from typing import Optional

from fastapi import FastAPI, Path, HTTPException
from models import *
from database import *
from mangum import Mangum

# File named main.py to fulfill requirements for AWS Lambda

description = """ 
Contacts API is a API to manage contacts.

## Users

You will be able to:

* **Create new contacts** .
* **Search contacts by fields** .
* **List all contacts** .
* **Delete contacts** .
* **Update existing contact** .

"""

app = FastAPI\
    (
        title="ContactsAPI",
        description=description,
        version="0.0.1",
        contact={
            "name": "Pedro Vicente",
            "email": "pedro-augusto32@hotmail.com",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    )

handler = Mangum(app)


@app.get('/')
def index():
    """
    Default page. Test connection to DB:
    """

    try:
        getDBCursor()
    except:
        return "Database connection failed. Try again later."

    return "API is running! Try the available operations."


@app.get('/populate-db/test-only')
def populateDB():
    """
    Populate the DB with default register. For test only:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """

    startDB()
    return 200


@app.get('/get-contacts/{field}/{value}')
def get_contact(
    field: str = Path(
        None,
        description="Fill with field you want to search"),
    value: str = Path(
            None,
            description="Fill with value you want to search")):

    """
    Search a Contact considering a field and a value.

    - **field**: Field to be used as search.
    - **value**: Value to seach.
    """

    if field == '' or value == '':
        raise HTTPException(status_code=422,
                            detail="Search can only be done when value and field are informed.")

    if field.lower() not in FIELDS_SEARCH:
        raise HTTPException(status_code=422,
                            detail="Search can only be done with " + str(FIELDS_SEARCH))

    results = searchBy(field.lower(), value)

    return results


@app.get('/get-contacts/all')
def get_contact():

    """
    Return the list of all contacts, ordered by last name.
    """

    results = searchBy(field = None, value = None)

    return results


@app.post('/create-contact/')
def create_contact(contact: Contact):

    """
    Add a new contact to the database.

    - **contact**: Json representing a contact (Check Pydantic class Contact for details).
    """

    validateContact(contact)

    results = searchBy(field = 'name', value = contact.personDetails.firstName + '_' + contact.personDetails.lastName)

    # Validating contact duplicated (Considering only one contact of same firstName and lastName can exist).
    if results:
        raise HTTPException(status_code=422,
                            detail="User already exists")

    return addContact(contact)


@app.delete('/delete-contact/{contact_id}')
def delete_contact(contact_id: int):

    """
    Remove Contact with informed id (if it exists).

    - **contact_id**: Id of the contact to be deleted
    """

    return deleteContact(contact_id)

@app.put('/update-contact/{contact_id}/')
def update_contact(contact_id: int, contact: Contact):

    """
    Populate the DB with default register. For test only:

    - **contact_id**: Id of the contact to be updated
    - **contact**: Json representing a contact (Check Pydantic class Contact for details).
    """

    validateContact(contact)

    results = searchBy(field = 'id', value = contact_id)

    # If contact does not exist, create a new one.
    if not results:
        return addContact(contact)
    return addContact(contact, updating=True)


def validateContact(contact):

    """
    Check the contact for issues with the values for address, profileImage and birthday

    - **contact**: Json representing a contact (Check Pydantic class Contact for details).
    """

    # Handle only brazilian addresses

    for add in contact.address.__root__:
        if add.country.upper() != 'BRAZIL':
            raise HTTPException(status_code=422, detail="Currently, only Brazil addresses allowed")
        if add.state.upper() not in STATES.keys():
            raise HTTPException(status_code=422,
                                detail="Currently, only Brazil addresses allowed. Use 2 letter notation for states.")

    # Handle correct image url
    if contact.profileImage != '' and contact.profileImage[-4:] not in IMAGE and contact.profileImage[-5:] not in IMAGE:
        raise HTTPException(status_code=422,
                            detail="Profile Image should be a URL with image extension.")

    # Handle invalid Birthday
    if contact.personDetails.dateOfBirth is None:
        raise HTTPException(status_code=422,
                            detail="Date invalid")

