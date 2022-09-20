from typing import Optional

from fastapi import FastAPI, Path
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

    results = searchBy(field = 'name', value = contact.personDetails.firstName + '_' + contact.personDetails.lastName)

    if results != []:
        return {'Error': 'Item exists'}

    print(results)
    # item['id'] = contact_id
    #
    # menu.append(item)
    return 4

@app.delete('/delete-contact/{contact_id}')
def delete_item(contact_id: int):
    return deleteContact(contact_id)


@app.get('/get-by-name')
def get_item(name: Optional[str] = None):

    search = list(filter(lambda x: x["name"] == name, menu))

    if search == []:
        return {'item': 'Does not exist'}

    return {'Item': search[0]}

@app.get('/list-menu')
def list_menu():
    return {'Menu': menu}





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