from supabaseClient import supabase


def insertReports(reportsData):
    for report in reportsData:

        response = (
            supabase.table("ReliefWebReports")
            .insert(report)
            .execute()
        )
        print("Row Inserted")
    print("All Data Inserted")




