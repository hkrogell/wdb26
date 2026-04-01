from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "msg": "Wow docker" }

@app.get("/hello")
def hello():
    return { "msg": "heyheyhey" }