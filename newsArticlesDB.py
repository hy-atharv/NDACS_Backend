from supabaseClient import supabase


def insertArticles(articlesData):
    for article in articlesData:

        response = (
            supabase.table("NewsArticles")
            .insert(article)
            .execute()
        )
        print("Row Inserted")
    print("All Data Inserted")



