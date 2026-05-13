from fastapi import FastAPI

from app.api.routers import ALL_ROUTERS

app = FastAPI(title="organization_api")

for router in ALL_ROUTERS:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
