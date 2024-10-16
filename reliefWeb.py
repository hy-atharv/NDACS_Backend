import time
import requests
import json

APP_NAME = "ndacs"


def getReports(state):
    try:
        API_ENDPOINT = f"""https://api.reliefweb.int/v1/reports?appname={APP_NAME}&query[value]={state}&filter[field]=date.created&filter[value][from]=2024-08-05T00:00:00%2B00:00"""
        response = requests.get(API_ENDPOINT)
        responseStr = response.text
        reportsJson = json.loads(responseStr)
        reports = reportsJson["data"]
        reportsData = []

        for report in reports:
            reportLink = report["href"]

            reportResponse = requests.get(reportLink)
            reportResponseStr = reportResponse.text
            reportResponseData = json.loads(reportResponseStr)

            report_file_url = (
                reportResponseData["data"][0]["fields"]["file"][0]["url"]
                if "file" in reportResponseData["data"][0]["fields"]
                else None
            )

            report_preview_url = (
                reportResponseData["data"][0]["fields"]["file"][0]["preview"]["url"]
                if "file" in reportResponseData["data"][0]["fields"]
                else None
            )

            date_string = reportResponseData["data"][0]["fields"]["date"]["original"]
            date = date_string.split("T")[0]

            reportsData.append(
                {
                    "reportDate": date,
                    "reportTitle": reportResponseData["data"][0]["fields"]["title"],
                    "reportBody": reportResponseData["data"][0]["fields"]["body"],
                    "reportFileUrl": report_file_url,
                    "reportPreviewUrl": report_preview_url,
                    "disasterName": reportResponseData["data"][0]["fields"]["disaster"][0]["name"],
                    "disasterStatusAsPerReportDate": reportResponseData["data"][0]["fields"]["disaster"][0]["status"],
                    "disasterType": [d["name"] for d in reportResponseData["data"][0]["fields"]["disaster"][0]["type"]]
                }
            )

            time.sleep(5)

        print(reportsData)
        return reportsData



    except Exception as e:
        print(e)
        return []

