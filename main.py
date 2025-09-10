import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import datetime
import calendar
import requests
import json
import warnings
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

api_url = "https://timeseries-dev/profile-manager/api/tss/v2/timeseriesmetadata" #Post

xsrf_token = "CfDJ8A7t2EOL0ipDrGiCgGk5RMb-9FQYIb3mJBhuiWdLw9oAeOuDdchx9JaS8tgwMA96g5fpuZIXQecFaH5DPhGDYrv1gRCnY3tjJWvGMVJ9pEizlXsCesJsNuaejfYJ9ebiUUGUE2maxTj8_hvEBZO-VZwEnKaNzgNAYUmyGDwudKAQgkVA1GiOT8z83uIPTLHp8Q"

auth_cookies = {
    '.AspNetCore.Antiforgery.9TtSrW0hzOs': 'CfDJ8A7t2EOL0ipDrGiCgGk5RMYWRZP1iIFXMAwYnWF8jO2GjDSige_ayBmrkGNG6B8oR0nYd9VjXsHfyBSbZGrJ3LiIM3Z72W95WQpQo1woewDJJo6Llp4PXMhqP-X2xk6-HkqBuas8gaIYVbKf1wkkVcM',
    'dateRange': '%7B%22from%22%3A1757368800000%2C%22to%22%3A1757455200000%7D',
    'MSHDO.Auth': 'CfDJ8A7t2EOL0ipDrGiCgGk5RMbvsFgAOds9R3mbJ4bqeGXxioOxi4HupOr-ZXtrU8JBMjoDYhjqDu9Put5LyGY_WzJQj8X87wrF4ru-VmK0VRS5XZaKi_FYoA8GFJX6wQrrm_R9j0OGMwy4duNuPXAmgMPvVKC3fexx43QXE2rsJRErL-G5RNYHJ996NKnappzpdWos5tFAZK9-GU-pWwSKSFl1MH-mmSZVmwOgkvGnlbi8og4okHFnvWOI_aPkEW4f0CRBgK4D6RcE8cYKlBAtnwL9MHH-FCmnRhiyM9KXpnr3fGGoMvSK5OQeP6OEuv0UGA',
    'MSHDO.Auth.TTL': '1757436755-1757437055',
    'XSRF-TOKEN': 'CfDJ8A7t2EOL0ipDrGiCgGk5RMb-9FQYIb3mJBhuiWdLw9oAeOuDdchx9JaS8tgwMA96g5fpuZIXQecFaH5DPhGDYrv1gRCnY3tjJWvGMVJ9pEizlXsCesJsNuaejfYJ9ebiUUGUE2maxTj8_hvEBZO-VZwEnKaNzgNAYUmyGDwudKAQgkVA1GiOT8z83uIPTLHp8Q',
    'MSHDO.Auth.Browser': 'faea7ff6335541bda1812cc0cdc8ae9e',
    'mshdo.NETCore.culture': 'en'
}

def parse_cookie_string(cookie_string):
    """Parse a cookie string and return a dictionary of cookie key-value pairs."""
    cookies = {}
    for cookie in cookie_string.split('; '):
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookies[key] = value
    return cookies

def update_auth_cookies(cookie_string):
    """Update the global auth_cookies with values from the provided cookie string."""
    global auth_cookies
    new_cookies = parse_cookie_string(cookie_string)
    auth_cookies.update(new_cookies)

def update_xsrf_token(token):
    """Update the global xsrf_token with the provided token."""
    global xsrf_token
    xsrf_token = token

def creteProfileComputed():
    t = input("Enter token: ")
    update_xsrf_token(t)
    cookie = input("Enter cookies: ")
    update_auth_cookies(cookie)

    # Data structures to store results
    results = {
        'creation_errors': [],  # Profiles that failed to create
        'validation_passed': [],  # Profiles that passed validation
        'validation_failed': [],  # Profiles that failed validation
        'data_retrieval_errors': [],  # Profiles that failed data retrieval
        'supported_periods': {},  # Periods that work with their profiles
        'period_summary': {}  # Summary count per period
    }
    
    periods = ["P1Y", "P1M", "P3M", "P6M", "P1W", "PT1H", "PT15M", "PT5M", "PT1M", "PT10M", "PT3M", "PT1S", "P1D"]
    for period in periods:
        kinds = ["Quantitative", "Continuous"]
        for kind in kinds:
            profilePeriods = ["H", "PD", "PW", "PE", "PM", "PQ", "PY"]
            for pP in profilePeriods:
                functions = ["sum", "avg", "min", "max"]
                for func in functions:
                    data = {
                        "Name": f"computed_{period}_{kind}_{pP}_{func}",
                        "Period": {
                            "Period": period,
                            "Offset": "00:00:00",
                            "TimeZone": "CET"
                        },
                        "Type": "Computed",
                        "DirectoryId": 1351527,
                        "Comment": "",
                        "Expression": f"{func}(\\one, {pP})",
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
                        results['creation_errors'].append({
                            'profile_name': f"computed_{period}_{kind}_{pP}_{func}",
                            'period': period,
                            'kind': kind,
                            'function': func,
                            'function_period': pP,
                            'status_code': response.status_code,
                            'error': response.text
                        })
                    else:
                        profile_id = response.json().get("Id")
                        print(f"Created profile ID: {profile_id}")
                        
                        # Get profile data
                        get_profile_data(profile_id, f"computed_{period}_{kind}_{pP}_{func}", results, period, {
                            "Period": period,
                            "Kind": kind,
                            "Function": func,
                            "FunctionPeriod": pP
                        })

    # Return results for further analysis
    return results

def generateDatesForPeriod():
    """Generate Unix timestamps for the first day of each month in 2023 and 2024 (leap year)."""
    datesUnix = []
    isLeap = []
    endDate = []
    months = []
    years = []
    
    # Generate dates for 2023 (non-leap year)
    for month in range(1, 13):
        data = f"1.{month}.2023 00:00:00"
        start_timestamp = int(datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S").timestamp())
        
        
        end_data = f"3.{month}.2023 00:00:00"
        end_timestamp = int(datetime.datetime.strptime(end_data, "%d.%m.%Y %H:%M:%S").timestamp())
        
        datesUnix.append(start_timestamp)
        endDate.append(end_timestamp)
        isLeap.append(False)
        months.append(month)
        years.append(2023)
    
    # Generate dates for 2024 (leap year)
    for month in range(1, 13):
        data = f"1.{month}.2024 00:00:00"
        start_timestamp = int(datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S").timestamp())
        
        
        end_data = f"3.{month}.2024 00:00:00"
        end_timestamp = int(datetime.datetime.strptime(end_data, "%d.%m.%Y %H:%M:%S").timestamp())
        
        datesUnix.append(start_timestamp)
        endDate.append(end_timestamp)
        isLeap.append(True)
        months.append(month)
        years.append(2024)
    
    return datesUnix, isLeap, endDate, months, years


def get_expected_value_for_month(function, function_period, month, year, is_leap_year):
    """Calculate expected value for a specific month and year based on function and function period."""
    
    # Get number of days in the month
    days_in_month = calendar.monthrange(year, month)[1]
    
    if function == "sum":
        if function_period == "H":  # Sum over hour
            return 1  # Each hour contains value 1
        elif function_period == "PD":  # Sum over day  
            return 24  # 24 hours per day
        elif function_period == "PW":  # Sum over week
            return 168  # 7 days * 24 hours = 168 hours
        elif function_period == "PE":  # Sum over epoch (same as week)
            return 168
        elif function_period == "PM":  # Sum over month
            return days_in_month * 24  # Actual days in month * 24 hours
        elif function_period == "PQ":  # Sum over quarter
            # For quarters, we need to consider which quarter this month belongs to
            quarter_months = {
                1: [1, 2, 3], 2: [4, 5, 6], 3: [7, 8, 9], 4: [10, 11, 12]
            }
            quarter = 1
            for q, months in quarter_months.items():
                if month in months:
                    quarter = q
                    break
            
            # Calculate total days in the quarter
            total_days = 0
            for q_month in quarter_months[quarter]:
                total_days += calendar.monthrange(year, q_month)[1]
            
            return total_days * 24  # Total days in quarter * 24 hours
        elif function_period == "PY":  # Sum over year
            if is_leap_year:
                return 366 * 24  # 366 days * 24 hours for leap year
            else:
                return 365 * 24  # 365 days * 24 hours for normal year
    
    elif function in ["avg", "min", "max"]:
        return 1  # Average, min, max should be 1 since source data is constant 1
    
    return None


def get_profile_data(profile_id, profile_name, results, period, profile_data):
    """Fetch data from a created profile and store results in the results dictionary."""
    dates, isLeapYear, endDate, months, years = generateDatesForPeriod()
    
    passed_months = []  # Store details of months that passed
    
    for dStart, leap, dEnd, month, year in zip(dates, isLeapYear, endDate, months, years):
        url_get_profile_data = f"https://timeseries-dev/profile-manager/api/tss/TimeSeriesData/?id={profile_id}&unixDateFrom={dStart}&unixDateTo={dEnd}&includeNulls=true"
        
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Referer': 'https://timeseries-dev/profile-manager/dockboard',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Gpc': '1',
            'mshdo-language': 'en',
            'priority': 'u=1, i'
        }
        
        try:
            response = requests.get(
                url_get_profile_data,
                headers=headers,
                cookies=auth_cookies,
                verify=False
            )

            if response.status_code == 200:
                data = response.json()
                
                if not data:
                    print(f"No data returned for profile {profile_id} for {year}-{month:02d}")
                    continue
                
                first_value = data[0].get("Value")
                
                # Calculate expected value based on the specific month and year
                expected_value = get_expected_value_for_month(
                    profile_data["Function"], 
                    profile_data["FunctionPeriod"], 
                    month, 
                    year, 
                    leap
                )
                
                validation_passed = False
                
                # Check validation with tolerance for floating point values
                if expected_value is not None:
                    if first_value == expected_value or abs(first_value - expected_value) < 1.05:
                        validation_passed = True
                    
                    profile_result = {
                        'profile_name': profile_name,
                        'profile_id': profile_id,
                        'period': profile_data["Period"],
                        'kind': profile_data["Kind"],
                        'function': profile_data["Function"],
                        'function_period': profile_data["FunctionPeriod"],
                        'actual_value': first_value,
                        'expected_value': expected_value,
                        'validation_passed': validation_passed,
                        'test_month': month,
                        'test_year': year,
                        'is_leap_year': leap,
                        'days_in_month': calendar.monthrange(year, month)[1]
                    }
                    
                    if validation_passed:
                        # Store this month's successful result
                        passed_months.append(profile_result)
                    else:
                        results['validation_failed'].append(profile_result)
                        print(f"Validation failed for {profile_name} - {year}-{month:02d}: expected {expected_value}, got {first_value}")
                        # If any month fails, we consider the whole profile failed
                        return
                else:
                    results['validation_failed'].append({
                        'profile_name': profile_name,
                        'profile_id': profile_id,
                        'period': profile_data["Period"],
                        'kind': profile_data["Kind"],
                        'function': profile_data["Function"],
                        'function_period': profile_data["FunctionPeriod"],
                        'actual_value': first_value,
                        'expected_value': 'Unknown',
                        'validation_passed': False,
                        'error': 'Unknown validation case',
                        'test_month': month,
                        'test_year': year,
                        'is_leap_year': leap
                    })
                    return
                    
            else:
                results['data_retrieval_errors'].append({
                    'profile_name': profile_name,
                    'profile_id': profile_id,
                    'status_code': response.status_code,
                    'error': response.text,
                    'test_month': month,
                    'test_year': year
                })
                print(f"Failed to get data for profile {profile_id} for {year}-{month:02d}. Status: {response.status_code}")
                return
                
        except Exception as e:
            results['data_retrieval_errors'].append({
                'profile_name': profile_name,
                'profile_id': profile_id,
                'error': str(e),
                'test_month': month,
                'test_year': year
            })
            print(f"Exception while getting data for profile {profile_id} for {year}-{month:02d}: {str(e)}")
            return
    
    # If we reach here, all months passed validation
    # Add all individual month results to validation_passed
    for month_result in passed_months:
        results['validation_passed'].append(month_result)
    
    # Also create a summary result with sample values from the first month
    if passed_months:
        first_month = passed_months[0]
        summary_result = {
            'profile_name': f"{profile_name}_SUMMARY",
            'profile_id': profile_id,
            'period': profile_data["Period"],
            'kind': profile_data["Kind"],
            'function': profile_data["Function"],
            'function_period': profile_data["FunctionPeriod"],
            'actual_value': first_month['actual_value'],
            'expected_value': first_month['expected_value'],
            'validation_passed': True,
            'months_tested': len(dates),
            'all_months_passed': True,
            'test_month': 'ALL',
            'test_year': 'ALL',
            'is_leap_year': 'BOTH',
            'days_in_month': 'VARIES'
        }
        
        results['validation_passed'].append(summary_result)
        
        # Add to supported periods using the summary
        if period not in results['supported_periods']:
            results['supported_periods'][period] = []
        results['supported_periods'][period].append(summary_result)
    
    print(f"Profile {profile_name} passed validation for all {len(dates)} months!")

def get_working_profiles_for_period(results, period):
    """Get all working profiles for a specific period."""
    return results['supported_periods'].get(period, [])

def get_profiles_by_function(results, function_name):
    """Get all working profiles that use a specific function (sum, avg, min, max)."""
    matching_profiles = []
    for profiles in results['supported_periods'].values():
        for profile in profiles:
            if profile['function'] == function_name:
                matching_profiles.append(profile)
    return matching_profiles

def get_profiles_by_kind(results, kind):
    """Get all working profiles of a specific kind (Quantitative, Continuous)."""
    matching_profiles = []
    for profiles in results['supported_periods'].values():
        for profile in profiles:
            if profile['kind'] == kind:
                matching_profiles.append(profile)
    return matching_profiles

def get_summary_stats(results):
    """Get summary statistics about the results."""
    total_attempted = (len(results['creation_errors']) + 
                      len(results['validation_passed']) + 
                      len(results['validation_failed']) + 
                      len(results['data_retrieval_errors']))
    
    return {
        'total_attempted': total_attempted,
        'successful_creations': len(results['validation_passed']) + len(results['validation_failed']),
        'validation_passed': len(results['validation_passed']),
        'validation_failed': len(results['validation_failed']),
        'creation_failed': len(results['creation_errors']),
        'data_retrieval_failed': len(results['data_retrieval_errors']),
        'working_periods': len(results['supported_periods']),
        'success_rate': len(results['validation_passed']) / total_attempted * 100 if total_attempted > 0 else 0
    }

def export_results_to_csv(results, filename="profile_results.csv"):
    """Export results to CSV file for further analysis."""
    import csv
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['profile_name', 'profile_id', 'period', 'kind', 'function', 'function_period', 
                     'actual_value', 'expected_value', 'validation_passed', 'status', 'error', 
                     'test_month', 'test_year', 'is_leap_year', 'days_in_month', 'months_tested', 'all_months_passed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        # Write validation passed profiles
        for profile in results['validation_passed']:
            row = {}
            # Only include fields that are in fieldnames
            for field in fieldnames:
                if field in profile:
                    row[field] = profile[field]
                else:
                    row[field] = ''
            row['status'] = 'validation_passed'
            if 'error' not in row or row['error'] == '':
                row['error'] = ''
            writer.writerow(row)
        
        # Write validation failed profiles
        for profile in results['validation_failed']:
            row = {}
            # Only include fields that are in fieldnames
            for field in fieldnames:
                if field in profile:
                    row[field] = profile[field]
                else:
                    row[field] = ''
            row['status'] = 'validation_failed'
            if 'error' not in row or row['error'] == '':
                row['error'] = profile.get('error', '')
            writer.writerow(row)
        
        # Write creation errors
        for error in results['creation_errors']:
            writer.writerow({
                'profile_name': error['profile_name'],
                'profile_id': '',
                'period': error['period'],
                'kind': error['kind'],
                'function': error['function'],
                'function_period': error['function_period'],
                'actual_value': '',
                'expected_value': '',
                'validation_passed': False,
                'status': 'creation_failed',
                'error': f"Status {error['status_code']}: {error['error']}",
                'test_month': '',
                'test_year': '',
                'is_leap_year': '',
                'days_in_month': '',
                'months_tested': '',
                'all_months_passed': ''
            })
        
        # Write data retrieval errors
        for error in results['data_retrieval_errors']:
            writer.writerow({
                'profile_name': error['profile_name'],
                'profile_id': error.get('profile_id', ''),
                'period': '',
                'kind': '',
                'function': '',
                'function_period': '',
                'actual_value': '',
                'expected_value': '',
                'validation_passed': False,
                'status': 'data_retrieval_failed',
                'error': error['error'],
                'test_month': error.get('test_month', ''),
                'test_year': error.get('test_year', ''),
                'is_leap_year': '',
                'days_in_month': '',
                'months_tested': '',
                'all_months_passed': ''
            })
    
    print(f"Results exported to {filename}")

def create_sankey_diagram(results):
    """Create a Sankey diagram showing the flow from periods to validation results."""
    
    # Prepare data for Sankey diagram
    labels = []
    source = []
    target = []
    value = []
    colors = []
    
    # Add period labels
    periods = list(results['supported_periods'].keys())
    for period in periods:
        labels.append(f"Period: {period}")
    
    # Add result type labels
    result_types = ["Validation Passed", "Validation Failed", "Creation Failed", "Data Retrieval Failed"]
    for result_type in result_types:
        labels.append(result_type)
    
    # Create flows from periods to validation passed
    period_start_idx = 0
    result_start_idx = len(periods)
    
    for i, period in enumerate(periods):
        period_profiles = results['supported_periods'][period]
        if period_profiles:
            source.append(period_start_idx + i)
            target.append(result_start_idx + 0)  # Validation Passed
            value.append(len(period_profiles))
    
    # Add flows for failed validations, creation errors, etc.
    period_failures = {}
    for profile in results['validation_failed']:
        period = profile['period']
        if period not in period_failures:
            period_failures[period] = 0
        period_failures[period] += 1
    
    for period, count in period_failures.items():
        if period in periods:
            period_idx = periods.index(period)
            source.append(period_start_idx + period_idx)
            target.append(result_start_idx + 1)  # Validation Failed
            value.append(count)
    
    # Add creation errors by period
    creation_failures = {}
    for error in results['creation_errors']:
        period = error['period']
        if period not in creation_failures:
            creation_failures[period] = 0
        creation_failures[period] += 1
    
    for period, count in creation_failures.items():
        if period in periods:
            period_idx = periods.index(period)
        else:
            # Add new period label if not in successful periods
            labels.insert(result_start_idx, f"Period: {period}")
            periods.append(period)
            period_idx = len(periods) - 1
            result_start_idx += 1
            # Update target indices
            for j in range(len(target)):
                if target[j] >= result_start_idx - 1:
                    target[j] += 1
        
        source.append(period_idx)
        target.append(result_start_idx + 2)  # Creation Failed
        value.append(count)
    
    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=["lightblue"] * len(periods) + ["green", "orange", "red", "purple"]
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=["rgba(0,255,0,0.3)" if target[i] == result_start_idx else 
                   "rgba(255,165,0,0.3)" if target[i] == result_start_idx + 1 else
                   "rgba(255,0,0,0.3)" for i in range(len(source))]
        )
    )])
    
    fig.update_layout(
        title_text="Profile Creation Flow: Periods → Results",
        font_size=12,
        height=600
    )
    
    return fig

def create_success_rate_chart(results):
    """Create a bar chart showing success rates by period."""
    
    periods = []
    success_rates = []
    total_attempts = []
    successful_counts = []
    
    # Calculate success rates for each period
    all_periods = set()
    
    # Get all periods from successful results
    for period in results['supported_periods'].keys():
        all_periods.add(period)
    
    # Get all periods from failed results
    for profile in results['validation_failed']:
        all_periods.add(profile['period'])
    
    for error in results['creation_errors']:
        all_periods.add(error['period'])
    
    for period in sorted(all_periods):
        successful = len(results['supported_periods'].get(period, []))
        failed_validation = sum(1 for p in results['validation_failed'] if p['period'] == period)
        failed_creation = sum(1 for e in results['creation_errors'] if e['period'] == period)
        failed_data = sum(1 for e in results['data_retrieval_errors'] if e.get('period') == period)
        
        total = successful + failed_validation + failed_creation + failed_data
        
        if total > 0:
            periods.append(period)
            success_rates.append((successful / total) * 100)
            total_attempts.append(total)
            successful_counts.append(successful)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=periods,
        y=success_rates,
        text=[f"{successful_counts[i]}/{total_attempts[i]}" for i in range(len(periods))],
        textposition='auto',
        name='Success Rate (%)',
        marker_color='lightgreen'
    ))
    
    fig.update_layout(
        title='Profile Creation Success Rate by Period',
        xaxis_title='Period',
        yaxis_title='Success Rate (%)',
        yaxis=dict(range=[0, 100]),
        height=500
    )
    
    return fig

def create_function_comparison_chart(results):
    """Create a stacked bar chart comparing function performance."""
    
    functions = ['sum', 'avg', 'min', 'max']
    periods = list(results['supported_periods'].keys())
    
    # Create data for each function
    data = {func: [] for func in functions}
    
    for period in periods:
        period_profiles = results['supported_periods'][period]
        function_counts = {func: 0 for func in functions}
        
        for profile in period_profiles:
            func = profile['function']
            if func in function_counts:
                function_counts[func] += 1
        
        for func in functions:
            data[func].append(function_counts[func])
    
    fig = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    for i, func in enumerate(functions):
        fig.add_trace(go.Bar(
            name=func,
            x=periods,
            y=data[func],
            marker_color=colors[i]
        ))
    
    fig.update_layout(
        title='Working Profiles by Function and Period',
        xaxis_title='Period',
        yaxis_title='Number of Working Profiles',
        barmode='stack',
        height=500
    )
    
    return fig

def create_kind_comparison_chart(results):
    """Create a pie chart comparing Quantitative vs Continuous profile success."""
    
    kind_counts = {'Quantitative': 0, 'Continuous': 0}
    
    for profiles in results['supported_periods'].values():
        for profile in profiles:
            kind = profile['kind']
            if kind in kind_counts:
                kind_counts[kind] += 1
    
    fig = go.Figure(data=[go.Pie(
        labels=list(kind_counts.keys()),
        values=list(kind_counts.values()),
        hole=0.3,
        marker_colors=['#FF9999', '#66B2FF']
    )])
    
    fig.update_layout(
        title='Distribution of Working Profiles by Kind',
        height=400
    )
    
    return fig

def create_comprehensive_dashboard(results):
    """Create a comprehensive dashboard with multiple visualizations."""
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Success Rate by Period', 'Function Distribution', 
                       'Kind Distribution', 'Validation Results'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "pie"}, {"type": "bar"}]]
    )
    
    # 1. Success Rate by Period
    periods = []
    success_rates = []
    
    all_periods = set()
    for period in results['supported_periods'].keys():
        all_periods.add(period)
    for profile in results['validation_failed']:
        all_periods.add(profile['period'])
    for error in results['creation_errors']:
        all_periods.add(error['period'])
    
    for period in sorted(all_periods):
        successful = len(results['supported_periods'].get(period, []))
        failed_validation = sum(1 for p in results['validation_failed'] if p['period'] == period)
        failed_creation = sum(1 for e in results['creation_errors'] if e['period'] == period)
        
        total = successful + failed_validation + failed_creation
        if total > 0:
            periods.append(period)
            success_rates.append((successful / total) * 100)
    
    fig.add_trace(
        go.Bar(x=periods, y=success_rates, name='Success Rate', marker_color='lightgreen'),
        row=1, col=1
    )
    
    # 2. Function Distribution
    function_counts = {'sum': 0, 'avg': 0, 'min': 0, 'max': 0}
    for profiles in results['supported_periods'].values():
        for profile in profiles:
            func = profile['function']
            if func in function_counts:
                function_counts[func] += 1
    
    fig.add_trace(
        go.Bar(x=list(function_counts.keys()), y=list(function_counts.values()), 
               name='Functions', marker_color='lightblue'),
        row=1, col=2
    )
    
    # 3. Kind Distribution
    kind_counts = {'Quantitative': 0, 'Continuous': 0}
    for profiles in results['supported_periods'].values():
        for profile in profiles:
            kind = profile['kind']
            if kind in kind_counts:
                kind_counts[kind] += 1
    
    fig.add_trace(
        go.Pie(labels=list(kind_counts.keys()), values=list(kind_counts.values()),
               name="Kind Distribution"),
        row=2, col=1
    )
    
    # 4. Validation Results Summary
    result_counts = {
        'Validation Passed': len(results['validation_passed']),
        'Validation Failed': len(results['validation_failed']),
        'Creation Failed': len(results['creation_errors']),
        'Data Retrieval Failed': len(results['data_retrieval_errors'])
    }
    
    colors = ['green', 'orange', 'red', 'purple']
    fig.add_trace(
        go.Bar(x=list(result_counts.keys()), y=list(result_counts.values()),
               name='Results', marker_color=colors),
        row=2, col=2
    )
    
    fig.update_layout(
        title_text="Profile Creation Results Dashboard",
        height=800,
        showlegend=False
    )
    
    return fig

def create_failed_profiles_detail_chart(results):
    """Create a detailed chart showing failed profiles with their information."""
    
    # Combine all failed profiles
    all_failures = []
    
    # Add validation failures
    for profile in results['validation_failed']:
        month_info = ""
        if profile.get('test_month') and profile.get('test_year'):
            leap_info = " (Leap)" if profile.get('is_leap_year') else ""
            days_info = f" ({profile.get('days_in_month', 'N/A')}d)" if profile.get('days_in_month') else ""
            month_info = f" [{profile['test_year']}-{profile['test_month']:02d}{leap_info}{days_info}]"
        
        all_failures.append({
            'profile_name': profile['profile_name'] + month_info,
            'period': profile['period'],
            'kind': profile['kind'],
            'function': profile['function'],
            'function_period': profile['function_period'],
            'failure_type': 'Validation Failed',
            'expected_value': profile.get('expected_value', 'N/A'),
            'actual_value': profile.get('actual_value', 'N/A'),
            'error': f"Expected: {profile.get('expected_value', 'N/A')}, Got: {profile.get('actual_value', 'N/A')}{month_info}"
        })
    
    # Add creation failures
    for error in results['creation_errors']:
        all_failures.append({
            'profile_name': error['profile_name'],
            'period': error['period'],
            'kind': error['kind'],
            'function': error['function'],
            'function_period': error['function_period'],
            'failure_type': 'Creation Failed',
            'expected_value': 'N/A',
            'actual_value': 'N/A',
            'error': f"Status {error['status_code']}: {error['error'][:100]}..."
        })
    
    # Add data retrieval failures
    for error in results['data_retrieval_errors']:
        all_failures.append({
            'profile_name': error['profile_name'],
            'period': 'Unknown',
            'kind': 'Unknown',
            'function': 'Unknown',
            'function_period': 'Unknown',
            'failure_type': 'Data Retrieval Failed',
            'expected_value': 'N/A',
            'actual_value': 'N/A',
            'error': str(error['error'])[:100] + "..."
        })
    
    if not all_failures:
        print("No failures to display!")
        return None
    
    # Create DataFrame for easier manipulation
    import pandas as pd
    df = pd.DataFrame(all_failures)
    
    # Create a heatmap-style visualization
    failure_types = df['failure_type'].unique()
    periods = df['period'].unique()
    
    # Count failures by type and period
    failure_matrix = []
    period_labels = []
    failure_labels = []
    
    for failure_type in failure_types:
        for period in periods:
            count = len(df[(df['failure_type'] == failure_type) & (df['period'] == period)])
            if count > 0:
                failure_matrix.append([failure_type, period, count])
    
    if not failure_matrix:
        return None
    
    # Create a detailed table visualization
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Profile Name', 'Period', 'Kind', 'Function', 'Function Period', 'Failure Type', 'Error Details'],
            fill_color='lightblue',
            align='left',
            font=dict(color='black', size=10)
        ),
        cells=dict(
            values=[
                df['profile_name'],
                df['period'],
                df['kind'],
                df['function'],
                df['function_period'],
                df['failure_type'],
                df['error']
            ],
            fill_color=[['lightcoral' if x == 'Creation Failed' else 
                        'lightyellow' if x == 'Validation Failed' else 
                        'lightpink' for x in df['failure_type']]],
            align='left',
            font=dict(color='black', size=9),
            height=30
        )
    )])
    
    fig.update_layout(
        title='Detailed Failed Profiles Information',
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def create_failure_heatmap(results):
    """Create a heatmap showing failure patterns by period and function."""
    
    import pandas as pd
    
    # Prepare data for heatmap
    all_data = []
    
    periods = ["P1Y", "P1M", "P3M", "P6M", "P1W", "PT1H", "PT15M", "PT5M", "PT1M", "PT10M", "PT3M", "PT1S", "P1D"]
    functions = ["sum", "avg", "min", "max"]
    
    # Initialize matrix
    for period in periods:
        for function in functions:
            # Count successful profiles
            successful = 0
            for profile in results['validation_passed']:
                if profile['period'] == period and profile['function'] == function:
                    successful += 1
            
            # Count failed profiles
            failed = 0
            for profile in results['validation_failed']:
                if profile['period'] == period and profile['function'] == function:
                    failed += 1
            
            # Count creation errors
            creation_failed = 0
            for error in results['creation_errors']:
                if error['period'] == period and error['function'] == function:
                    creation_failed += 1
            
            total = successful + failed + creation_failed
            success_rate = (successful / total * 100) if total > 0 else 0
            
            all_data.append({
                'Period': period,
                'Function': function,
                'Success_Rate': success_rate,
                'Successful': successful,
                'Failed': failed,
                'Creation_Failed': creation_failed,
                'Total': total
            })
    
    df = pd.DataFrame(all_data)
    
    # Create pivot table for heatmap
    pivot_success = df.pivot(index='Function', columns='Period', values='Success_Rate')
    pivot_total = df.pivot(index='Function', columns='Period', values='Total')
    
    # Create custom text for hover info
    hover_text = []
    for i, function in enumerate(functions):
        hover_row = []
        for j, period in enumerate(periods):
            row_data = df[(df['Function'] == function) & (df['Period'] == period)].iloc[0]
            text = f"Period: {period}<br>Function: {function}<br>" + \
                   f"Success Rate: {row_data['Success_Rate']:.1f}%<br>" + \
                   f"Successful: {row_data['Successful']}<br>" + \
                   f"Failed Validation: {row_data['Failed']}<br>" + \
                   f"Failed Creation: {row_data['Creation_Failed']}<br>" + \
                   f"Total Attempted: {row_data['Total']}"
            hover_row.append(text)
        hover_text.append(hover_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_success.values,
        x=pivot_success.columns,
        y=pivot_success.index,
        text=hover_text,
        texttemplate="%{text}",
        textfont={"size": 8},
        hovertemplate='%{text}<extra></extra>',
        colorscale='RdYlGn',
        zmin=0,
        zmax=100,
        colorbar=dict(title="Success Rate (%)")
    ))
    
    fig.update_layout(
        title='Profile Success Rate Heatmap by Period and Function',
        xaxis_title='Period',
        yaxis_title='Function',
        height=500,
        xaxis=dict(tickangle=45)
    )
    
    return fig

def create_profile_status_sunburst(results):
    """Create a sunburst chart showing the hierarchy of profile status."""
    
    import pandas as pd
    
    # Prepare hierarchical data
    sunburst_data = []
    
    # Add successful profiles
    for profile in results['validation_passed']:
        sunburst_data.append({
            'ids': f"Success-{profile['period']}-{profile['function']}-{profile['profile_name']}",
            'labels': profile['profile_name'],
            'parents': f"Success-{profile['period']}-{profile['function']}",
            'values': 1
        })
        
        sunburst_data.append({
            'ids': f"Success-{profile['period']}-{profile['function']}",
            'labels': profile['function'],
            'parents': f"Success-{profile['period']}",
            'values': 1
        })
        
        sunburst_data.append({
            'ids': f"Success-{profile['period']}",
            'labels': profile['period'],
            'parents': "Success",
            'values': 1
        })
    
    # Add failed validation profiles
    for profile in results['validation_failed']:
        sunburst_data.append({
            'ids': f"Failed-{profile['period']}-{profile['function']}-{profile['profile_name']}",
            'labels': profile['profile_name'],
            'parents': f"Failed-{profile['period']}-{profile['function']}",
            'values': 1
        })
        
        sunburst_data.append({
            'ids': f"Failed-{profile['period']}-{profile['function']}",
            'labels': profile['function'],
            'parents': f"Failed-{profile['period']}",
            'values': 1
        })
        
        sunburst_data.append({
            'ids': f"Failed-{profile['period']}",
            'labels': profile['period'],
            'parents': "Failed",
            'values': 1
        })
    
    # Add creation errors
    for error in results['creation_errors']:
        sunburst_data.append({
            'ids': f"Error-{error['period']}-{error['function']}-{error['profile_name']}",
            'labels': error['profile_name'],
            'parents': f"Error-{error['period']}-{error['function']}",
            'values': 1
        })
        
        sunburst_data.append({
            'ids': f"Error-{error['period']}-{error['function']}",
            'labels': error['function'],
            'parents': f"Error-{error['period']}",
            'values': 1
        })
        
        sunburst_data.append({
            'ids': f"Error-{error['period']}",
            'labels': error['period'],
            'parents': "Error",
            'values': 1
        })
    
    # Add root categories
    sunburst_data.extend([
        {'ids': 'Success', 'labels': 'Validation Passed', 'parents': '', 'values': 0},
        {'ids': 'Failed', 'labels': 'Validation Failed', 'parents': '', 'values': 0},
        {'ids': 'Error', 'labels': 'Creation Failed', 'parents': '', 'values': 0}
    ])
    
    df = pd.DataFrame(sunburst_data)
    
    # Remove duplicates and sum values
    df_grouped = df.groupby(['ids', 'labels', 'parents']).agg({'values': 'sum'}).reset_index()
    
    fig = go.Figure(go.Sunburst(
        ids=df_grouped['ids'],
        labels=df_grouped['labels'],
        parents=df_grouped['parents'],
        values=df_grouped['values'],
        branchvalues="total",
        maxdepth=3,
    ))
    
    fig.update_layout(
        title="Profile Status Hierarchy",
        height=600
    )
    
    return fig

def visualize_results(results):
    """Create and display all visualizations for the results."""
    
    print("Creating visualizations...")
    
    # Create original visualizations
    sankey_fig = create_sankey_diagram(results)
    sankey_fig.show()
    
    success_fig = create_success_rate_chart(results)
    success_fig.show()
    
    function_fig = create_function_comparison_chart(results)
    function_fig.show()
    
    kind_fig = create_kind_comparison_chart(results)
    kind_fig.show()
    
    dashboard_fig = create_comprehensive_dashboard(results)
    dashboard_fig.show()
    
    # Create new detailed failure visualizations
    print("Creating detailed failure analysis...")
    
    failed_details_fig = create_failed_profiles_detail_chart(results)
    if failed_details_fig:
        failed_details_fig.show()
    
    heatmap_fig = create_failure_heatmap(results)
    heatmap_fig.show()
    
    sunburst_fig = create_profile_status_sunburst(results)
    sunburst_fig.show()
    
    print("All visualizations have been displayed!")
    
    return {
        'sankey': sankey_fig,
        'success_rate': success_fig,
        'function_comparison': function_fig,
        'kind_comparison': kind_fig,
        'dashboard': dashboard_fig,
        'failed_details': failed_details_fig,
        'failure_heatmap': heatmap_fig,
        'profile_sunburst': sunburst_fig
    }

if __name__ == "__main__":
    results = creteProfileComputed()

    # Print all results where validation failed
    print(f"\n{'='*60}")
    print("VALIDATION FAILURES SUMMARY")
    print(f"{'='*60}")
    for profile in results['validation_failed']:
        month_info = ""
        if profile.get('test_month') and profile.get('test_year'):
            leap_info = " (Leap Year)" if profile.get('is_leap_year') else ""
            days_info = f" ({profile.get('days_in_month', 'N/A')} days)" if profile.get('days_in_month') else ""
            month_info = f" for {profile['test_year']}-{profile['test_month']:02d}{leap_info}{days_info}"
        
        print(f"Profile {profile['profile_name']} failed validation{month_info}: expected {profile['expected_value']}, got {profile['actual_value']}")
    
    # Export results to CSV for further analysis
    export_results_to_csv(results)
    
    # Create and display visualizations
    visualizations = visualize_results(results)
   