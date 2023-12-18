import uvicorn


def launch_api():
    """Launches api."""
    uvicorn.run(
        "file_data_transfer_api.main:app",
        host="127.0.0.1",
        port=8000,
        reload_dirs="file_data_transfer_api",
        reload=True
    )


if __name__ == '__main__':
    launch_api()
