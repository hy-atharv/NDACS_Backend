from geminiAPI import genai
import textwrap
import json
import reliefWeb

# Define the schema for an article
report = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'disasterSummary': genai.protos.Schema(type=genai.protos.Type.STRING),
        'reportTitle': genai.protos.Schema(type=genai.protos.Type.STRING),
        'districtsAffected': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.STRING)),
        'totalLivesLost': genai.protos.Schema(type=genai.protos.Type.NUMBER),
        'reliefDescription': genai.protos.Schema(type=genai.protos.Type.STRING),
        'totalHousesDamaged': genai.protos.Schema(type=genai.protos.Type.NUMBER),
        'numberOfPersonMissing': genai.protos.Schema(type=genai.protos.Type.NUMBER),
        'alertStatus': genai.protos.Schema(type=genai.protos.Type.STRING)
    },
    required=['disasterSummary', 'reportTitle', 'districtsAffected', 'totalLivesLost', 'reliefDescription', 'totalHousesDamaged', 'numberOfPersonMissing', 'alertStatus' ]
)

# Define the schema for a list of articles
reports = genai.protos.Schema(
    type=genai.protos.Type.ARRAY,
    items=report
)

# Define the function declaration for filtering and adding articles to the database
analyzed_reports = genai.protos.FunctionDeclaration(
    name="analyzed_reports",
    description=textwrap.dedent("""\
        Analyzes reports about natural disasters in India and adds relevant information to the database.
    """),
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={
            'reports': reports,
        }
    )
)


# Define the function to analyze the articles
def analyzeReports(report_list):
    # Initialize the Gemini model with the function declaration
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-pro-latest',
        tools=[analyzed_reports]
    )

    # Prepare the prompt for the API call
    prompt = f"""
    Please analyze the reports about natural disasters in India and add the relevant details and an "alertStatus" from (High, Medium, Neutralized), from this report list to the database:
    {report_list}
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


def analyzedReportData():
    a = reliefWeb.getReports("Himachal Pradesh")

    data = analyzeReports(a)

    print(data)

    reportsDbData = []

    # Loop through data["args"]["articles"]
    for report in data["args"]["reports"]:
        # Find the corresponding article in list 'a'
        matching_report = next((item for item in a if item["reportTitle"] == report["reportTitle"]), None)

        # Add the article data to articlesDbData
        if matching_report:
            reportsDbData.append({
                "report_title": report["reportTitle"],
                "disaster_summary": report["disasterSummary"],
                "districts": report["districtsAffected"],
                "lives_lost": report["totalLivesLost"],
                "person_missing": report["numberOfPersonMissing"],
                "houses_damaged": report["totalHousesDamaged"],
                "relief_description": report["reliefDescription"],
                "alert_Status": report["alertStatus"],
                "report_date": matching_report["reportDate"],
                "report_content": matching_report["reportBody"],
                "report_file": matching_report["reportFileUrl"],
                "report_preview_image": matching_report["reportPreviewUrl"],
                "disaster_type": matching_report["disasterType"]
            })
    print("\n\n\n\n\n\n")
    print(reportsDbData)

analyzedReportData()