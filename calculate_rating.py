import json

def load_music_data_from_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        music_data = json.load(f)
    return music_data

def calculate_rating(constant, score):
    #传入定数和分数计算单曲rating
    if score >= 1009000:
        return constant + 2.15
    elif 1007500 <= score < 1009000:
        return constant + 2.0 + 0.15 * (score - 1007500) / 1500
    elif 1005000 <= score < 1007500:
        return constant + 1.5 + 0.5 * (score - 1005000) / 2500
    elif 1000000 <= score < 1005000:
        return constant + 1.0 + 0.5 * (score - 1000000) / 5000
    elif 975000 <= score < 1000000:
        return constant + (score - 975000) / 25000
    elif 925000 <= score < 975000:
        return constant - 3.0 + 3.0 * (score - 925000) / 50000
    elif 900000 <= score < 925000:
        return constant - 5.0 + 2.0 * (score - 900000) / 25000
    elif 800000 <= score < 900000:
        return (constant - 5.0) / 2 + (constant - 5.0) / 2 * (score - 800000) / 100000
    else:
        return 0

def get_difficulty_name_value(music_id, music_data):
    music_id = str(music_id)
    for music_entry in music_data:
        if music_entry['id'] == music_id:
            return music_entry['difficulties'],music_entry['name'],music_entry['jaketFile']
    return None

def convert_level_to_difficulty(level):
    difficulty_mapping = {
        0: "basic",
        1: "advanced",
        2: "expert",
        3: "master",
        4: "ultima",
        5: "world's end"
    }
    return difficulty_mapping.get(level, None)



