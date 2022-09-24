
# ContactAPI - Pedro Augusto Vicente

ContactsAPI is a RESTFul API to manage contacts.



## Authors

- Pedro Augusto Vicente (pedro-augusto32@hotmail)


## Features

- Create new contacts.
- Search contacts by fields.
- List all contacts.
- Delete contacts.
- Update existing contact.


## Notes

This was the first time I had the opportunity to directly develop an API.
 
As Python is the language I am more familiar with, it was the direct option. First, i looked up 
for Frameworks that could support the development. FastAPI was the choice, mainly because 
there are a good documentation i could use to learn 
about the tool.
 
Also, the use of the Pydantic module was a facilitator to do the Data validation.
 
I got a little excited and also did a Web Client Application using Python (Flask Framework)
to use the ContactAPI. This was also a great opportunity to exercise with different skills that,
as a QA/PO, is not always my main role.  
 
For persistence, AWS Relational Database Service is being used. Data representation can be 
checked below. As we are talking about a simple Contact register i considered that maybe a NoSQL document based 
approach could be used but i went with the relational option.
 
Database, Web Client Application and API are hosted by different AWS cloud services. The last
two are available for online evaluation (Check Demo section)



## Database representation

![App Screenshot](https://i.ibb.co/Ltnnz74/Capture3.png)


## Assumptions

- ContactAPI has support for Contacts with (O..N) numbers of emails, phone numbers and addresses. 
- We are considering Contacts from Brazil. Therefore, phone numbers and addresses should use brazilian patterns.
- Profile image is a URL with the most common image type extensions.
- Only one contact with same First and Last names can be included.
- For more details about the implementation check the documentation and inline comments.



## Demo

## Client (Using AWS Elastic Beanstalk) 

SSL required for POST requests (Create and Update)

http://contactsapitest-env.eba-f2jwqmh7.us-east-1.elasticbeanstalk.com/

![App Screenshot](https://i.ibb.co/zJmwZtT/Demo.png)

## API (Using AWS Lambda) 

SSL required for POST requests (Create and Update)

![App Screenshot](https://i.ibb.co/HTYzKYk/API.png)

https://6ahjvquitxcghde3f4jihyjwcy0vqnov.lambda-url.us-east-1.on.aws/docs


## Documentation

[API Documentation](https://6ahjvquitxcghde3f4jihyjwcy0vqnov.lambda-url.us-east-1.on.aws/docs)


## Run Locally

Clone the project

```bash
  git clone https://github.com/paugusto1/ContactsAPI.git
```

Go to the project directory

```bash
  cd APIRest
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload
```




## Test

Unit tests were included to search endpoint. 

```bash
  pytest test_main.py
```
    
## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedro-vicente-1577a2105/)

