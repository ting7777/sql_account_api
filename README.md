## Run SQL Account API

### Requirements
- Python 3.7+

### Install FastAPI
```console 
pip install fastapi
```

### Install Uvicorn server
```console 
pip install "uvicorn[standard]"
```

### Download sql_account_api.py file
- [click here to download](sql_account_api.py)
- <a href="/sql_account_api.py" download>Click to Download</a>

### Open PowerShell and Navigate to the folder containing the downloaded file

### Run the server with:
```console 
uvicorn sqlapi:app --reload
```

The following output should be displayed, indicating the port on which the API is currently running.
![api](pic.png)