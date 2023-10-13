Objective: The code aims to calculate rarity scores for various trait types in a JSON dataset, with the rarity scores ranging from 0 to 1. Higher values for certain traits result in lower rarity scores.

Input: The input is a JSON dataset (loaded from the file data.json) containing tokens with different trait types and values. Trait types include "Eyes," "Mouth," "vigor," "wages," "resilience," "character," "background," and their variations.

Output: The output is a modified JSON dataset (saved as data_with_rarity.json) with added trait types and rarity scores for each token. The rarity scores are scaled between 0 and 1.

Procedure:

Load the JSON data from data.json and create a copy to store the updated data.

Define a mapping for trait type conversions to ensure uniform processing.

Iterate through each token in the dataset.

For each token, calculate rarity scores for specific trait types:

For "vigor," "resilience," and "wages," rarity is based on their values. A higher value corresponds to a lower rarity score, scaled between 0 and 1.
For other trait types, rarity is calculated based on the frequency of occurrence in the dataset.
Update the dataset with trait types and their corresponding rarity scores.

Save the updated JSON dataset to a new file (data_with_rarity.json).

Extraction of Color and Numeric Values:

Trait Types Extraction:

The code starts by iterating through each token in the dataset. It extracts the "trait_type" and "value" for each attribute in the token.
Numeric Values Extraction:

To extract numeric values from the trait types, the code checks if the current trait type belongs to the following categories:
"Eyes" and its variations: If the trait type contains "Eyes," it splits the string by "-" and extracts the last part, which is assumed to be numeric.
"features" and its variations: If the trait type contains "features," it splits the string by "-" and extracts the last part, which is assumed to be numeric.
"vigor," "wages," and "resilience": For these traits, numeric values are already in numeric format and are directly used.
Color Extraction:

Color information is not explicitly extracted in the code, but it can be assumed based on the remaining part of the trait type (excluding the numeric value). For example:
"Eyes" and its variations are assumed to contain color information.
"features" and its variations are assumed to contain color information.
Trait Frequency Calculation:

After extracting numeric values and determining the remaining part of the trait type as color, the code calculates the frequency of each combination of trait type and numeric value. The frequency counters, such as trait_frequencies, are used to store these counts.
Rarity Calculation for Numeric Values:

For trait types such as "Eyes" and "features," the rarity score is calculated based on the frequency of each numeric value. The rarity score is scaled from 0 to 1, where higher rarity corresponds to lower frequency.
Trait Type Conversion:

The code also performs trait type conversion to ensure uniform processing. For example, "Eyes" and "eyes" are converted to "eyes," while "Mouth" and "features" are converted to "features."