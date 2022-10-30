def nearest(latval,lonval):
    from math import cos, asin, sqrt, pi

    def distance(lat1, lon1, lat2, lon2):
        p = pi/180
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        return 12742 * asin(sqrt(a))
    import pandas as pd
    df=pd.read_csv("csv/organizations.csv")
    mini=100000000.0
    
    for ind in df.index:
        if distance(float(df["LAT"][ind]),float(df["LON"][ind]),latval,lonval)<mini:
            mini=distance(float(df["LAT"][ind]),float(df["LON"][ind]),latval,lonval)

    details={}
    for ind in df.index:
        if distance(float(df["LAT"][ind]),float(df["LON"][ind]),latval,lonval)==mini:
            details["Name"]=df["NAME"][ind]
            details["ADDRESS"]=df["ADDRESS"][ind]+", "+df["CITY"][ind]+", "+df["ZIP"][ind]
            details["PHONE"]=df["PHONE"][ind]
            details["distance"]=int(mini)
    return details  

