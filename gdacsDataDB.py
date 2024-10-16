from supabaseClient import supabase
from gdacsData import getGdacsData


def insertGdacsData(gdacsData):
    for data in gdacsData:
        response = (
            supabase.table("GDACSData")
            .insert(data)
            .execute()
        )
        print("Row Inserted")
    print("All Data Inserted")


data = getGdacsData()
insertGdacsData(data)
