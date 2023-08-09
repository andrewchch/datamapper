import pandas as pd
import requests
import argparse
import pickle
import re

from tqdm import tqdm
from collections import defaultdict

url_pattern = re.compile(r'http[s]?://[^\]\s]+')


def check_url_exists(url):
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


def extract_urls(text):
    # Regular expression to match URLs
    try:
        return url_pattern.findall(text)
    except TypeError as e:
        return []


def main():
    parser = argparse.ArgumentParser(description="Process some file.")
    parser.add_argument('filename', type=str, help='The name of the file to process.')
    parser.add_argument('type', type=str, help='type of URL being processed.')

    args = parser.parse_args()
    src = args.filename
    url_type = args.type

    # 1. Read a list of URLs from an Excel file
    df = pd.read_excel(src)

    # Fetch the pickled url_exists_dict
    try:
        with open('url_exists_dict.pkl', 'rb') as f:
            url_exists_dict = pickle.load(f)
    except FileNotFoundError:
        url_exists_dict = {}

    # 2. Compile a list of unique URLs
    code_urls = defaultdict(set)
    code_details = defaultdict(tuple)
    output_data = []
    url_codes = defaultdict(set)  # mirror dict of codes per URL

    # iterate over each row in the dataframe using tqdm to show progress
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows", unit="row"):
        text = row['URL']
        urls = extract_urls(text)

        # Also track which URLs are associated with which course
        code = row['CourseCode']
        code_urls[code].update(urls)
        code_details[code] = (
            row['GivenNames'],
            row['FamilyName'],
            row['CourseContributorRoleDesc'],
            row['OrgUnitDesc'],
            row['SupplementaryTypeDesc']
        )

        # Update the existence of each unique URL
        for url in urls:
            exists = None
            if not pd.isna(url):
                exists = url_exists_dict.get(url, None)
                if exists is None:
                    exists = check_url_exists(url)
                    url_exists_dict[url] = exists

                url_codes[url].add(code)

            # Store a record for each code and URL
            output_data.append({"code": code, "URL": url, "exists": exists})

    # Pickle the url_exists_dict
    with open('url_exists_dict.pkl', 'wb') as f:
        pickle.dump(url_exists_dict, f)

    # 4. Create an output Excel file
    output_df = pd.DataFrame(output_data)
    output_df.to_excel("data\%s_urls_out.xlsx" % url_type, index=False)

    # Create an Excel file with unique URLs that do not exist and the corresponding code
    non_existent_df = pd.DataFrame([k for k, v in url_exists_dict.items() if v is False], columns=["URL"])
    non_existent_df.to_excel("data\\non_existent_%s_urls.xlsx" % url_type, index=False)

    # Create an excel file listing all codes associated with non-existent URLs, with one row per (code, URL) combination
    ne_code_url_list = []
    for url, codes in url_codes.items():
        if url_exists_dict[url] is False:
            for code in codes:
                fn, ln, role, org_unit, supplementary_type = code_details[code]
                ne_code_url_list.append({
                    "code": code,
                    "URL": url,
                    "GivenNames": fn,
                    "FamilyName": ln,
                    "CourseContributorRoleDesc": role,
                    "OrgUnitDesc": org_unit,
                    "SupplementaryTypeDesc": supplementary_type
                })

    non_existent_codes_df = pd.DataFrame(ne_code_url_list)
    non_existent_codes_df.to_excel("data\\non_existent_%s_url_codes.xlsx" % url_type, index=False)


if __name__ == "__main__":
    main()
