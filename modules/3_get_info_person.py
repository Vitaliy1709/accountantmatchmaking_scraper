"""
    Проходит по каждому человеку и собирает полную инфу.
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
    "x-b3-spanid": "898ddc09b3533794",
    "x-b3-traceid": "12077250068f27be43ba80ed8d8e2c40",
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
    "analytics_session_id": "1732520959947",
    "REGION": "US",
    "CONSENTMGR": "c1:1|c2:1|c3:1|c4:1|c5:1|c6:1|c7:1|c8:1|c9:1|c10:1|c11:1|c12:1|c13:1|c14:1|c15:1|ts:1732521012926|consent:true",
    "fs_is_sampled": "false",
    "_ga": "GA1.1.1776205919.1732453159",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Mon+Nov+25+2024+09%3A50%3A16+GMT%2B0200+(Eastern+European+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fquickbooks.intuit.com%2Ffind-an-accountant%2F&groups=1%3A1%2C4%3A1",
    "websdk_swiper_flags": "",
    "analytics_session_id.last_access": "1732522304832",
    "_ga_HNWDE5R92K": "GS1.1.1732520505.2.1.1732522318.59.0.0",
}

# Payload
payload = {
    "operationName": "getPublicListings_matchmaking",
    "variables": {
        "pluginInfo": {
            "omitCookies": True,
            "allowRequestPartialSuccess": True
        }
    },
    "query": """query getPublicListings_matchmaking {
        company {
            publicAccountantListings (first: 1, filterBy: "{dynamic_filter}", with: "captchaResponse=''"){
                edges {
                    node {
                        entityVersion
                        id
                        searchId
                        type
                        person {
                            givenName
                            middleName
                            familyName
                            __typename
                        }
                        telephones {
                            telephoneType
                            number
                            extension
                            __typename
                        }
                        addresses {
                            addressComponents {
                                name
                                value
                                __typename
                            }
                            geoLocation {
                                latitude
                                longitude
                                __typename
                            }
                            __typename
                        }
                        summary
                        website
                        companyName
                        industries
                        languages
                        services
                        socialLinks {
                            name
                            url
                            __typename
                        }
                        consultationPrice
                        softwareExpertise
                        professionalDesignations
                        yearsInBusiness
                        numberOfPartners
                        region
                        additionalLanguages
                        imageId
                        certifications {
                            advanced
                            expired
                            name
                            region
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
                __typename
            }
            __typename
        }
    }"""
}


for company in Company.objects.filter(status="New"):
    search_id = company.search_id
    print(f"Обновляем данные для доктора с ID: {search_id}")

    dynamic_payload = payload.copy()
    dynamic_payload["query"] = payload["query"].replace("{dynamic_filter}", f"searchId='{str(search_id)}'")

    response = requests.post(url, headers=headers, cookies=cookies, json=dynamic_payload)

    if response.status_code == 200:
        data = response.json()

        company_info = data.get("data", {}).get("company", {}).get("publicAccountantListings", {}).get("edges", [])

        if not company_info:
            print(f"Нет данных для доктора с ID {search_id}.")
            continue

        for edge in company_info:
            node = edge.get("node", {})

            data_making = {}

            data_making["website"] = node.get("website", "")
            data_making["phone_numbers"] = [phone.get("number", "") for phone in (node.get("telephones") or [])]
            data_making["languages"] = node.get("languages", [])
            data_making["social_links"] = {social.get("name", ""): social.get("url", "") for social in (node.get("socialLinks") or [])}
            data_making["years_in_business"] = node.get("yearsInBusiness", "")
            data_making["search_id"] = node.get("searchId", "")
            data_making["person_name"] = node.get("person", {}).get("givenName", "")
            data_making["person_family"] = node.get("person", {}).get("familyName", "")
            data_making["software_expertise"] = node.get("softwareExpertise", [])
            data_making["industries"] = node.get("industries", [])
            data_making["status"] = "Done"

            Company.objects.update_or_create(
                        search_id=node.get("searchId"),
                        defaults=data_making,
                    )

            print(f"Данные для доктора с ID {search_id} обновлены.")
    else:
        print(f"Нет данных для доктора с ID {search_id}.")
