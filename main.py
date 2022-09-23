from typing import Optional

from fastapi import FastAPI, Path, HTTPException
from contacts import menu
from models import *
from database import *
from mangum import Mangum

app = FastAPI()

handler = Mangum(app)

@app.get("/")
def hello_world_root():
    return {"Hello": "World"}

@app.get('/get-contacts/{field}/{value}')
def get_contact(
    field: str = Path(
        None,
        description="Fill with ID of the contact you want to view"),
    value: str = Path(
            None,
            description="Fill with ID of the contact you want to view")):

    results = searchBy(field, value)

    return results

@app.get('/get-contacts/all')
def get_contact():

    results = searchBy(field = None, value = None)

    return results

@app.post('/create-contact/')
def create_contact(contact: Contact):

    print(contact)

    for add in contact.address.__root__:
        if add.country.upper() != 'BRAZIL':
            raise HTTPException(status_code=422, detail="Currently, only Brazil addresses allowed")
        if add.state.upper() not in STATES.keys():
            raise HTTPException(status_code=422, detail="Currently, only Brazil addresses allowed. Use 2 letter notation for states.")

    print(contact.profileImage[-4:])

    if contact.profileImage != '' and contact.profileImage[-4:] not in IMAGE and contact.profileImage[-5:] not in IMAGE:
        raise HTTPException(status_code=422,
                            detail="Profile Image should be a URL with image extension.")


    if contact.personDetails.dateOfBirth is None:
        raise HTTPException(status_code=422,
                            detail="Date invalid")

    results = searchBy(field = 'name', value = contact.personDetails.firstName + '_' + contact.personDetails.lastName)

    if results != []:
        raise HTTPException(status_code=422,
                            detail="User already exists")

    print(type(contact.email.__root__))
    return addContact(contact)

    print(results)
    # item['id'] = contact_id
    #
    # menu.append(item)
    return 4

@app.delete('/delete-contact/{contact_id}')
def delete_item(contact_id: int):
    return deleteContact(contact_id)

@app.post('/update-contact/')
def update_contact(contact: Contact):

    print(contact)

    for add in contact.address.__root__:
        if add.country.upper() != 'BRAZIL':
            raise HTTPException(status_code=422, detail="Currently, only Brazil addresses allowed")
        if add.state.upper() not in STATES.keys():
            raise HTTPException(status_code=422, detail="Currently, only Brazil addresses allowed. Use 2 letter notation for states.")

    print(contact.profileImage[-4:])

    if contact.profileImage != '' and contact.profileImage[-4:] not in IMAGE and contact.profileImage[-5:] not in IMAGE:
        raise HTTPException(status_code=422,
                            detail="Profile Image should be a URL with image extension.")


    if contact.personDetails.dateOfBirth is None:
        raise HTTPException(status_code=422,
                            detail="Date invalid")

    results = searchBy(field = 'name', value = contact.personDetails.firstName + '_' + contact.personDetails.lastName)


    return addContact(contact, updating=True)

    print(results)
    # item['id'] = contact_id
    #
    # menu.append(item)
    return 4


# @app.put('/update-item/{item_id}')
# def update_item(item_id: int, item: UpdateItem):
#
#     search = list(filter(lambda x: x["id"] == item_id, menu))
#
#     if search == []:
#         return {'Item': 'Does not exist'}
#
#     if item.name is not None:
#         search[0]['name'] = item.name
#
#     if item.price is not None:
#         search[0]['price'] = item.price
#
#     return search
#
#
# @app.delete('/delete-item/{item_id}')
# def delete_item(item_id: int):
#     search = list(filter(lambda x: x["id"] == item_id, menu))
#
#     if search == []:
#         return {'Item': 'Does not exist'}
#
#     for i in range(len(menu)):
#         if menu[i]['id'] == item_id:
#             del menu[i]
#             break
#     return {'Message': 'Item deleted successfully'}

#if __name__ == '__main__':
#   uvicorn.run("apiContact:apiContact", port=5000, log_level="info")