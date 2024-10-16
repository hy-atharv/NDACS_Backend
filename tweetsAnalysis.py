from geminiAPI import genai
import textwrap
import json
from datetime import datetime
import xScraper

# Define the schema for a tweet
tweet = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'tweetLink': genai.protos.Schema(type=genai.protos.Type.STRING),
        'tweetText': genai.protos.Schema(type=genai.protos.Type.STRING),
        'districtsAffected': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.STRING)),
        'disasterType': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.STRING)),
    },
    required=['tweetLink', 'tweetText', 'districtsAffected', 'disasterType']
)

# Define the schema for a list of tweets
tweets = genai.protos.Schema(
    type=genai.protos.Type.ARRAY,
    items=tweet
)

# Define the function declaration for filtering and adding tweets to the database
filtered_tweets_DB = genai.protos.FunctionDeclaration(
    name="filtered_tweets_DB",
    description=textwrap.dedent("""\
        Filters tweets about natural disasters in India and adds relevant information to the database.
    """),
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={
            'tweets': tweets,
        }
    )
)

# Define the function to analyze the tweets
def analyzeTweets(tweet_list):
    # Initialize the Gemini model with the function declaration
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-pro-latest',
        tools=[filtered_tweets_DB]
    )

    # Prepare the prompt for the API call
    prompt = f"""
    Please filter the tweets about natural disasters in India and add the relevant details from this tweet list to the database:
    {tweet_list}
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
    return json.loads(function_call_dict)



def filteredTweets():

    a = xScraper.disasterTweets()
    filteredTweetData = analyzeTweets(a)
    print(filteredTweetData)

    data = filteredTweetData
    print(data)

    tweetsDbData = []

    # Loop through data["args"]["tweets"]
    for tweet in data["args"]["tweets"]:
        # Find the corresponding tweet in list 'a'
        matching_tweet = next((item for item in a if item["tweetLink"] == tweet["tweetLink"]), None)

        # Add the tweet data to tweetsDbData
        if matching_tweet:
            date_string = matching_tweet["tweetDate"]
            date_string = date_string.replace('·', '').strip()
            date_format = "%b %d, %Y %I:%M %p %Z"
            date_object = datetime.strptime(date_string, date_format)
            date = date_object.date()
            date = date.strftime('%Y-%m-%d')
            time = date_object.time()
            time = time.strftime('%H:%M:%S')

            tweetsDbData.append({
                "tweet_link": tweet["tweetLink"],
                "tweet_text": tweet["tweetText"],
                "disaster_type": tweet["disasterType"],
                "districts": tweet["districtsAffected"],
                "tweet_date": date,
                "tweet_time": time,
                "tweet_pictures": matching_tweet["tweetPicturesLinks"],
                "tweet_videos": matching_tweet["tweetVideosLinks"],
                "tweet_user": matching_tweet["tweetUser"]
            })

    print(tweetsDbData)

filteredTweets()