from dataclasses import dataclass
from fastapi import FastAPI
from scripts.core.services.mis_report_service import mis_router


@dataclass
class FastAPIConfig:
    title: str = "Sample App"
    version: str = "1.0.0"
    description: str = "Sample App Description"


app = FastAPI(**FastAPIConfig().__dict__)
app.include_router(mis_router)

# app = FastAPI()
# import uvicorn
# #
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)