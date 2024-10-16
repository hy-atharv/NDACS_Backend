from geminiAPI import genai
import textwrap
import json
import newsScraper
from newsScraper import disasterNews

# Define the schema for an article
article = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'articleTitle': genai.protos.Schema(type=genai.protos.Type.STRING),
        'articleUrl': genai.protos.Schema(type=genai.protos.Type.STRING),
        'districtsAffected': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.STRING)),
        'disasterType': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.STRING)),
    },
    required=['articleTitle', 'articleUrl', 'districtsAffected', 'disasterType']
)

# Define the schema for a list of articles
articles = genai.protos.Schema(
    type=genai.protos.Type.ARRAY,
    items=article
)

# Define the function declaration for filtering and adding articles to the database
filtered_articles_DB = genai.protos.FunctionDeclaration(
    name="filtered_articles_DB",
    description=textwrap.dedent("""\
        Filters articles about natural disasters in India and adds relevant information to the database.
    """),
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={
            'articles': articles,
        }
    )
)


# Define the function to analyze the articles
def analyzeArticles(article_list):
    # Initialize the Gemini model with the function declaration
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-pro-latest',
        tools=[filtered_articles_DB]
    )

    # Prepare the prompt for the API call
    prompt = f"""
    Please filter the articles about natural disasters in India and add the relevant details from this article list to the database:
    {article_list}
    """

    # Call the API
    result = model.generate_content(
        f"""{prompt}""",
        tool_config={'function_calling_config': 'Auto'}
    )

    # Extract and process the result
    fc = result.candidates[0].content.parts[0].function_call
    function_call_dict = json.dumps(type(fc).to_dict(fc), indent=4)

    # Return the processed function call result
    print(function_call_dict)
    print(json.loads(function_call_dict))
    return json.loads(function_call_dict)



def filteredArticles():
    a = disasterNews()

    filteredArticleData = analyzeArticles(a)

    data = filteredArticleData

    print(data)

    articlesDbData = []

    # Loop through data["args"]["articles"]
    for article in data["args"]["articles"]:
        # Find the corresponding article in list 'a'
        matching_article = next((item for item in a if item["articleSourceURL"] == article["articleUrl"]), None)

        # Add the article data to articlesDbData
        if matching_article:
            articlesDbData.append({
                "article_url": article["articleUrl"],
                "article_title": article["articleTitle"],
                "disaster_type": article["disasterType"],
                "districts": article["districtsAffected"],
                "article_date": matching_article["articleDate"],
                "article_time": matching_article["articleTime"],
                "article_content": matching_article["articleText"],
                "article_image": matching_article["articleTopImage"]
            })
    print("\n\n\n")
    print(articlesDbData)


filteredArticles()