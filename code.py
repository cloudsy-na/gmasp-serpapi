from serpapi import GoogleSearch
import json
import pandas as pd
import os

params = {
    "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",   # API key from environment variable
    "engine": "google_maps_reviews",                                                 # serpapi search engine
    "hl": "id",                                                                      # language of the search
    "data_id": "0x2e69eb395fa7b3b9:0x3e935c615cc3aec4"                               # place id from Google Maps Place URL
}

search = GoogleSearch(params)

reviews = []

page_num = 0
while True:
    page_num += 1
    results = search.get_dict()

    print(f"Extracting reviews from {page_num} page.")

    if "error" not in results:
        for result in results.get("reviews", []):
            # Only collect the desired fields: name, rating, date, and snippet
            user = result.get("user", {})
            reviews.append({
                "name": user.get("name", ""),
                "rating": result.get("rating", ""),
                "date": result.get("date", ""),
                "snippet": result.get("snippet", ""),
            })
    else:
        print(results["error"])
        break

    # Check for next page using next_page_token, making sure it's not None
    pagination = results.get("serpapi_pagination")
    if pagination and pagination.get("next_page_token"):
        next_page_token = pagination.get("next_page_token")
        # Update search parameters with the new page token
        search.params_dict.update({"next_page_token": next_page_token})
    else:
        break

# Print reviews as JSON
# print(json.dumps(reviews, indent=2, ensure_ascii=False))

# Save the reviews to CSV
df = pd.DataFrame(reviews)
df.to_csv("data_mahakam.csv", index=False)
