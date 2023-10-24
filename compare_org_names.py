import os
import re
import pandas as pd
import math


def cosine_similarity(str1, str2):
    # Tokenize the strings
    tokens_str1 = str1.lower().split()
    tokens_str2 = str2.lower().split()

    # Create a combined vocabulary
    vocabulary = set(tokens_str1).union(set(tokens_str2))

    # Create vectors using the vocabulary
    vector_str1 = [tokens_str1.count(word) for word in vocabulary]
    vector_str2 = [tokens_str2.count(word) for word in vocabulary]

    # Compute the dot product
    dot_product = sum([vector_str1[i] * vector_str2[i] for i in range(len(vector_str1))])

    # Compute the magnitudes of the vectors
    magnitude_str1 = math.sqrt(sum([vector_str1[i] ** 2 for i in range(len(vector_str1))]))
    magnitude_str2 = math.sqrt(sum([vector_str2[i] ** 2 for i in range(len(vector_str2))]))

    # Compute the cosine similarity
    if magnitude_str1 * magnitude_str2 == 0:
        return 0
    else:
        return dot_product / (magnitude_str1 * magnitude_str2)


def jaccard_similarity(str1, str2):
    """Calculate Jaccard Similarity between two strings."""
    set1 = set(clean_string(str1).lower().split())
    set2 = set(clean_string(str2).lower().split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0
    return intersection / union


def clean_string(input_str):
    # Remove any non-alphabetic characters
    cleaned_str = re.sub(r'[^a-zA-Z\s]', '', input_str)
    # Truncate any remaining whitespace sequences to a single space
    cleaned_str = re.sub(r'\s+', ' ', cleaned_str).strip()
    return cleaned_str


def main():
    input_filepath = os.path.join("data", "ps_org_units.xls")

    # Load the data from the two sheets
    org_unit_df = pd.read_excel(input_filepath, sheet_name="OrganisationalUnit")
    cms_org_units_df = pd.read_excel(input_filepath, sheet_name="cms_org_units")
    ps_depts_df = pd.read_excel(input_filepath, sheet_name="PeopleSoft")

    # Create a dataframe to store the best matches for each "Name"
    best_matches = []

    # For each name in the "Name" column, identify the best match from "OrgUnitDesc"
    for cms_org_unit_name in cms_org_units_df["Name"]:
        best_org_similarity = 0
        best_org_match = ""
        best_ps_similarity = 0
        best_ps_match = ""

        # Compare the "Organisational Unit" sheet (where did this come from?)
        for org_unit_name in org_unit_df["OrgUnitDesc"]:
            j_similarity = jaccard_similarity(org_unit_name, cms_org_unit_name)
            c_similarity = cosine_similarity(org_unit_name, cms_org_unit_name)

            # If the current match is better than the previous best, update the best match
            max_similarity = max(j_similarity, c_similarity)
            if max_similarity > best_org_similarity:
                best_org_similarity = max_similarity
                best_org_match = org_unit_name

        # Compare to the "PeopleSoft" tab "Full Description" column
        for org_unit_name in ps_depts_df["Full Description"]:
            j_similarity = jaccard_similarity(org_unit_name, cms_org_unit_name)
            c_similarity = cosine_similarity(org_unit_name, cms_org_unit_name)

            # If the current match is better than the previous best, update the best match
            max_similarity = max(j_similarity, c_similarity)
            if max_similarity > best_ps_similarity:
                best_ps_similarity = max_similarity
                best_ps_match = org_unit_name

        best_matches.append({
            "Name": cms_org_unit_name,
            "Best Match (OrgUnitDesc)": best_org_match,
            "Similarity (OrgUnitDesc)": best_org_similarity,
            "Best Match (PeopleSoft)": best_ps_match,
            "Similarity (PeopleSoft)": best_ps_similarity,
        })

    best_matches_df = pd.DataFrame(best_matches)

    # Save the matches to a CSV
    file_path = os.path.join("data", "best_matches.csv")
    best_matches_df.to_csv(file_path, index=False)


if __name__ == "__main__":
    main()


