import os
import xml.etree.ElementTree as ET

# 指定包含所有XML文件的文件夹路径SDHD - CHUNITHM LUMINOUS SDHD - CHUNITHM SUN PLUS F:/SDHD - CHUNITHM LUMINOUS/HDD/data/A000/chara
folder_path = 'F:/SDHD - CHUNITHM LUMINOUS/HDD/data/A000/chara'
opt_folder_path='F:/SDHD - CHUNITHM LUMINOUS/HDD/bin/option'
# 存储提取的数据的列表
data_list = []
chara_path=os.listdir(folder_path)[:-1]
# 遍历A000文件夹中的每个文件
for filename in chara_path:
        file_path = os.path.join(folder_path, filename,"Chara.xml")
        tree = ET.parse(file_path)
        root = tree.getroot()
        # 提取 <name> 下的 <id> 和 <str>
        name_id = root.find('.//name/id').text
        name_str = root.find('.//name/str').text
        # 提取 <works> 下的 <str>
        works_str = root.find('.//works/str').text
        # 创建一个字典存储提取的数据
        data = {
            'name_id': name_id,
            'name_str': name_str,
            'works_str': works_str
        }
        # 将字典添加到数据列表中
        data_list.append(data)
#遍历opt包中的chara
for opt_id in os.listdir(opt_folder_path):
    chara_dir= os.path.join(opt_folder_path, opt_id, 'chara')
    """跳过没有chara文件的opt包"""
    if not os.path.isdir(chara_dir):
        continue
    for filename in os.listdir(chara_dir):
        if filename=="CharaSort.xml":
            continue
        file_path = os.path.join(chara_dir, filename, "Chara.xml")
        tree = ET.parse(file_path)
        root = tree.getroot()
        # 提取 <name> 下的 <id> 和 <str>
        name_id = root.find('.//name/id').text
        name_str = root.find('.//name/str').text
        # 提取 <works> 下的 <str>
        works_str = root.find('.//works/str').text
        # 创建一个字典存储提取的数据
        data = {
            'name_id': name_id,
            'name_str': name_str,
            'works_str': works_str
        }
        # 将字典添加到数据列表中
        data_list.append(data)

#查找特定的角色和IP
#プロジェクトセカイ カラフルステージ！ feat. 初音ミク
target_name_str=""
target_works_str="ぼっち"


if target_name_str!="":
    for data in data_list:
        #if data['name_str'] == target_name_str:
        if target_name_str in data['name_str']:
            # 打印对应的name_id,name_str和works_str
            print(f"Name ID: {data['name_id']}")
            print(f"Name Str: {data['name_str']}")
            print(f"Works Str: {data['works_str']}\n")


if target_works_str!="":
    for data in data_list:
        #if data['works_str'] == target_works_str:
        if target_works_str in data['works_str']:
            # 打印对应的name_id,name_str和works_str
            print(f"Name ID: {data['name_id']}")
            print(f"Name Str: {data['name_str']}")
            print(f"Works Str: {data['works_str']}\n")
