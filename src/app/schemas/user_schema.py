from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )
