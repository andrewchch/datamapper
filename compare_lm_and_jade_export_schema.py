
# Importing necessary libraries
import pandas as pd

# Loading the datasets
jade_data = pd.read_excel("jade_export_norm_cols.xls")
lm_attributes = pd.read_excel("logical_model_tables_and_columns.xlsx")

# Extracting relevant columns
jade_relevant_cols_updated = jade_data[["TABLE_NAME", "COLUMN_NAME", "DATA_TYPE", "CHARACTER_MAXIMUM_LENGTH", "IS_NULLABLE"]]
merged_attributes_relevant_cols_with_export_file = lm_attributes[["Table Name", "Column Name"]]

# Creating merge key with a fallback mechanism
lm_attributes["Merge_Key"] = lm_attributes["Column Name"].str.lower()
jade_data["Merge_Key"] = jade_data["COLUMN_NAME"].str.lower()

# Adjusting the merging criteria for case-insensitive comparison
lm_attributes["Table Name (lower)"] = lm_attributes["Table Name"].str.lower()
jade_data["TABLE_NAME (lower)"] = jade_data["TABLE_NAME"].str.lower()

# Merging datasets using the adjusted criteria
retried_merge = pd.merge(lm_attributes, jade_data,
                         left_on=["Table Name (lower)", "Merge_Key"],
                         right_on=["TABLE_NAME (lower)", "Merge_Key"],
                         how="left")

# Adding a "Match_Status" column
retried_merge["Match_Status"] = "Matched"
retried_merge.loc[retried_merge["TABLE_NAME"].isna(), "Match_Status"] = "Not Matched"

# Counting matches and extracting matched table name values
match_counts_retried = retried_merge["Match_Status"].value_counts()
matched_target_entities_retried = retried_merge[retried_merge["Match_Status"] == "Matched"]["Table Name"].unique()

# Exporting the results
retried_merge.to_excel("lm_jade_export_matched.xlsx", index=False)
