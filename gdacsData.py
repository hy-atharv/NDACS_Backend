from gdacs.api import GDACSAPIReader, GDACSAPIError


def getGdacsData():
    try:
        client = GDACSAPIReader()

        latest_events = client.latest_events()

        features = latest_events.features

        if features:
            latestEvents = []
            for event in features:
                # Get the list of affected countries
                affected_countries = event['properties'].get('affectedcountries', [])

                # Check if 'India' is in the affected countries
                if any(country['countryname'] == 'India' for country in affected_countries):
                    from_date_string = event['properties'].get('fromdate')
                    from_date = from_date_string.split("T")[0]
                    to_date_string = event['properties'].get('todate')
                    to_date = to_date_string.split("T")[0]

                    # Print relevant details about the event
                    print(f"Event Name: {event['properties'].get('name')}")
                    print(f"Description: {event['properties'].get('description')}")
                    print(f"Coordinates: {event['geometry'].get('coordinates')}")
                    print(f"Icon Image: {event['properties'].get('icon')}")
                    print(f"Alert Level: {event['properties'].get('alertlevel')}")
                    print(f"Alert Score: {event['properties'].get('alertscore')}")
                    print(f"Severity: {event['properties'].get('severitydata', {}).get('severitytext')}")
                    print(f"Date From: {from_date}")
                    print(f"Date To: {to_date}")
                    print(f"Affected Countries: {[c['countryname'] for c in affected_countries]}")
                    print("=" * 50)

                    latestEvents.append({
                        "event_name": event['properties'].get('name'),
                        "event_description": event['properties'].get('description'),
                        "event_coordinates": event['geometry'].get('coordinates'),
                        "event_icon": event['properties'].get('icon'),
                        "event_alert_level": event['properties'].get('alertlevel'),
                        "event_alert_score": event['properties'].get('alertscore'),
                        "event_severity_description": event['properties'].get('severitydata', {}).get('severitytext'),
                        "event_from_date": from_date,
                        "event_to_date": to_date,
                        "event_affected_countries": [c['countryname'] for c in affected_countries]
                    })

            print(latestEvents)
            return latestEvents




    except GDACSAPIError as error:
        print(f"An error occurred: {error}")


