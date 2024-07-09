import json
import random


def load_ball_frequencies(ball_frequency_file):
    with open(ball_frequency_file, 'r') as f:
        data = json.load(f)
    return data["top_balls_per_position"], data["overall_top_balls"]


def load_previous_results(results_json_file):
    with open(results_json_file, 'r') as f:
        previous_results = json.load(f)
    return previous_results


def evaluate_combination(combination, previous_results):
    match_count = 0
    for result in previous_results:
        if are_combinations_close(combination, result):
            match_count += 1
    return match_count


def are_combinations_close(combination1, combination2, max_distance=10):
    for num1 in combination1:
        for num2 in combination2:
            if abs(num1 - num2) <= max_distance:
                return True
    return False


def rank_combinations(random_combinations, previous_results):
    ranked_combinations = []
    for combination in random_combinations:
        match_count = evaluate_combination(combination, previous_results)
        ranked_combinations.append((combination, match_count))
    ranked_combinations.sort(key=lambda x: x[1], reverse=True)
    return ranked_combinations


def save_ranked_combinations(file_path, ranked_combinations):
    with open(file_path, 'w') as f:
        json.dump(ranked_combinations, f, indent=4)


def generate_random_combinations(top_balls_per_position, overall_top_balls, num_combinations=1000, random_variation=2):
    most_common_positions = get_most_common_positions(top_balls_per_position)
    overall_top_values = [entry["ball_number"]
                          for entry in overall_top_balls[:num_combinations]]
    random_combinations = []
    for _ in range(num_combinations):
        combination = []
        for pos_data in most_common_positions:
            top_values = pos_data["top_values"]
            if random.random() < 0.5:
                selected_values = top_values
            else:
                selected_values = overall_top_values

            selected_value = random.choice(selected_values)

            random_variation_value = random.uniform(
                -random_variation, random_variation)
            selected_value += random_variation_value
            # Adjust range if needed
            selected_value = max(1, min(selected_value, 60))

            combination.append(selected_value)

        random_combinations.append(combination)

    return random_combinations


def save_random_combinations(file_path, random_combinations):
    with open(file_path, 'w') as f:
        json.dump(random_combinations, f, indent=4)


def get_most_common_positions(top_balls_per_position, ball_count=10):
    most_common_positions = []
    for pos_data in top_balls_per_position:
        most_common_positions.append({
            "position": pos_data["position"],
            "top_values": [entry["ball_number"] for entry in pos_data["top_values"][:ball_count]]
        })
    return most_common_positions


def main():
    ball_frequency_file = "./dupla-sena/generated/ball_frequency.json"
    results_json_file = "./dupla-sena/generated/previous_results.json"
    ranked_combinations_file = "./dupla-sena/generated/ranked_combinations.json"

    top_balls_per_position, overall_top_balls = load_ball_frequencies(
        ball_frequency_file)
    previous_results = load_previous_results(results_json_file)

    random_combinations = generate_random_combinations(
        top_balls_per_position, overall_top_balls)

    ranked_combinations = rank_combinations(
        random_combinations, previous_results)
    save_ranked_combinations(ranked_combinations_file, ranked_combinations)


if __name__ == "__main__":
    main()
