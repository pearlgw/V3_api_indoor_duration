from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str
    verification_token: str
    
# class RegisterRequest(BaseModel):
#     nim: str
#     fullname: str
#     address: str
#     email: str
#     password: str