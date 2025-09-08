# yearData = {
#     "Name": "yearTwo",
#     "Period": {
#         "Period": "P1Y",
#         "Offset": "00:00:00",
#         "TimeZone": "CET"
#     },
#     "Type": "Stored",
#     "DirectoryId": 1175335,
#     "Comment": "",
#     "Expression": null,
#     "DirectoryPath": "\\mbencek\\v5_4_43\\",
#     "Unit": null,
#     "Kind": "Quantitative"
# }

# monthData = {
#     "Name": "month",
#     "Period": {
#         "Period": "P1M",
#         "Offset": "00:00:00",
#         "TimeZone": "CET"
#     },
#     "Type": "Stored",
#     "DirectoryId": 1175335,
#     "Comment": "",
#     "Expression": null,
#     "DirectoryPath": "\\mbencek\\v5_4_43\\",
#     "Unit": null,
#     "Kind": "Quantitative"
# }

# quantalData = {
#   "Name": "kvartal",
#   "Period": {
#     "Period": "P3M",
#     "Offset": "00:00:00",
#     "TimeZone": "CET"
#   },
#   "Type": "Stored",
#   "DirectoryId": 1175335,
#   "Comment": "",
#   "Expression": null,
#   "DirectoryPath": "\\mbencek\\v5_4_43\\",
#   "Unit": null,
#   "Kind": "Quantitative"
# }

# weeekData = {
#     "Name": "week",
#     "Period": {
#         "Period": "P1W",
#         "Offset": "00:00:00",
#         "TimeZone": "CET"
#     },
#     "Type": "Stored",
#     "DirectoryId": 1175335,
#     "Comment": "",
#     "Expression": null,
#     "DirectoryPath": "\\mbencek\\v5_4_43\\",
#     "Unit": null,
#     "Kind": "Quantitative"
# }

# monthComputed = {
#     "Id": 3258473,
#     "Name": "computedMonth",
#     "Period": {
#         "Period": "P1M",
#         "Offset": "00:00:00",
#         "TimeZone": "CET"
#     },
#     "Type": "Computed",
#     "DirectoryId": 1348911,
#     "Comment": "",
#     "Expression": "sum(\\one, PQ)",
#     "Kind": "Quantitative",
#     "Policy": "00000000-0000-0000-0000-000000000000",
#     "Created": "0001-01-01T00:00:00+00:00",
#     "LastUpdate": "0001-01-01T00:00:00+00:00"
# }

api_url = "https://timeseries-dev/profile-manager/api/tss/v2/timeseriesmetadata" #Post

xsrf_token = "CfDJ8A7t2EOL0ipDrGiCgGk5RMbPO7CY6Qy-f8sk75pTBA-iELw7lQMeTo76AMQ-Ec5KyK-JqKPHg3PfsMFOWMCGikSUBDyTgkQoIF7peVslaZ4NprggdjAq3i5NPhRkYOwTWWTLpPBm_64bIF4fAvmbGe3JeHUWasdCJgUUTFlA_XGVzGt2HHaRgbvSD3MO8RKibg"

auth_cookies = {
    '.AspNetCore.Antiforgery.9TtSrW0hzOs': 'CfDJ8A7t2EOL0ipDrGiCgGk5RMYWRZP1iIFXMAwYnWF8jO2GjDSige_ayBmrkGNG6B8oR0nYd9VjXsHfyBSbZGrJ3LiIM3Z72W95WQpQo1woewDJJo6Llp4PXMhqP-X2xk6-HkqBuas8gaIYVbKf1wkkVcM',
    'XSRF-TOKEN': 'CfDJ8A7t2EOL0ipDrGiCgGk5RMbPO7CY6Qy-f8sk75pTBA-iELw7lQMeTo76AMQ-Ec5KyK-JqKPHg3PfsMFOWMCGikSUBDyTgkQoIF7peVslaZ4NprggdjAq3i5NPhRkYOwTWWTLpPBm_64bIF4fAvmbGe3JeHUWasdCJgUUTFlA_XGVzGt2HHaRgbvSD3MO8RKibg',
    'dateRange': '%7B%22from%22%3A1757282400000%2C%22to%22%3A1757368800000%7D',
    'MSHDO.Auth.TTL': '1757358726-1757359026',
    'MSHDO.Auth': 'CfDJ8A7t2EOL0ipDrGiCgGk5RMbpMlghgj31VciRyMO-0Y3Lz7fHkhKMuBLQYdC6IEaLWrd-VxMkyZzzqEAoR03zs6POlsyac1KclTuQcR-awS-1g29LPNeshcdWS4fjIAoxyQcYFiUOLx-WUvuk31fa2MlHFrAMjM9wmOJdCKNnVR47wg_yb_yMnqP3bTuRAR4xsY8PlOkrFLV4A-jZKVWKTC7qjNvDsvDngbFA7cRVNaOD5M-8S1mogJigtUJwrc4LL6DzYhihYD3rxcpmXsj7COZnyLrlPpOxzmwKMS1ul6aIZeCvp85z48A_o9zbxBIcqA',
    'MSHDO.Auth.Browser': 'faea7ff6335541bda1812cc0cdc8ae9e',
    'mshdo.NETCore.culture': 'en'
}

import requests
import json

def creteProfileComputed():
    periods = ["P1Y", "P1M", "P3M", "P6M", "P1W", "PT1H", "PT15M", "PT5M", "PT1M", "PT10M", "PT3M", "PT1S", "P1D"]
    for period in periods:
        kinds = ["Quantitative", "Continuous"]
        for kind in kinds:
            data = {
                "Name": f"computed_{period}_{kind}",
                "Period": {
                    "Period": period,
                    "Offset": "00:00:00",
                    "TimeZone": "CET"
                },
                "Type": "Computed",
                "DirectoryId": 1349193,
                "Comment": "",
                "Expression": f"sum(\\one, {kind[0:2]})",
                "Kind": kind,
                "Policy": "00000000-0000-0000-0000-000000000000"
            }
            
            # Complete headers matching the working frontend request
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
                'Origin': 'https://timeseries-dev',
                'Referer': 'https://timeseries-dev/profile-manager/dockboard',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'mshdo-language': 'en',
                'x-xsrf-token': xsrf_token
            }
            
            response = requests.post(
                api_url, 
                headers=headers, 
                cookies=auth_cookies,
                data=json.dumps(data), 
                verify=False
            )
            print(f"Status: {response.status_code} for {period}_{kind}")
            if response.status_code != 200:
                print(f"Error response: {response.text}")
            else:
                print("Success!")

if __name__ == "__main__":
    creteProfileComputed()