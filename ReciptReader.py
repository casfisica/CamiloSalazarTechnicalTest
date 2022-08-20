import re

class ReciptReader:
    """
        Attributes
        ----------
        file : str
            text file name (include)
        company : str
            t
        date : str
            t
        address : str
            t
        total : str
            t
        line_items : Array
            Array of dictionarys with keys:"sku","quantity","price","total"

        Methods
        -------
        setComponets()
            p
        getComponets()
            P

    """
    def __init__(self, file = None):
        """
        ReciptReader constructor
        
        Parameters
        ----------
        file : str
            Text file name (include)     
        """

        if file == None : 
            raise ValueError('you need to specify file name')
            
        self.file = file
        self.company = None
        self.date = None
        self.total = None
        self.address = ""
        self.line_items = []
        self.setComponets()

    def setComponets(self):
        """
        Fill the Attributes company, date, total, address and line_items
        
        Parameters
        ----------
        None
        """
        with open(self.file,'r') as OCR_file:
            #Address array
            addressArray = []
            addressStart = None
            addressEnd = None
            # read the content of the file opened
            content = OCR_file.readlines()
            # length
            length = len(content)
            #iterate over lines in the OCR text
            #Item
            itemStar = None
            itemEnd = None
            for l in range(length):
                line = content[l]
                #Get address
                patternAddStart= re.compile('CO\.')
                patternAddEnd= re.compile(r'\-INVOICE\-')
                if re.findall(patternAddStart,line): 
                    addressStart = l+1
                if re.findall(patternAddEnd,line): 
                    addressEnd = l

                #Get name of the company
                patternCo= re.compile(r'CO\.')
                if re.findall(patternCo, line):
                    #print("Company Name:",getTextAfterCharRep(content[l-1]))
                    self.company = getTextAfterCharRep(content[l-1]).replace('\n','')
                    

                #Get the date
                patternDa= re.compile('CASHIER')
                if re.findall(patternDa, line):
                    #print("Date:",getTextAfterCharRep(content[l-1]))
                    self.date = getTextAfterCharRep(content[l-2])[:8]


                #Get TOTAL
                patternCo= re.compile(r'(TOTAL)$')
                if re.findall(patternCo, line):
                    #print('TOTAL:',getTextAfterCharRep(content[l+1]).replace('RM ',''))
                    self.total = getTextAfterCharRep(content[l+1]).replace('RM ','').replace('\n','')
                
                #Get Items 
                patternItemStart= re.compile(r'\-INVOICE\-')
                patternItemEnd= re.compile(r'ITEM')
                if re.findall(patternItemStart, line): 
                    #To start in the item
                    itemStar = l+1
                if re.findall(patternItemEnd, line): 
                    itemEnd = l

            #To start recovery of the address
            for k in range(addressStart,addressEnd):
                #print(getTextAfterCharRep(content[k]))
                addressArray.append(getTextAfterCharRep(content[k]))
            # Format the address
            for i in addressArray:
                self.address += i.replace('\n','')
            #print(textAdd)


            mask = ['name','reference','sku','quantity','x','price','Total']
            #
            Selected = (len(range(itemStar,itemEnd))//7)*mask
            #Loop over itmes properties
            #print(Selected)
            #print(range(itemStar,itemEnd))
            for (i, j) in zip(range(itemStar,itemEnd),Selected):
                #print(j,': ',getTextAfterCharRep(content[i]).replace('\n',''))
                if j == 'sku':
                    self.line_items.append(
                        {
                            "sku": getTextAfterCharRep(content[i]).replace('\n',''),
                            "quantity": getTextAfterCharRep(content[i+1]).replace('\n',''),
                            "price": getTextAfterCharRep(content[i+3]).replace('\n',''),
                            "total": getTextAfterCharRep(content[i+4]).replace('\n','')
                        }
                    )


    def getComponets(self):
        """
        
        """
        dic = {
                "company": self.company,
                "date": self.date,
                "address": self.address,
                "line_items": self.line_items,
                "total": self.total
        }
        return dic

def getTextAfterCharRep(stringText, char = r'\,' , num = 8):
    """
    Get the text after a string (char), repeted a number (num) of times
        
    Parameters
    ----------
    stringText : str
        The 
    char : str
        The 
    num : int, optional
        The number of  (default is 8)
    
    """
    indexPrint = [(m.start(0), m.end(0)) for m in re.finditer(char,stringText )][num-1][1]
    return stringText[indexPrint:]

if __name__ == "__main__":
    print("")