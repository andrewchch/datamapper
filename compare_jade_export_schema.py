
# Importing necessary libraries
import pandas as pd

# Loading the datasets
jade_data_updated = pd.read_excel("jade_export_norm_cols.xls")
merged_attributes_updated = pd.read_excel("JADE and CIS - merged attributes.xlsx")

# Extracting relevant columns
jade_relevant_cols_updated = jade_data_updated[["TABLE_NAME", "COLUMN_NAME", "DATA_TYPE", "CHARACTER_MAXIMUM_LENGTH", "IS_NULLABLE"]]
merged_attributes_relevant_cols_with_export_file = merged_attributes_updated[["Ref #", "Info category", "CIS Webpage Field", "TargetEntity",
                                                                             "Export file field name", "DataType", "Description", "Example",
                                                                             "Suggestion for future state CDM (include, exclude, combine, modify)"]]

# Creating merge key with a fallback mechanism
merged_attributes_updated["Merge_Key"] = merged_attributes_updated["Export file field name"].fillna(merged_attributes_updated["FieldName"]).str.lower()
jade_data_updated["Merge_Key"] = jade_data_updated["COLUMN_NAME"].str.lower()

# Adjusting the merging criteria for case-insensitive comparison
merged_attributes_updated["TargetEntity (lower)"] = merged_attributes_updated["TargetEntity"].str.lower()
jade_data_updated["TABLE_NAME (lower)"] = jade_data_updated["TABLE_NAME"].str.lower()

# Merging datasets using the adjusted criteria
retried_merge = pd.merge(merged_attributes_updated, jade_data_updated,
                         left_on=["TargetEntity (lower)", "Merge_Key"],
                         right_on=["TABLE_NAME (lower)", "Merge_Key"],
                         how="left")

# Adding a "Match_Status" column
retried_merge["Match_Status"] = "Matched"
retried_merge.loc[retried_merge["TABLE_NAME"].isna(), "Match_Status"] = "Not Matched"

# Counting matches and extracting matched "TargetEntity" values
match_counts_retried = retried_merge["Match_Status"].value_counts()
matched_target_entities_retried = retried_merge[retried_merge["Match_Status"] == "Matched"]["TargetEntity"].unique()

# Exporting the results
retried_merge.to_excel("merged_attributes_jade_export_retried.xlsx", index=False)
