import pandas as pd

class customerservices:

    def __init__(self):
        self.serviceType = "return closest camera based on user input and position"
        self.database = pd.read_csv('morerealdata.csv',delimiter=";")
        self.result = pd.DataFrame()

    def getcamIDfromCtype(self, Camlist, type):
        goodTypeCam = []
        for cam in Camlist:
            if(cam.Ctype == type ):
                goodTypeCam.append(cam)
        return(goodTypeCam)

    def findclosestCam(self, goodTypeCam, userPosition):
        # return the closest camera
        closetoyouCam = []
        for cam in goodTypeCam:
            # Call API: api(cam.coordX, cam.coordY, userPosition[0], userPosition[1])
            print("Running API")
        
        #Run example:
        closetoyouCam.append(goodTypeCam[0])
        closetoyouCam.append(goodTypeCam[len(goodTypeCam)-1])
        return(closetoyouCam)
    
    def returnAllcorrespondingData(self, closetoyouCam):
        for cam in closetoyouCam:
            self.result = self.result.append(self.database.loc[self.database['camera'] == cam.databaseID], ignore_index = True)
        return self.result

    def solve_request(self, Camlist, Ctype, userPosition):
        goodTypeCam = self.getcamIDfromCtype(Camlist, Ctype)
        closetoyouCam = self.findclosestCam(goodTypeCam, userPosition)
        return(self.returnAllcorrespondingData(closetoyouCam))




