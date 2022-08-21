import uvicorn

from shortify.app.core.config import settings


def run_dev_server() -> None:
    """Run the uvicorn server in development environment."""
    uvicorn.run(
        "shortify.app.main:app",  # path to the FastAPI application
        host="127.0.0.1" if settings.DEBUG else "0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    run_dev_server()
