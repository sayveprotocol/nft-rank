import json
from collections import Counter

# Read the JSON data from the file
with open('./src/data.json', 'r') as data_file:
    data = json.load(data_file)

# Create dictionaries to store the frequency of numeric values and other traits
trait_frequencies = {trait_type: Counter() for trait_type in ["eyes", "features", "character", "background"]}

# Create a dictionary to store the updated data
updated_data = data.copy()

# Mapping for trait type conversions
trait_type_mapping = {
    "Eyes": "eyes",
    "eyes": "eyes",
    "Mouth": "features",
    "features": "features"
}

# First loop to calculate frequencies
for id in data.keys():
    data_id = data[id]["data"]["extension"]["attributes"]
    for attr in data_id:
        trait_type = attr["trait_type"]
        value = attr["value"]

        # Convert trait types to a common format
        converted_trait_type = trait_type_mapping.get(trait_type, trait_type)

        if converted_trait_type in trait_frequencies:
            if converted_trait_type in ["eyes", "features", "character", "background"]:
                trait_frequencies[converted_trait_type][value] += 1

# Second loop to calculate rarity
for id in data.keys():
    data_id = data[id]["data"]["extension"]["attributes"]

    # Create a dictionary to store the rarity scores for this token
    rarity_scores = {}

    # Calculate rarity for each trait type
    for attr in data_id:
        trait_type = attr["trait_type"]
        value = attr["value"]

        # Convert trait types to a common format
        converted_trait_type = trait_type_mapping.get(trait_type, trait_type)

        if converted_trait_type in ["eyes", "features", "character", "background"]:
            rarity_score = 0  # Default to 0 for division by zero
            if value in trait_frequencies[converted_trait_type]:
                rarity_score = (1 / trait_frequencies[converted_trait_type][value]) * 100
            rarity_scores[converted_trait_type.lower() + "_rarity"] = rarity_score
        if converted_trait_type in ["vigor", "resilience", "wages"]:
            # Calculate rarity for traits based on their values
            rarity_score = 0  # Default to 0 for traits without frequency counts
            if value:
                rarity_score = 1 - (float(value) / 20.0)  # Scale rarity between 0 and 1, with higher values resulting in lower rarity

            rarity_scores[converted_trait_type.lower() + "_rarity"] = rarity_score


    # Update the updated_data dictionary with trait types and rarity scores
    updated_data[id]["data"]["extension"]["attributes"] = data_id + [{"trait_type": key.lower() + "_rarity", "value": value} for key, value in rarity_scores.items()]

# Save the JSON data with the new trait data to a new file
with open('data_with_rarity.json', 'w') as output_file:
    json.dump(updated_data, output_file, indent=4)
