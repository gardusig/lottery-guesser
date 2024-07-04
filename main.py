import openpyxl
import json


def filter_and_sort_balls(file_path: str):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    results = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        balls_draw_1 = row[2:8]
        balls_draw_2 = row[18:24]
        balls_draw_1 = [int(ball) for ball in balls_draw_1 if isinstance(
            ball, (int, float)) or (isinstance(ball, str) and ball.isnumeric())]
        balls_draw_2 = [int(ball) for ball in balls_draw_2 if isinstance(
            ball, (int, float)) or (isinstance(ball, str) and ball.isnumeric())]
        sorted_balls_draw_1 = sorted(balls_draw_1)
        sorted_balls_draw_2 = sorted(balls_draw_2)
        results.append(sorted_balls_draw_1)
        results.append(sorted_balls_draw_2)
    frequency_at_index = [[0 for _ in range(6)] for _ in range(51)]
    for result in results:
        for index, ball in enumerate(result):
            frequency_at_index[ball][index] += 1
    return frequency_at_index, results


def get_top_balls_per_position(frequency_at_index, top_n=10):
    top_balls_per_position = []
    for i in range(6):
        position_frequencies = [(ball, frequency_at_index[ball][i])
                                for ball in range(1, 51)]
        sorted_position_frequencies = sorted(
            position_frequencies, key=lambda x: (-x[1], x[0]))
        top_balls_per_position.append({
            f"position_{i+1}": [
                {"ball_number": ball, "ball_frequency": freq}
                for ball, freq in sorted_position_frequencies[:top_n]
            ]
        })
    return top_balls_per_position


def get_overall_top_balls(frequency_at_index, top_n=10):
    total_frequencies = [(ball, sum(frequency_at_index[ball]))
                         for ball in range(1, 51)]
    sorted_total_frequencies = sorted(
        total_frequencies, key=lambda x: (-x[1], x[0]))
    overall_top_balls = [
        {"ball_number": ball, "ball_frequency": freq}
        for ball, freq in sorted_total_frequencies[:top_n]
    ]
    return overall_top_balls


def save_to_json(file_path, top_balls_per_position, overall_top_balls):
    data = {
        "top_balls_per_position": top_balls_per_position,
        "overall_top_balls": overall_top_balls
    }
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    input_file = "input.xlsx"
    json_file = "ball_frequency.json"
    frequency_at_index, _ = filter_and_sort_balls(input_file)
    top_balls_per_position = get_top_balls_per_position(frequency_at_index)
    overall_top_balls = get_overall_top_balls(frequency_at_index)
    save_to_json(json_file, top_balls_per_position, overall_top_balls)
