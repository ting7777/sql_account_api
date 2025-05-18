## Run SQL Account API

### Requirements
- Python 3.13+

### Install FastAPI
```console 
py -m ensurepip --upgrade
py -m pip install --upgrade pip
py -m pip install fastapi
```

### Install Uvicorn server
```console 
py -m pip install "uvicorn[standard]"
```

### Install pywin32
```console 
py -m pip install pywin32
```

### Install Git for Windows
https://git-scm.com/download/win

### Open PowerShell and run the following command line:
```console 
git clone https://github.com/Nb-Richard/sql_account_api
```

### Navigate to the cloned folder
```console 
cd sql_account_api
```

### Run the server with:
```console 
py -m uvicorn sql_account_api:app --reload
```

<br/>

**The following output should be displayed, indicating the port on which the API is currently running.**  

![api](pic.png)