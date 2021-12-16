from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic.types import UUID4

from models import User, Role, Gender

app = FastAPI()

db: List[User] = [
    User(id=UUID4("4a7abbea-a231-449c-94c4-84bbff4f586c"),
         first_name="Jamila",
         last_name="sanchez",
         gender=Gender.female,
         roles=[Role.student]
         ),

    User(id=UUID4("79108352-ce28-4b65-b84e-f38cc71fe614"),
         first_name="Alex",
         last_name="Jones",
         gender=Gender.male,
         roles=[Role.admin, Role.user]
         )
]

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get('/api/vi/users')
async def fetch_users():
    return db;

@app.post("/api/vi/users") #same ressource because the method change from get to post
async def register_user(user: User): #User is the entity while user is what we recieve from this request
    db.append(user)
    return {"id": user.id}

@app.delete("/api/vi/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException( #if the user is not deleted then ...
        status_code=404,
        detail = f"user with id: {user_id} does not exists"
    )
