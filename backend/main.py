import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

class Fruit(BaseModel):
  name: str

class Fruits(BaseModel):
  fruits: list[Fruit]

# allows to send request from frontend to backend
# web applications able to access this fastapi application
origins = [
  "http://localhost:8000",

]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_headers=["*"],
  allow_methods=["*"]

)

# in memory db(db exists even when application shuts down)
memory_db = {"fruits": []} # this is a dictionary


@app.get("/fruits", response_model=Fruits)
def get_fruits():
  return Fruits(fruits=memory_db["fruits"]) # fetches the fruits list inside the dictionary and wraps it in the Fruits pydantic model then return to user as JSON response

@app.post("/fruits", response_class=Fruit)
def add_fruit(fruit: Fruit):
  memory_db["fruits"].append(fruit)
  return fruit
