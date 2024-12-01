"""
    По каждому посткоду собирает инфу о компании.
"""

import requests
from load_django import *
from parser_app.models import *

# URL for the POST request
url = "https://accountantmatchmaking.api.intuit.com/v4/graphql"

# Headers
headers = {
    "Accept": "application/json;charset=UTF-8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": "Intuit_APIKey intuit_apikey=prdakyresmylgUdbVpuhf4wHZnk09pUU850acHFg,intuit_apikey_version=1.0",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://proadvisor.intuit.com",
    "Pragma": "no-cache",
    "Referer": "https://proadvisor.intuit.com/",
    "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Linux"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "x-b3-sampled": "1",
    "x-b3-spanid": "bc3a7e638be6ca02",
    "x-b3-traceid": "4c71babd7c33330cba5f120314adf0a0",
}

# Cookies
cookies = {
    "ivid": "9fc1e3d9-0ffd-4b1a-8d62-a2f36187aafa",
    "qbn.sbm_global_sc_channel_timer": "1740229158812",
    "aam_uuid": "77996859184412934840480351106119253248",
    "s_ecid": "MCMID|78146828912480692410497600900778594773",
    "nmstat": "a24b3ad8-b55e-6946-52bb-31950069bb9e",
    "_gcl_au": "1.1.169844877.1732453160",
    "_fbp": "fb.1.1732453159763.330746965824583838",
    "_gid": "GA1.2.64276072.1732453160",
    "_cq_duid": "1.1732453160.3BUUFEaHpyMVEAJ0",
    "ivid_b": "4d806e1e-deee-437e-8147-5a1383362397",
    "s_vi": "[CS]v1|33A191E128C5624F-60000210B0A33485[CE]",
    "ajs_anonymous_id": "9fc1e3d9-0ffd-4b1a-8d62-a2f36187aafa",
    "priorityCode": "3468337910",
    "AKA_A2": "A",
    "ak_bmsc": "FDB57C2DF835E80C90446D8E2D7BA347~000000000000000000000000000000~YAAQo3p7XPcGqF2TAQAAr+hEYhkZatF37oBvyhyA1NuwPMSdrNt22HiM35P0Rw9FrOpkkLGML+pCeUh+2S58rijks0YD25KqgZ0fY6UGoUX+1b+Ub+E/zglNG3OKmsrJ4bR/VJBOtk7pCMZqUdDr2VevRqM2nW0sK/ryyq1FHHCLGY3Pf7oUXLCe/VMf3d4SO6eJoA11aSc/Lfmr9+wCNzwEbIq4W45SZj1yfSRAY7nIdIJ6mWQbrLfF6BJGUiS86TJbfhUFrqOUwllyr/DrU/lxb+H/h8EtESng/vh7v9QIKe2ux48uypuqb/SdE0SQvMZtLwlXJoJtblZSThqQ8IUdFfqwfxN/QzhsjJ7n6/vLCVhzWdjmCeeloK04Oq/TyX3j0otonuoBkjM=",
}

# Payload
payload = {
    "operationName": "getSearchResults_matchmaking",
    "variables": {
        "first": 100,
        "filterBy": "criteria.region='AU' && criteria.distanceWithin='31.068559611866696' && addresses.freeFormAddressLine='{dynamic_filter}'",
        "orderBy": None,
        "after": None,
        "with": "version='V2' && intent='combined-3' && visitorId='084754356641822400' && extVisitorId='[CS]v1|33A191E128C5624F-60000210B0A33485[CE]'",
    },
    "query": """query getSearchResults_matchmaking($first: Int!, $filterBy: String, $with: String, $after: String, $orderBy: String) {
      company {
        searchAccountantListings(first: $first, filterBy: $filterBy, with: $with, after: $after, orderBy: $orderBy) {
          edges {
            node {
              id
              criteria {
                region
                location {
                  latitude
                  longitude
                  __typename
                }
                distanceWithin
                industryServed
                serviceProvided
                productSupported
                __typename
              }
              person {
                givenName
                familyName
                __typename
              }
              imageId
              companyName
              distanceFromSearchLocation
              searchId
              services
              consultationPrice
              professionalDesignations
              summary
              companyName
              customFields {
                value
                __typename
              }
              addresses {
                addressComponents {
                  name
                  value
                  __typename
                }
                __typename
              }
              certifications {
                abbreviation
                __typename
              }
              reviewsInfo {
                id
                reviewStats {
                  numberOfReviews
                  avgOverallRating
                  __typename
                }
                __typename
              }
              __typename
            }
            cursor
            __typename
          }
          totalCount
          pageInfo {
            startCursor
            endCursor
            hasNextPage
            hasPreviousPage
            __typename
          }
          __typename
        }
        __typename
      }
    }""",
}

for location in Location.objects.filter(status="Done"):
    postcode = location.postcode


    dynamic_payload = payload.copy()
    dynamic_payload["variables"] = payload["variables"].copy()
    dynamic_payload["variables"]["filterBy"] = dynamic_payload["variables"]["filterBy"].replace("{dynamic_filter}", postcode)


    # Make the POST request
    response = requests.post(url, headers=headers, cookies=cookies, json=dynamic_payload)


    # Handle the response
    if response.status_code == 200:
        print(f"Request succeeded. Response JSON: postcode {postcode}")


        data = response.json()
        parsed_data = []

        listings = data.get("data", {}).get("company", {}).get("searchAccountantListings", {}).get("edges", [])

        for edge in listings:
            node = edge.get("node", {})

            record = {}

            record["company_id"] = node.get("id")
            record["summary"] = node.get("summary")
            record["image_id"] = node.get("imageId")
            record["consultation_price"] = node.get("consultationPrice")
            record["company_name"] = node.get("companyName")
            record["search_id"] = node.get("searchId")
            record["distance_from_search_location"] = node.get("distanceFromSearchLocation")

            record["addresses"] = [
                component.get("value")
                for address in node.get("addresses", [])
                for component in address.get("addressComponents", [])
            ] or None

            record["distance_within"] = node.get("criteria", {}).get("distanceWithin")
            record["latitude"] = node.get("criteria", {}).get("location", {}).get("latitude")
            record["longitude"] = node.get("criteria", {}).get("location", {}).get("longitude")
            record["region"] = node.get("criteria", {}).get("region")
            record["services"] = node.get("services", [])
            record["certifications"] = [cert.get("abbreviation") for cert in node.get("certifications", [])]
            record["person_name"] = node.get("person", {}).get("givenName")
            record["person_family"] = node.get("person", {}).get("familyName")
            reviews = node.get("reviews_info", {}).get("reviewStats", {})
            record["avg_overall_rating"] = reviews.get("avgOverallRating")
            record["number_of_reviews"] = reviews.get("numberOfReviews")
            record["professional_designations"] = node.get("professionalDesignations", [])


            record = {key: value for key, value in record.items() if value is not None}

            parsed_data.append(record)

            unique_data = {record["search_id"]: record for record in parsed_data}.values()

            for record in unique_data:

                obj, created = Company.objects.update_or_create(
                    search_id=record["search_id"],
                    defaults={
                        "company_id": record.get("company_id"),
                        "summary": record.get("summary"),
                        "image_id": record.get("image_id"),
                        "consultation_price": record.get("consultation_price"),
                        "company_name": record.get("company_name"),
                        "distance_from_search_location": record.get("distance_from_search_location"),
                        "addresses": record.get("addresses"),
                        "person_name": record.get("person_name"),
                        "person_family": record.get("person_family"),
                        "distance_within": record.get("distance_within"),
                        "latitude": record.get("latitude"),
                        "longitude": record.get("longitude"),
                        "region": record.get("region"),
                        "services": record.get("services"),
                        "certifications": record.get("certifications"),
                        "avg_overall_rating": record.get("avg_overall_rating"),
                        "number_of_reviews": record.get("number_of_reviews"),
                        "professional_designations": record.get("professional_designations"),
                        "status": "New"
                    },
                )
                print(f"{'Создана' if created else 'Обновлена'} компания с ID: {record['company_id']}")

    else:
        print(f"Request failed with status code: {response.status_code}")
        exit()
