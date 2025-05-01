from dataclasses import dataclass
from pydantic import BaseModel, EmailStr, field_validator
x=10
print(x)
x='hello mr Wahid'
print(x)

@dataclass
class Person:
    name: str
    age: str

ali = Person("Ali", 24) 
print(ali)
ali = Person("Ali", "24")
print(ali) 

# Using Pydantic
class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int

    @field_validator("account_id")
    def validate_account_id(cls, value):
        if value <= 0:
            raise ValueError(f"account_id must be positive: {value}")
        return value

user = User(
    name = "Salah",
    email = "salah@gmail.com",
    account_id = 12345
)
print(user)
user_data = {
    'name': 'Samir',
    'email': 'samir@gmail.com',
    'account_id': 54321
}

user1 = User(**user_data)
print(user1)
print(user.name)   
print(user.email)    
print(user.account_id)

#user3 = User(name = 'Ali', email = 'ali@gmailcom', account_id = 'hello')
#user = User(name = 'Ali', email = 'ali', account_id = 1234)
#print(user)



# you will get a validation error with account_id = -12
user = User(name = 'Ali', email = 'ali@gmail.com', account_id = 12)
print(user)

user_json_str = user.model_dump_json()
# this will return a JSON strinf representation of the model's data
print(user_json_str)
user_json_obj = user.model_dump()
print(user_json_obj)
json_str = '{"name": "Ali", "email": "ali@gmail.com", "account_id": 1234}'
user = User.model_validate_json(json_str)
print(user)

