import json
from collections import Counter

# Read the JSON data from the file
with open('data.json', 'r') as data_file:
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

# Second loop to calculate rarity and total rarity per ID
for id in data.keys():
    data_id = data[id]["data"]["extension"]["attributes"]

    # Create a dictionary to store the rarity scores for this token
    rarity_scores = {}

    # Initialize a list to store individual rarity scores per ID
    individual_rarities = []

    # Initialize variables to calculate pfp_rarity and game_rarity
    pfp_rarity_sum = 0
    pfp_rarity_count = 0
    game_rarity_sum = 0
    game_rarity_count = 0

    # Calculate rarity for each trait type
    for attr in data_id:
        trait_type = attr["trait_type"]
        value = attr["value"]

        # Convert trait types to a common format
        converted_trait_type = trait_type_mapping.get(trait_type, trait_type)

        if converted_trait_type in ["eyes", "features", "character", "background"]:
            rarity_score = 0  # Default to 0 for division by zero
            if value in trait_frequencies[converted_trait_type]:
                total_count = sum(trait_frequencies[converted_trait_type].values())
                rarity_score = (trait_frequencies[converted_trait_type][value] / total_count)

            rarity_scores[converted_trait_type.lower() + "_rarity"] = rarity_score
            individual_rarities.append(rarity_score)
            if converted_trait_type in ["eyes", "features", "character", "background"]:
                pfp_rarity_sum += rarity_score
                pfp_rarity_count += 1
        if converted_trait_type in ["vigor", "resilience", "wages"]:
            # Calculate rarity for traits based on their values
            rarity_score = 0  # Default to 0 for traits without frequency counts
            if value:
                rarity_score = 1 - (float(value) / 20.0)  # Scale rarity between 0 and 1, with higher values resulting in lower rarity

            rarity_scores[converted_trait_type.lower() + "_rarity"] = rarity_score
            individual_rarities.append(rarity_score)
            if converted_trait_type in ["vigor", "resilience", "wages"]:
                game_rarity_sum += rarity_score
                game_rarity_count += 1

    # Calculate the total rarity as an average of all individual rarities
    if individual_rarities:
        total_rarity = sum(individual_rarities) / len(individual_rarities)
    else:
        total_rarity = 0

    # Add the total rarity to the rarity_scores dictionary
    rarity_scores["total_rarity"] = total_rarity

    # Calculate pfp_rarity as an average of "eyes," "features," "character," and "background" rarities
    if pfp_rarity_count:
        pfp_rarity = pfp_rarity_sum / pfp_rarity_count
    else:
        pfp_rarity = 0

    # Add the pfp_rarity to the rarity_scores dictionary
    rarity_scores["pfp_rarity"] = pfp_rarity

    # Calculate game_rarity as an average of "vigor," "resilience," and "wages" rarities
    if game_rarity_count:
        game_rarity = game_rarity_sum / game_rarity_count
    else:
        game_rarity = 0

    # Add the game_rarity to the rarity_scores dictionary
    rarity_scores["game_rarity"] = game_rarity

    # Update the updated_data dictionary with trait types and rarity scores
    data_id.append({"trait_type": "total_rarity", "value": total_rarity})
    data_id.append({"trait_type": "pfp_rarity", "value": pfp_rarity})
    data_id.append({"trait_type": "game_rarity", "value": game_rarity})
    updated_data[id]["data"]["extension"]["attributes"] = data_id + [{"trait_type": key.lower() + "_rarity", "value": value} for key, value in rarity_scores.items()]


# Save the JSON data with the new trait data to a new file
with open('data_with_rarity.json', 'w') as output_file:
    json.dump(updated_data, output_file, indent=4)
