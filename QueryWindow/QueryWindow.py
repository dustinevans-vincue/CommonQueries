'''
Created on May 19, 2026

@author: admin
'''

# import json
import tkinter as tk
from tkinter import ttk
#    from tkinter import messagebox
# from os import getenv
from dotenv import load_dotenv
from mssql_python import connect 

def backHome():
    for item in frm.winfo_children():
        item.destroy()
        
    homeSetup()
    
def homeSetup():
    ttk.Label(frm, text = "Select the query to run").grid(row = 0, column = 1)
    ttk.Button(frm, text = "Inventory counts by dealer", command = invByDealerSetup).grid(row = 2, column = 0)
    ttk.Button(frm, text = "Inventory counts by group", command = invByGroupSetup).grid(row = 2, column = 1)
    ttk.Button(frm, text = "Inventory counts by make", command = invByMakeSetup).grid(row = 2, column = 2)
    ttk.Button(frm, text = "Import history date search", command = importByDaySetup).grid(row = 3, column = 0)
    ttk.Button(frm, text = "Import history name search", command = importByImportSetup).grid(row = 3, column = 1)
    
def clearScreen():
    for item in frm.winfo_children():
        item.destroy()
        
    ttk.Button(frm, text = 'Back', command = backHome).grid(row = 0, column = 1)
    
def formatTable(tableString):
    # recordString = str(tableString).replace('}{', '\n')
    recordString = str(tableString).replace('[', '').replace(']', '')
    recordString = recordString.replace('), (', '\n')
    recordString = recordString.replace('(', '').replace(')', '')
    recordString = recordString.replace("'", '').replace("'", '')

    return recordString

def invByDealerSetup():
    
    def charCheck(event):
        maxChars = 6
    
        text = idInput.get("1.0", "end-1c")
        textLen = len(text)
        if textLen >= maxChars and event.keysym not in {'BackSpace', 'Delete', 'Return'}: 
            return 'break'
        
    def invByDealerPull(event):
        dealerID = idInput.get("1.0", "end-1c")
        if dealerID == '':
            ttk.Label(frm, text = 'You done goofed').grid(row = 4, column = 1)
        else:    
            clearScreen()
        
            sqlQueryIn = """select case when listingtypeid = 1 then 'New' else 'Used' end, 
            case when donotexport = 0 then 'Off Hold' else 'On Hold' end, 
            count(vin) 
            from dealersite..inventory 
            where dealerid = 
            and inventorystatusid = 1 
            group by listingtypeid, donotexport 
            order by listingtypeid, donotexport"""
            
            sqlQuery = sqlQueryIn.replace("where dealerid = ", "where dealerid = " + dealerID)
            
            ttk.Label(frm, text = "Executing SQL").grid(row = 1, column = 1)
            
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            
            records = cursor.fetchall()
            
            formatString = formatTable(records)
            
            ttk.Label(frm, text = formatString).grid(row = 1, column = 1)


    clearScreen()
    
    idLabel = ttk.Label(frm, text = "Enter DealerID here:").grid(row = 1, column = 1)
    idInput = tk.Text(frm, height = 1, width = 6)    
    idInput.grid(row = 2, column = 1)
    
    idInput.bind("<KeyPress>", charCheck)
    idInput.bind("<Return>", invByDealerPull, add = "+")
    
    sendButton = ttk.Button(frm, text = "Send")
    sendButton.grid(row = 3, column = 1)
    sendButton.bind("<Button-1>", invByDealerPull)
            
def invByGroupSetup():
    def charCheck(event):
        maxChars = 20
    
        text = idInput.get("1.0", "end-1c")
        textLen = len(text)
        if textLen >= maxChars and event.keysym not in {'BackSpace', 'Delete', 'Return'}: 
            return 'break'
    
    def invByGroupPull(event):
        groupName = idInput.get("1.0", "end-1c")
        if groupName == '':
            ttk.Label(frm, text = 'You done goofed').grid(row = 4, column = 1)
        else:
            clearScreen()
            
            sqlQueryIn = """select 
            d.dealerid, 
            d.dealername,
            d.city,
            case when listingtypeid = 1 then 'New' else 'Used' end,
            case when donotexport = 0 then 'Off Hold' else 'On Hold' end,
            count(vin)
            from dealersite..inventory i
            left join admin..Dealer d on d.dealerid = i.DealerID
            left join admin..Account_Dealer ad on d.DealerID = ad.DealerID
            left join admin..account a on a.AccountID = ad.AccountID
            where inventorystatusid = 1
            and d.ClientInd = 1
            and a.name like '%
            group by d.dealerid, d.dealername, d.city, listingtypeid, donotexport
            order by d.dealerid, d.dealername, d.city, listingtypeid, donotexport"""
                
            sqlQuery = sqlQueryIn.replace("and a.name like '%", "and a.name like '%" + groupName + "%'")
            
            ttk.Label(frm, text = "Executing SQL").grid(row = 1, column = 1)
            
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            
            records = cursor.fetchall()
            
            formatString = formatTable(records)
            
            ttk.Label(frm, text = formatString).grid(row = 1, column = 1)


    clearScreen()
    
    ttk.Label(frm, text = "Enter group name here:").grid(row = 1, column = 1)
    idInput = tk.Text(frm, height = 1, width = 20)
    idInput.grid(row = 2, column = 1)
    sendButton = ttk.Button(frm, text = "Send")
    sendButton.grid(row = 3, column = 1)
    
    idInput.bind("<KeyPress>", charCheck)
    idInput.bind("<Return>", invByGroupPull, add = "+")
    sendButton.bind("<Button-1>", invByGroupPull)
    
    
    
def invByMakeSetup():
    def charCheck(event):
        maxChars = 6
    
        text = idInput.get("1.0", "end-1c")
        textLen = len(text)
        if textLen >= maxChars and event.keysym not in {'BackSpace', 'Delete', 'Return'}: 
            return 'break'

    def invByMakePull(event):
        dealerID = idInput.get("1.0", "end-1c")
        if dealerID == '':
            exit()
            
            
        clearScreen()
        
        sqlQueryIn = """select
        case when listingtypeid = 1 then 'New' else 'Used' end,
        make,
        case when donotexport = 0 then 'Off Hold' else 'On Hold' end,
        count(vin)
        from DealerSite..inventory
        where dealerid = 
        and InventoryStatusId = 1
        group by listingtypeid, Make, donotexport
        order by listingtypeid, make, donotexport"""
        
        
        sqlQuery = sqlQueryIn.replace("where dealerid = ", "where dealerid = " + dealerID)
        
        ttk.Label(frm, text = "Executing SQL").grid(row = 1, column = 1)
        
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
        
        records = cursor.fetchall()
        
        formatString = formatTable(records)
        
        ttk.Label(frm, text = formatString).grid(row = 1, column = 1)

    
    clearScreen()
    
    ttk.Label(frm, text = "Enter DealerID here:").grid(row = 1, column = 1)
    idInput = tk.Text(frm, height = 1, width = 6)
    idInput.grid(row = 2, column = 1)
    sendButton = ttk.Button(frm, text = "Send")
    sendButton.grid(row = 3, column = 1)
    
    idInput.bind("<KeyPress>", charCheck)
    idInput.bind("<Return>", invByMakePull, add = '+')
    sendButton.bind("<Button-1>", invByMakePull)

    
    
##
# main starts here
##

def importByDaySetup():
    def charCheck(event):
        maxChars = 6
    
        text = idInput.get("1.0", "end-1c")
        textLen = len(text)
        if textLen >= maxChars and event.keysym not in {'BackSpace', 'Delete', 'Return'}: 
            return 'break'
        
    def importByDayPull(event):
        dealerID = idInput.get("1.0", "end-1c")
        if dealerID == '':
            exit()
        
        days = dayInput.get("1.0", "end-1c")
        if days == '':
            exit()    
            
        clearScreen()
        
        sqlQueryIn = """select si.ImportName, fi.FileName, ih.FileVersionID, ih.HistoryDate
        from integration..Import_History ih
        left join Integration..file_version fv on ih.FileVersionID = fv.FileVersionID
        left join Integration..File_Info fi on fv.fileid = fi.FileID
        left join Integration..Source_Import si on si.ImportProcessorID = ih.ImportProcessorID
        where ih.dealerid = 
        and ih.HistoryDate > dateadd(day, -
        order by ih.HistoryDate desc"""
        
        sqlQuery = sqlQueryIn.replace("where ih.dealerid = ", "where ih.dealerid = " + dealerID)
        sqlQuery = sqlQuery.replace("and ih.HistoryDate > dateadd(day, -", "and ih.HistoryDate > dateadd(day, -" + days + ", getdate())")
        
        ttk.Label(frm, text = "Executing SQL").grid(row = 1, column = 1)
        
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
        
        records = cursor.fetchall()
        
        formatString = formatTable(records)
        
        ttk.Label(frm, text = formatString).grid(row = 1, column = 1)


    clearScreen()
    
    ttk.Label(frm, text = "Enter DealerID here:").grid(row = 1, column = 1)
    ttk.Label(frm, text = "Enter number of days to search:").grid(row = 2, column = 1)
    idInput = tk.Text(frm, height = 1, width = 6)
    idInput.grid(row = 1, column = 2)
    dayInput = tk.Text(frm, height = 1, width = 3)
    dayInput.grid(row = 2, column = 2)
    sendButton = ttk.Button(frm, text = "Send")
    sendButton.grid(row = 3, column = 2)
    
    idInput.bind("<KeyPress>", charCheck)
    sendButton.bind("<Button-1>", importByDayPull)
    
    
def importByImportSetup():
    def charCheckDealer(event):
        maxChars = 6
    
        text = idInput.get("1.0", "end-1c")
        textLen = len(text)
        if textLen >= maxChars and event.keysym not in {'BackSpace', 'Delete', 'Return'}: 
            return 'break'
    def charCheckName(event):
        maxChars = 20
    
        text = idInput.get("1.0", "end-1c")
        textLen = len(text)
        if textLen >= maxChars and event.keysym not in {'BackSpace', 'Delete', 'Return'}: 
            return 'break'
        
    def importByImportPull(event):
        dealerID = idInput.get("1.0", "end-1c")
        if dealerID == '':
            exit()
        
        impName = importName.get("1.0", "end-1c")
        if impName == '':
            exit()    
            
        clearScreen()
        
        sqlQueryIn = """select si.ImportName, fi.FileName, ih.FileVersionID, ih.HistoryDate
        from integration..Import_History ih
        left join Integration..file_version fv on ih.FileVersionID = fv.FileVersionID
        left join Integration..File_Info fi on fv.fileid = fi.FileID
        left join Integration..Source_Import si on si.ImportProcessorID = ih.ImportProcessorID
        where ih.dealerid = 
        and ih.ImportProcessorID = (select ImportProcessorID from Integration..Source_Import where ImportName = '
        order by ih.HistoryDate desc"""
        
        sqlQuery = sqlQueryIn.replace("where ih.dealerid = ", "where ih.dealerid = " + dealerID)
        sqlQuery = sqlQuery.replace("and ih.ImportProcessorID = (select ImportProcessorID from Integration..Source_Import where ImportName = '", "and ih.ImportProcessorID = (select ImportProcessorID from Integration..Source_Import where ImportName = '" + impName + "')")
        
        ttk.Label(frm, text = "Executing SQL").grid(row = 1, column = 1)
        
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
        
        records = cursor.fetchall()
        
        formatString = formatTable(records)
        
        ttk.Label(frm, text = formatString).grid(row = 1, column = 1)


    clearScreen()
    
    ttk.Label(frm, text = "Enter DealerID here:").grid(row = 1, column = 1)
    ttk.Label(frm, text = "Enter import name here:").grid(row = 2, column = 1)
    idInput = tk.Text(frm, height = 1, width = 6)
    idInput.grid(row = 1, column = 2)
    importName = tk.Text(frm, height = 1, width = 20)
    importName.grid(row = 2, column = 2)
    sendButton = ttk.Button(frm, text = "Send")
    sendButton.grid(row = 3, column = 2)
    
    idInput.bind("<KeyPress>", charCheckDealer)
    importName.bind("<KeyPress>", charCheckName)
    sendButton.bind("<Button-1>", importByImportPull)
    
    
    
try:
    import pyi_splash
    pyi_splash.close()
except:
    pass

root = tk.Tk()
root.title("Common Queries")
frm = ttk.Frame(root, padding=100)
frm.grid()

homeSetup()

load_dotenv()
conn = connect("Server=192.168.2.19;Encrypt=yes;TrustServerCertificate=yes;Authentication=SqlPassword;UID=integration;PWD=integration")
    
sqlQueryIn = ''

root.mainloop()