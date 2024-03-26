import os
import json
import xml.etree.ElementTree as ET


def parse_music_data(xml_file,music_id_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    music_info = {
        "name": root.find("./name/str").text,
        "id": root.find("./cueFileName/id").text,
        "genreNames": [genre.find("./str").text for genre in root.findall("./genreNames/list/StringID")],
        "jaketFile": os.path.join(music_id_dir, root.find("./jaketFile/path").text),
        "difficulties": {}
    }

    for fumen in root.findall("./fumens/MusicFumenData"):
        if fumen.find("./enable").text.lower() == 'false':
            level = 0
        else:
            level = float(fumen.find("./level").text)
            level += float(fumen.find("./levelDecimal").text) / 100
        music_info["difficulties"][fumen.find("./type/data").text.lower()] = level

    return music_info

all_music_info=[]
"""扫描A000文件歌曲"""
A000_dir = 'F:/SDHD - CHUNITHM LUMINOUS/HDD/data/A000'
music_dir = os.path.join(A000_dir, 'music')
for musicid in os.listdir(music_dir):
    """跳过GenreSort.xml与MusicSort.xml"""
    if musicid not in ["GenreSort.xml", "MusicSort.xml"]:
        music_id_dir = os.path.join(music_dir, musicid)
        xml_file = os.path.join(music_id_dir, 'Music.xml')
        music_info = parse_music_data(xml_file,music_id_dir)
        all_music_info.append(music_info)
    else:
        continue

"""扫描option文件歌曲"""
opt_music_info=[]
option_dir = 'F:/SDHD - CHUNITHM LUMINOUS/HDD/bin/option'
for opt_id in os.listdir(option_dir):
    music_dir=os.path.join(option_dir,opt_id,'music')
    """跳过没有music文件的opt包"""
    if not os.path.isdir(music_dir):
        continue
    for musicid in os.listdir(music_dir):
        music_id_dir = os.path.join(music_dir, musicid)
        xml_file = os.path.join(music_id_dir, 'Music.xml')
        music_info = parse_music_data(xml_file,music_id_dir)
        all_music_info.append(music_info)

"写入json文件"
filename = "lmn.json"
with open(filename, 'a',encoding='utf-8') as json_file:
    # 写入文件前的初始括号
    json_file.write("[\n")

    # 遍历 music_info 列表
    for i, music_info in enumerate(all_music_info):
        # 写入逗号和换行符，除了第一个 music_info 外
        if i != 0:
            json_file.write(",\n")
        # 写入当前 music_info
        json.dump(music_info, json_file, indent=4,ensure_ascii=False)
       #写入结尾括号
with open(filename, 'a') as json_file:
    json_file.write("\n]\n")