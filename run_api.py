import uvicorn
from loguru import logger

if __name__ == "__main__":
    logger.add("logs/api.log", rotation="500 MB")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
