# backend/app/schemas/user.py

from pydantic import BaseModel, Field

#
# 1. Shared properties for reading and creating a user
#
class UserBase(BaseModel):
    phone: str = Field(..., example="+15551231234", description="Unique phone number for login")
    full_name: str = Field(..., example="Jane Doe", description="User’s full name")
    is_manager: bool = Field(
        False,
        description="Whether this user has manager privileges (staff vs. manager)"
    )

#
# 2. Incoming data for registration
#
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Plain-text password to hash and store")

#
# 3. Incoming data for login
#
class UserLogin(BaseModel):
    phone: str = Field(..., example="+15551231234", description="Registered phone number")
    password: str = Field(..., min_length=8, description="User’s password")

#
# 4. Outgoing data after registration or lookup
#
class UserRead(UserBase):
    id: int = Field(..., description="Database ID of the user")

    class Config:
        orm_mode = True  # allow returning SQLAlchemy models directly

#
# 5. JWT token response model
#
class Token(BaseModel):
    access_token: str = Field(..., description="JWT for Authorization header")
    token_type: str = Field("bearer", const=True, description="Type of the token, always 'bearer'")

#
# 6. Password reset request model
#
class PasswordResetRequest(BaseModel):
    phone: str = Field(
        ...,
        example="+15551231234",
        description="Phone number of the user requesting a password reset"
    )

#
# 7. Password reset execution model
#
class PasswordReset(BaseModel):
    token: str = Field(..., description="Reset token sent via SMS/email")
    new_password: str = Field(
        ...,
        min_length=8,
        description="New password to replace the old one"
    )
