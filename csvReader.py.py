#
#Create javascript code from Excel file of all brands and their products
# Created by Harry Bartlett
# Modified 10/27/2014
#

import csv

#CSV Reader portion
with open('Brands Page.csv','rU') as file:
    contents = csv.reader(file)
    #raw imported csv data    
    brandList = list()
    #processed csv data
    outList = list()
    #holds abridged url for each broquet picture
    #if unabridged, must change brand paga Javascript code to
    #reflect that.
    picUrlDict = dict()   
    #holds url for each broquet's shop page    
    urlDict = dict()
    for row in contents:
        if (contents.line_num == 1):
            #skip over titles
           continue
        x = [row[1]]
        y = [row[2]]
        row[1] = x
        row[2] = y
        brandList.append(row[0:6])
        #create dictionaries of picture and site urls for each broquet
        if(row[6] != ""):
            picUrlDict[row[6]]=row[7]
            urlDict[row[6]]=row[8]
    
    #concatinator
    #creates a list containing each product and its catagory for each
    #brand, outputted finally as outlist
    g = range(len(brandList)-1,-1,-1)
    for i in g:
        if(brandList[i][0] == ''):
            brandList[i-1][1] += brandList[i][1]
            brandList[i-1][2] += brandList[i][2]
    for i in brandList:
       # print i
        if (i[0] != ''):
            outList.append(i)
    #print outList
    open('outputcode.txt', 'w').close()
    
    
    counter = -1
      
   #write the outlist as javascript code
    for i in outList:
        
        #remove empty products for general        
        if "General" in i[1]: i[1].remove("General")
        #deal with apostrophies in the code        
        if("\'" in i[0]):
            idx = i[0].find("\'",0,len(i[0]))            
            i[0] = i[0][:idx] + "\\" + i[0][idx:]

        #lists to hold info
        urlList = list()
        picList = list()
        #change produts to have url to be loaded for img changing
        for j in range(len(i[1])):
            try:            
                picList.append(picUrlDict[(i[1][j])])
                urlList.append(urlDict[(i[1][j])])
            except Exception, e:
                    if(i[2][j] == "General"):
                        continue
                        #picList.append("GenHold")
                        #urlList.append("GenHold")
        counter = counter + 1
        with open("outputcode.txt", "a") as myfile:  
           outArray = "var outArray" + str(counter) + "= new Array("
           outURLArray = "var outURLArray" + str(counter) + "= new Array("
           outPICArray = "var outPICArray" + str(counter) + "= new Array("
           for k in range(len(i[1])):
                if(k != (len(i[1]) - 1)):   
                   outArray += "\'" + i[1][k] + "\',"
                   outURLArray += "\'" + urlList[k] + "\',"
                   outPICArray += "\'" + picList[k] + "\',"
                else:
                    outArray += "\'" + i[1][k] + "\');"
                    outURLArray +=  "\'" + urlList[k] + "\');"
                    outPICArray +=  "\'" + picList[k] + "\');"
           myfile.write("//"+i[0] + "Brand Code:\n")
           myfile.write(outArray + "\n")
           myfile.write(outURLArray + "\n")
           myfile.write(outPICArray + "\n")
           myfile.write("var genBrandVal" + str(counter) + " = new Brand('" + str(counter) + "',"  +\
           "'" + i[0] + "'," \
           + "'" + i[5] + "'," + "'" + i[3] + "',"  + "'" + i[4] + "'," \
           + str(i[2]) + ", outArray" + str(counter) + ", outURLArray" + str(counter)\
           + ", outPICArray" + str(counter) + ");\n\n")
