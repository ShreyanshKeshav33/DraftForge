Swagger UI- localhost:8000/docs- fastapi generated it automatically it returns al the routes, input, response without writing any documentation. this is one of the reasons companies use fastapi, for example team can open /docs and know exactly whats happening by pinpointing it

dont write duplicate operation because it breaks the doucmentation. example
@app.get("/health")
@app.get("/health")
2 times

