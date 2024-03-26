import sqlite3
from calculate_rating import calculate_rating,get_difficulty_name_value,load_music_data_from_json,convert_level_to_difficulty

# 指定数据库文件和定数表的路径
db_file_path = 'F:/rinsama-aqua/rinsama-aqua/data/db.sqlite'
json_path="test.json"
# 连接到数据库文件
conn = sqlite3.connect(db_file_path)

# 创建一个游标对象，用于执行SQL语句
cursor = conn.cursor()

"""查询数据库并计算歌曲对应rating"""
cursor.execute('SELECT music_id, score_max,level,is_all_justice,is_full_combo FROM chusan_user_music_detail')
rows = cursor.fetchall()
rating_list = []
"""定数列表"""
music_data = load_music_data_from_json(json_path)

for row in rows:
    music_id, score_max,level,is_all_justice,is_full_combo = row
    """获取定数"""
    difficulty_data,music_name,jacket=get_difficulty_name_value(music_id, music_data)
    difficulte=convert_level_to_difficulty(level)
    constant=difficulty_data.get(difficulte, None)
    """获取单曲rating"""
    rating_value = calculate_rating(constant, score_max)
    rating_list.append({'music_id': music_id, 'score_max': score_max, 'rating': rating_value,'level':level,'constant':constant,'is_all_justice':is_all_justice,'is_full_combo':is_full_combo,'music_name':music_name,'jacket':jacket})
    """取rating最高的30首乐曲"""
sorted_rating_list = sorted(rating_list, key=lambda x: x['rating'], reverse=True)
top_30_ratings = sorted_rating_list[:30]
for item in top_30_ratings:
    """将 'rating' 对应的值保留两位小数"""
    item['rating'] = round(item['rating'], 2)
count=1
for rating_item in top_30_ratings:
    music_name=rating_item['music_name']
    difficulte=convert_level_to_difficulty(rating_item['level'])
    rating = str(round(rating_item['rating'], 2))  # 将评分转换为字符串并保留两位小数
    score_max = str(rating_item['score_max'])
    constant=str(rating_item['constant'])
    idx=str(count)
    """输出是否AJ或者FC"""
    if(rating_item['is_all_justice']==1):
        print(idx + " " + music_name + " " + difficulte + " rating: " + constant + "->" + rating + " 最高分数：" + score_max+" AJ"+"\n")
    elif(rating_item['is_full_combo']==1):
        print(idx + " " + music_name + " " + difficulte + " rating: " + constant + "->" + rating + " 最高分数：" + score_max+" FC"+"\n")
    else:
        print(idx + " " + music_name + " " + difficulte + " rating: " + constant + "->" + rating + " 最高分数：" + score_max+"\n")
    count=count+1

# 关闭游标和数据库连接
cursor.close()
conn.close()