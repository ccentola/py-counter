from fastapi import FastAPI


def get_db():
    pass


app = FastAPI()


@app.get("/")
def home():
    return "hello"
