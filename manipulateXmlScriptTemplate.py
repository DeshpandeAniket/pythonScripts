##imports
import xml.etree.ElementTree as ET
import mysql.connector as db
import re
import urllib.parse as rawurl
import pycurl

##constants

#STAGE
UPLOAD_URL = '##URL##'
USERNAME = "root"  # USERNAME##
PASSWORD = ""  # PASSWORD##
HOSTNAME = "localhost"  # HOSTNAME##
DATABASENAME = "root"  # DATABASENAME##
QUERY = ""
FILEPATH = '##INPUTFILEPATH##'
FILEOUTPUTPATH = '##OUTPUTFILEPATH##'
FILENAME = "output.xml"
XMLTEMPLATEFILENAMENAME = "xmlTemplate.xml"
PLACEHOLDERS = {}

"""
context manager for databases connection
@input hostname, username, password, databasename
@return database connection
"""
class mysqlDatabaseConnection():
    def __init__(self, hostname, user, password, databaseName):
        self.hostname = hostname
        self.user = user
        self.password = password
        self.databaseName = databaseName

    def __enter__(self):
            self.connection = db.connect(
                host=self.hostname, user=self.user, password=self.password, database=self.databaseName)
            return self.connection

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection.close()


"""
Function to Connect and Retrive database 
values
"""
def getDatabaseValues():
    ## HOSTNAME, USERNAME, PASSWORD, DATABASENAME##
    with mysqlDatabaseConnection(HOSTNAME, USERNAME, PASSWORD, DATABASENAME) as conn:
        executer = conn.cursor()
        executer.execute(QUERY)
        dataset = executer.fetchall()
        return dataset


"""
Function to find element 
@return child element
"""
def findElement(parent, childName):
    return parent.find(childName)


"""
Function to get content of file
@input filePath, fileName
@return FileContent
"""
def getFileContent(filePath, fileName):
    with open(filePath+fileName) as f:    
        data = f.read()  
        return data

"""
Function to push content of file
@input filePath, fileName
@return BOOLEAN
"""
def putContentToFile(fileOutputPath, fileName, content):
    with open(fileOutputPath+fileName) as f:    
        f.write(content)
        print("SAVED")


"""
Function used to Replace PlaceHolders with Data
@input data, contentwithplaceholders
@return replaced string
"""
def replacePlaceHolders(data, content):
    for x,y in PLACEHOLDERS.items():
        content = re.sub(y, data[x], content)
    return content


def createXmlTemplate(xmlTemplate, fileContent, row):
    # updatedContent = replacePlaceHolders(row, fileContent)
    ## TO DO
    tree =  ET.fromstring(xmlTemplate)
    website = findElement(tree, "WEBSITE")
    pages = findElement(website, "PAGES")
    page = findElement(pages, "PAGE")
    PAGE_NAME = findElement(page, "PAGE_NAME")
    PAGE_NAME.text = 0
    return True

def pushXmlToCMS(generatedXML):
    c = pycurl.Curl()
    c.setopt(pycurl.URL, UPLOAD_URL)
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.POSTFIELDS, "##POSTFIELDDATA##")
    c.perform()

"""
logic execution is starts
"""

def main():
    #pull data from DATABASE
    dataSet = getDatabaseValues()
    #get body content template
    fileContent = getFileContent(FILEPATH, FILENAME)
    #get xml content template
    xmlTemplate = getFileContent(FILEPATH, XMLTEMPLATEFILENAMENAME)
    for row in dataSet:
        OUTPUTFILENAME = row["CITYNAME"] + ".xml"
        generatedXML = createXmlTemplate(xmlTemplate, fileContent, row)
        putContentToFile(FILEOUTPUTPATH, OUTPUTFILENAME, generatedXML)
        pushXmlToCMS(generatedXML)

## execution starts here
if __name__ == "__main__":
    main()
