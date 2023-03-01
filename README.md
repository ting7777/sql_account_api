## Run SQL Account API

<br/>

### Requirements
- Python 3.7+

<br/>

### Install FastAPI
```console 
pip install fastapi
```

<br/>

### Install Uvicorn server
```console 
pip install "uvicorn[standard]"
```

<br/>

### Download sql_account_api.py file
- [click here to download](sql_account_api.py)
- <a href="/sql_account_api.py" download>Click to Download</a>
- {{< a href="sql_account_api.py" download="download" >}}
Click here to download
{{< /a >}}

### Open PowerShell and Navigate to the folder containing the downloaded file

### Run the server with:
```console 
uvicorn sqlapi:app --reload
```

<br/>

The following output should be displayed, indicating the port on which the API is currently running.
![api](pic.png)