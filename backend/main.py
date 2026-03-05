from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.api import users
from backend.db.database import Base, engine


# create tables (for demo only; use Alembic in real projects)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(on_startup=[init_models])

# configure CORS
FRONTEND_ORIGIN = "http://localhost:3000"  # adjust to your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)


def main():
    uvicorn.run(app="backend.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
