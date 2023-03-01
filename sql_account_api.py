import win32com.client
import datetime
from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel
import json

ComServer = win32com.client.Dispatch("SQLAcc.BizApp")

def CheckLogin():
    B = ComServer.IsLogin
    if B == True:
        ComServer.Logout()
    ComServer.Login("ADMIN", "ADMIN", #UserName, Password
                    "C:\eStream\SQLAccounting\Share\Default.DCF",  #DCF file
                    "ACC-0002 (2).FDB") #Database Name

CheckLogin()

app = FastAPI()



class Item(BaseModel):
    DOCKEY: Union[str, None] = None
    DOCNO: Union[str, None] = None
    DOCNOEX: Union[str, None] = None
    DOCDATE: Union[str, None] = None
    POSTDATE: Union[str, None] = None
    TAXDATE: Union[str, None] = None
    CODE: Union[str, None] = None
    COMPANYNAME: Union[str, None] = None
    ADDRESS1: Union[str, None] = None
    ADDRESS2: Union[str, None] = None
    ADDRESS3: Union[str, None] = None
    ADDRESS4: Union[str, None] = None
    PHONE1: Union[str, None] = None
    MOBILE: Union[str, None] = None
    FAX1: Union[str, None] = None
    ATTENTION: Union[str, None] = None
    AREA: Union[str, None] = None
    AGENT: Union[str, None] = None
    PROJECT: Union[str, None] = None
    TERMS: Union[str, None] = None
    CURRENCYCODE: Union[str, None] = None
    CURRENCYRATE: Union[str, None] = None
    SHIPPER: Union[str, None] = None
    DESCRIPTION: Union[str, None] = None
    COUNTRY: Union[str, None] = None
    CANCELLED: Union[str, None] = None
    DOCAMT: Union[str, None] = None
    LOCALDOCAMT: Union[str, None] = None
    D_AMOUNT: Union[str, None] = None
    P_DOCNO: Union[str, None] = None
    P_PAYMENTMETHOD: Union[str, None] = None
    P_CHEQUENUMBER: Union[str, None] = None
    P_PAYMENTPROJECT: Union[str, None] = None
    P_BANKCHARGE: Union[str, None] = None
    P_BANKCHARGEACCOUNT: Union[str, None] = None
    P_AMOUNT: Union[str, None] = None
    P_PAIDAMOUNT: Union[str, None] = None
    VALIDITY: Union[str, None] = None
    DELIVERYTERM: Union[str, None] = None
    CC: Union[str, None] = None
    DOCREF1: Union[str, None] = None
    DOCREF2: Union[str, None] = None
    DOCREF3: Union[str, None] = None
    DOCREF4: Union[str, None] = None
    BRANCHNAME: Union[str, None] = None
    DADDRESS1: Union[str, None] = None
    DADDRESS2: Union[str, None] = None
    DADDRESS3: Union[str, None] = None
    DADDRESS4: Union[str, None] = None
    DATTENTION: Union[str, None] = None
    DPHONE1: Union[str, None] = None
    DMOBILE: Union[str, None] = None
    DFAX1: Union[str, None] = None
    TAXEXEMPTNO: Union[str, None] = None
    ATTACHMENTS: Union[str, None] = None
    NOTE: Union[str, None] = None
    TRANSFERABLE: Union[str, None] = None
    UPDATECOUNT: Union[str, None] = None
    PRINTCOUNT: Union[str, None] = None
    # detailList: Union[Union[str, None], None] = None
    # detailList: Set[dict] = set()
    detailList: list[dict] = []



@app.get("/")
def read_root():
    # return {"Hello": "World"}
    return "SQL Accounting API"



@app.get("/{doctype_name}/getAll")
# async def read_item(doctype_name: str, q: Union[str, None] = None):
async def read_all_item(doctype_name: str):
    
    lSQL = f"SELECT * FROM {doctype_name}"
    lDataSet = ComServer.DBManager.NewDataSet(lSQL)
    # n = 0
    aa = ""
    aaa = ""
    # tt = ""
    lst = []

    while not lDataSet.eof:
        fc = lDataSet.Fields.Count
        for x in range(fc-1):
            fn = lDataSet.Fields.Items(x).FieldName
            fv = lDataSet.FindField(fn).AsString
            lresult = f'"{fn}": "{fv}"' + ','
            # "Index : "+ str(x) + " FieldName : " + fn + " Value : " + fv
            # print ("{" + lresult + "}")
            aa = aa + lresult
            # print(lresult)
            # print("====")
            # print(aa)
            # print ("[" + lresult + "]")
            # return lresult
        fn = lDataSet.Fields.Items(fc-1).FieldName
        fv = lDataSet.FindField(fn).AsString
        lresult = f'"{fn}": "{fv}"'
        aa = aa + lresult
        # print("====")
        # n = n+1
        bb = "{" + aa + "}"
        aaa = json.loads(bb)
        lst.append(aaa)
        lDataSet.Next()
        aa = ""
        # tt = tt + aaa
        # print(aa)
        # aaa = aaa + aaa
        # aaaa = "[" + aaa + "]"
        # aaaa = tt.split(';')
        # aaa = "[" + aa + "]"
    
    # my = lDataSet.FindField("DocNo").AsString

    # return {"doctype_name": my}
    # return f"Done. {n} record"
    # print(aaaa)
    return lst



@app.get("/{doctype_name}/getall")
async def read_all_item(doctype_name: str):    
    lSQL = f"SELECT * FROM {doctype_name}"
    lDataSet = ComServer.DBManager.NewDataSet(lSQL)
    aa = ""
    aaa = ""
    lst = []
    while not lDataSet.eof:
        fc = lDataSet.Fields.Count
        for x in range(fc-1):
            fn = lDataSet.Fields.Items(x).FieldName
            fv = lDataSet.FindField(fn).AsString
            lresult = f'"{fn}": "{fv}"' + ','
            aa = aa + lresult
        fn = lDataSet.Fields.Items(fc-1).FieldName
        fv = lDataSet.FindField(fn).AsString
        lresult = f'"{fn}": "{fv}"'
        aa = aa + lresult
        bb = "{" + aa + "}"
        aaa = json.loads(bb)
        lst.append(aaa)
        lDataSet.Next()
        aa = ""
    return lst



@app.post("/{doctype_name}/add")
async def create_item(doctype_name: str, data: Item):
    BizObject = ComServer.BizObjects.Find(f"{doctype_name}")
    lMain = BizObject.DataSets.Find("MainDataSet") #lMain contains master data
    lDetail = BizObject.DataSets.Find("cdsDocDetail") #lDetail contains detail data

    # lDate = datetime.datetime.today()

    BizObject.New();
    # lMain.FindField("DocKey").value = -1
    if data.DOCNO is not None:
        lMain.FindField("DocNo").AsString = f"{data.DOCNO}"
    if data.DOCDATE is not None:
        lDate = data.DOCDATE
        lMain.FindField("DocDate").value =  lDate.strftime('%m/%d/%Y')
    # lMain.FindField("PostDate").value = data.POSTDATE
    if data.CODE is not None:
        lMain.FindField("Code").AsString = f"{data.CODE}"
    if data.COMPANYNAME is not None:
        lMain.FindField("CompanyName").AsString = data.COMPANYNAME
    if data.ADDRESS1 is not None:
        lMain.FindField("Address1").AsString = data.ADDRESS1
    # lMain.FindField("Address2").AsString = data.ADDRESS2
    # lMain.FindField("Address3").AsString = data.ADDRESS3
    # lMain.FindField("Address4").AsString = data.ADDRESS4
    # lMain.FindField("Phone1").AsString = data.PHONE1
    if data.DESCRIPTION is not None:
        lMain.FindField("Description").AsString = data.DESCRIPTION

    if data.detailList is not None:
        for child in data.detailList:

            lDetail.Append()
            # lDetail.FindField("DtlKey").value = -1
            # lDetail.FindField("DocKey").value = -1
            # lDetail.FindField("Seq").value = 1
            # lDetail.FindField("Account").AsString = "500-000" #Sales Account
            if child["ITEMCODE"] is not None:
                lDetail.FindField("ItemCode").AsString = child["ITEMCODE"]
            # lDetail.FindField("Account").AsString = "500-000"
            if child["DESCRIPTION"] is not None:
                lDetail.FindField("Description").AsString = child["DESCRIPTION"]
            if child["QTY"] is not None:
                lDetail.FindField("Qty").AsFloat = child["QTY"]
            if child["DISC"] is not None:
                lDetail.FindField("DISC").AsString = child["DISC"]
            if child["UOM"] is not None:
                lDetail.FindField("UOM").AsString = child["UOM"]
            if child["TAX"] is not None:
                lDetail.FindField("Tax").AsString = child["TAX"]
            if child["TAXRATE"] is not None:
                lDetail.FindField("TaxRate").AsString = child["TAXRATE"]
            # if child["TAXINCLUSIVE"] is not None:
                # lDetail.FindField("TaxInclusive").value = child["TAXINCLUSIVE"]
            if child["UNITPRICE"] is not None:
                lDetail.FindField("UnitPrice").AsFloat = child["UNITPRICE"]
            if child["AMOUNT"] is not None:
                lDetail.FindField("Amount").AsFloat = child["AMOUNT"]
            if child["TAXAMT"] is not None:
                lDetail.FindField("TaxAmt").AsFloat = child["TAXAMT"]
            if child["AmountWithTax"] is not None:
                lDetail.FindField("AmountWithTax").AsFloat = child["AmountWithTax"]
            lDetail.Post()
    BizObject.Save()
    BizObject.Close()

    return "done"



@app.put("/{doctype_name}/edit")
async def update_item(doctype_name:str, data: Item):
    BizObject = ComServer.BizObjects.Find(f"{doctype_name}")
    lMain = BizObject.DataSets.Find("MainDataSet")
    lDetail = BizObject.DataSets.Find("cdsDocDetail") #lDetail contains detail data

    
    # lDocKey = BizObject.FindKeyByRef("DocNo", "--IV Test--")
    lDocKey = BizObject.FindKeyByRef("DocNo", f"{data.DOCNO}")
        
    if lDocKey is None:
        # BizObject.New()
        # lMain.FindField("CODE").value = "FAIRY"
        # lMain.FindField("DESCRIPTION").value = "FAIRY TAIL"
        print ("Record Not Found")
    else:
        BizObject.Params.Find("DocKey").Value = lDocKey
        BizObject.Open()
        BizObject.Edit()
        if data.DOCDATE is not None:
            lMain.FindField("DocDate").value = data.DOCDATE
        if data.POSTDATE is not None:
            lMain.FindField("PostDate").value = data.POSTDATE
        if data.CODE is not None:
            lMain.FindField("Code").AsString = data.CODE
        if data.COMPANYNAME is not None:
            lMain.FindField("CompanyName").AsString = data.COMPANYNAME
        if data.ADDRESS1 is not None:
            lMain.FindField("Address1").AsString = data.ADDRESS1
        # lMain.FindField("Address2").AsString = data.ADDRESS2
        # lMain.FindField("Address3").AsString = data.ADDRESS3
        # lMain.FindField("Address4").AsString = data.ADDRESS4
        # lMain.FindField("Phone1").AsString = data.PHONE1
        if data.DESCRIPTION is not None:
            lMain.FindField("Description").AsString = data.DESCRIPTION

        if data.detailList is not None:
            for child in data.detailList:

                lDetail.Append()
                # lDetail.FindField("DtlKey").value = -1
                # lDetail.FindField("DocKey").value = -1
                # lDetail.FindField("Seq").value = 1
                # lDetail.FindField("Account").AsString = "500-000" #Sales Account
                if child["ITEMCODE"] is not None:
                    lDetail.FindField("ItemCode").AsString = child["ITEMCODE"]
                # lDetail.FindField("Account").AsString = "500-000"
                if child["DESCRIPTION"] is not None:
                    lDetail.FindField("Description").AsString = child["DESCRIPTION"]
                if child["QTY"] is not None:
                    lDetail.FindField("Qty").AsFloat = child["QTY"]
                if child["DISC"] is not None:
                    lDetail.FindField("DISC").AsString = child["DISC"]
                if child["UOM"] is not None:
                    lDetail.FindField("UOM").AsString = child["UOM"]
                if child["TAX"] is not None:
                    lDetail.FindField("Tax").AsString = child["TAX"]
                if child["TAXRATE"] is not None:
                    lDetail.FindField("TaxRate").AsString = child["TAXRATE"]
                # if child["TAXINCLUSIVE"] is not None:
                    # lDetail.FindField("TaxInclusive").value = child["TAXINCLUSIVE"]
                if child["UNITPRICE"] is not None:
                    lDetail.FindField("UnitPrice").AsFloat = child["UNITPRICE"]
                if child["AMOUNT"] is not None:
                    lDetail.FindField("Amount").AsFloat = child["AMOUNT"]
                if child["TAXAMT"] is not None:
                    lDetail.FindField("TaxAmt").AsFloat = child["TAXAMT"]
                if child["AmountWithTax"] is not None:
                    lDetail.FindField("AmountWithTax").AsFloat = child["AmountWithTax"]
                lDetail.Post()
        
    try:
        BizObject.Save()
    except Exception as e:
        print("Oops!", e)    
    # print ("Done")
    return "Done"



@app.delete("/{doctype_name}/delete/{key}")
async def delete_item(doctype_name: str, key: str):
    BizObject = ComServer.BizObjects.Find(f"{doctype_name}")
    lDocKey = BizObject.FindKeyByRef("DocNo", f"{key}")
        
    if lDocKey is None:
        print ("Not Found...")
    else:
        try:
            BizObject.Params.Find("Dockey").Value = lDocKey            
            BizObject.Open()
            BizObject.Delete()
        except Exception as e:
            print("Oops!", e)
    BizObject.Close()    
    print ("Done")



######################################################################################



@app.get("/{doctype_name}/getDetail/{element}")
async def read_all_item_details(doctype_name: str, element: str):    
    BizObject = ComServer.BizObjects.Find(f"{doctype_name}")
    lMain = BizObject.DataSets.Find("MainDataSet") #lMain contains master data
    lDetail = BizObject.DataSets.Find("cdsDocDetail") #lDetail contains detail data
    lknockoff = BizObject.DataSets.Find("cdsKnockOff")
    
   #  lDocKey = BizObject.FindKeyByRef("CODE", "300-C0001")
    lDocKey = BizObject.FindKeyByRef("DocNo", f"{element}")
    aa = ""
    aaa = ""
    lst = []
        
    # if lDocKey is None:
    #     print("no record")
    # else:
    BizObject.Params.Find("DocKey").Value = lDocKey
    BizObject.Open()
    BizObject.Edit()
    # lMain.FindField("DESCRIPTION").value = "FAIRY TAIL WIZARD"
    # print(lMain.FindField("DESCRIPTION").value)
    # while not lDataSet.eof
    # print(lDetail.Fields.Count)
   
    if lDetail:
        while not lDetail.eof:
            fc = lDetail.Fields.Count
            for x in range(fc-1):
                fn = lDetail.Fields.Items(x).FieldName
                fv = lDetail.FindField(fn).AsString
                lresult = f'"{fn}": "{fv}"' + ','
                aa = aa + lresult
            fn = lDetail.Fields.Items(fc-1).FieldName
            fv = lDetail.FindField(fn).AsString
            lresult = f'"{fn}": "{fv}"'
            aa = aa + lresult
            bb = "{" + aa + "}"
            aaa = json.loads(bb)
            lst.append(aaa)
            lDetail.Next()
            aa = ""
    else:
        while not lknockoff.eof:
            fc = lknockoff.Fields.Count
            for x in range(fc-1):
                fn = lknockoff.Fields.Items(x).FieldName
                fv = lknockoff.FindField(fn).AsString
                lresult = f'"{fn}": "{fv}"' + ','
                aa = aa + lresult
            fn = lknockoff.Fields.Items(fc-1).FieldName
            fv = lknockoff.FindField(fn).AsString
            lresult = f'"{fn}": "{fv}"'
            aa = aa + lresult
            bb = "{" + aa + "}"
            aaa = json.loads(bb)
            lst.append(aaa)
            lknockoff.Next()
            aa = ""

    return lst
