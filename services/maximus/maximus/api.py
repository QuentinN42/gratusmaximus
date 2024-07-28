from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def healthcheck():
    return {"healthy": True}
