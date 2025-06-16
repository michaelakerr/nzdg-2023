import numpy as np

# Base points for each placement
BASE_POINTS = {
    1: 100, 2: 80, 3: 70, 4: 60, 5: 55, 6: 50, 7: 45, 8: 40, 9: 35, 10: 30
}

# Minimum points for participation (if placement > 10)
MIN_POINTS = 10

# Number of best events to consider for final score
BEST_X_EVENTS = 6

def calculate_points(placement, division_size):
    """Calculate points for a given placement and division size."""
    if placement == "Not Played":
        return 0  # No points if not played

    placement = int(placement)  # Convert placement to integer
    base_score = BASE_POINTS.get(placement, MIN_POINTS)  # Get base score, defaulting to MIN_POINTS

    # Scaling factor based on division size (normalized around 10 players)
    scaling_factor = 1 + (division_size - 10) / 50  # Adjust based on division size
    return round(base_score * scaling_factor, 2)

def calculate_overall_scores(results):
    """
    Takes a dictionary of player results and calculates final scores.
    Results format: { "Player Name": { "Event 1": (placement, division_size), "Event 2": "Not Played", ... } }
    """
    player_scores = {}

    for player, events in results.items():
        event_scores = []

        for event, result in events.items():
            if isinstance(result, tuple):  # Ensure it's a played event
                placement, division_size = result
                score = calculate_points(placement, division_size)
                event_scores.append(score)

        # Sort scores (best to worst) and sum the best X events
        best_scores = sorted(event_scores, reverse=True)[:BEST_X_EVENTS]
        final_score = round(sum(best_scores), 2)

        player_scores[player] = final_score

    return player_scores

# Example Data (Player results per event)
results = {
    "Mac": {
        "Event 1": (1, 20),  # 1st place, 20 players
        "Event 2": "Not Played",
        "Event 3": (5, 10),  # 5th place, 10 players
        "Event 4": (3, 30),  # 3rd place, 30 players
        "Event 5": "Not Played",
        "Event 6": (2, 15)   # 2nd place, 15 players
    },
    "Alex": {
        "Event 1": (4, 25),
        "Event 2": (7, 18),
        "Event 3": "Not Played",
        "Event 4": (2, 40),
        "Event 5": (1, 12),
        "Event 6": "Not Played"
    },
    "Jordan": {
        "Event 1": (10, 30),
        "Event 2": (9, 22),
        "Event 3": (8, 15),
        "Event 4": "Not Played",
        "Event 5": "Not Played",
        "Event 6": "Not Played"
    }
}

# Calculate scores and print results
final_scores = calculate_overall_scores(results)

print("Final Scores:")
for player, score in sorted(final_scores.items(), key=lambda x: x[1], reverse=True):
    print(f"{player}: {score}")
