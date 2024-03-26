import sqlite3
from calculate_rating import calculate_rating,get_difficulty_name_value,load_music_data_from_json,convert_level_to_difficulty
from PIL import Image,ImageFont, ImageDraw
import os
import imageio.v2 as imageio
import xml.etree.ElementTree as ET

"""将b30查询封装为一个函数"""
def b30(db_file_path):
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
        """获取定数,曲名，封面地址"""
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
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return top_30_ratings

"""返回r10列表"""
def r10(db_file_path):
    json_path = "test.json"
# 连接到数据库文件
    conn = sqlite3.connect(db_file_path)

    # 创建一个游标对象，用于执行SQL语句
    cursor = conn.cursor()

    """查询数据库并计算歌曲对应rating"""
    cursor.execute('SELECT music_id, score,level,is_all_justice,is_full_combo FROM chusan_user_playlog ORDER BY id DESC LIMIT 30')
    rows = cursor.fetchall()
    rating_list = []
    """定数列表"""
    music_data = load_music_data_from_json(json_path)

    for row in rows:
        music_id, score_max, level, is_all_justice, is_full_combo = row
        """获取定数,曲名，封面地址"""
        difficulty_data, music_name, jacket = get_difficulty_name_value(music_id, music_data)
        difficulte = convert_level_to_difficulty(level)
        constant = difficulty_data.get(difficulte, None)
        """获取单曲rating"""
        rating_value = calculate_rating(constant, score_max)
        rating_list.append(
            {'music_id': music_id, 'score_max': score_max, 'rating': rating_value, 'level': level, 'constant': constant,
             'is_all_justice': is_all_justice, 'is_full_combo': is_full_combo, 'music_name': music_name,
             'jacket': jacket})
        """取rating最高的10首乐曲"""
    sorted_rating_list = sorted(rating_list, key=lambda x: x['rating'], reverse=True)
    recent_10_ratings = sorted_rating_list[:10]
    for item in recent_10_ratings:
        """将 'rating' 对应的值保留两位小数"""
        item['rating'] = round(item['rating'], 2)
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return recent_10_ratings

"""返回rating图片"""
def rank_pic(rating):
    if rating <= 399:
        level = 'green'
    elif rating <= 699:
        level = 'orange'
    elif rating <= 999:
        level = 'red'
    elif rating <= 1199:
        level = 'purple'
    elif rating <= 1324:
        level = 'bronze'
    elif rating <= 1449:
        level = 'silver'
    elif rating <= 1524:
        level = 'gold'
    elif rating <= 1599:
        level = 'platinum'
    else:
        level = 'rainbow'

    # 将输入的整数转换为xx.xx格式的字符串
    rating /= 100
    formatted_number = f"{rating:.2f}"  # 保留两位小数，但不在整数部分填充0

    # 评分图片存储的目录
    rating_dir = 'assets/rating'

    # 分割格式化后的数字为整数部分和小数部分
    integer_part, decimal_part = formatted_number.split('.')

    # 创建列表存储对应的图片文件名
    image_files = []

    # 添加整数部分的数字图片文件名，对于小于10的数字不添加前导零
    for digit in integer_part:
        image_files.append(f'rating_{level}_{int(digit):02d}.png')

    # 添加小数点图片文件名
    image_files.append(f'rating_{level}_comma.png')

    # 添加小数部分的数字图片文件名，确保每个数字都是两位数
    for digit in decimal_part:
        image_files.append(f'rating_{level}_{int(digit):02d}.png')

    # 加载图片并计算总宽度和最大高度
    images = [Image.open(os.path.join(rating_dir, file)).convert("RGBA") for file in image_files]
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)

    # 创建新图像
    result_image = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))

    # 粘贴数字到新图像，确保高度上居中
    current_width = 0
    for i, img in enumerate(images):
        # 通过索引判断当前是否为小数点图片
        if image_files[i].endswith('_comma.png'):
            # 小数点位置稍低
            offset_y = max_height - img.height
        else:
            # 数字居中
            offset_y = (max_height - img.height) // 2
        result_image.paste(img, (current_width, offset_y), img)
        current_width += img.width

    # 返回最终的图片
    return result_image

"""转换角色id字符串形式"""
def parse_chara_id_to_chara_and_trans(chara_id):
    return str(chara_id)[0: len(str(chara_id)) - 1].zfill(4), str(chara_id)[-1].zfill(2)

"""返回角色图片，格式CHU_UI_Character_{chara1}_{chara2}_02.png"""
def find_chara_pic(character_id):
    chara1,chara2=parse_chara_id_to_chara_and_trans(character_id)
    pic_name="CHU_UI_Character_"+chara1+"_"+chara2+"_02.dds"
    A000_dir='F:/SDHD - CHUNITHM SUN PLUS/HDD/data/A000'
    option_dir = 'F:/SDHD - CHUNITHM SUN PLUS/HDD/bin/option'
    """尝试在A000下匹配角色，格式ddsImage016570"""
    chara_dir = os.path.join(A000_dir, 'ddsImage')
    for dir in os.listdir(chara_dir):
        if(dir=="ddsImage0"+str(character_id)):
            chara_pic_dir=os.path.join(chara_dir,dir,pic_name)
            chara_pic=imageio.imread(chara_pic_dir)
            chara_pic=Image.fromarray(chara_pic)
            return chara_pic
    """尝试在opt包中匹配角色"""
    for opt_id in os.listdir(option_dir):
        chara_dir = os.path.join(option_dir, opt_id, 'ddsImage')
        """跳过没有ddsImage文件的opt包"""
        if not os.path.isdir(chara_dir):
            continue
        for dir in os.listdir(chara_dir):
            if (dir == "ddsImage0" + str(character_id)):
                chara_pic_dir = os.path.join(chara_dir, dir, pic_name)
                chara_pic = imageio.imread(chara_pic_dir)
                chara_pic = Image.fromarray(chara_pic)
                return chara_pic

"""返回名牌图片"""
def find_nameplate_pic(nameplate_id):
    nameplate_name="CHU_UI_NamePlate_000"+str(nameplate_id)+".dds"
    A000_dir = 'F:/SDHD - CHUNITHM SUN PLUS/HDD/data/A000'
    option_dir = 'F:/SDHD - CHUNITHM SUN PLUS/HDD/bin/option'
    """尝试在A000下匹配名牌，格式namePlate00025017"""
    nameplate_dir = os.path.join(A000_dir, 'namePlate')
    for dir in os.listdir(nameplate_dir):
        if (dir == "namePlate000" + str(nameplate_id)):
            plate_pic_dir = os.path.join(nameplate_dir, dir, nameplate_name)
            plate_pic = imageio.imread(plate_pic_dir)
            plate_pic = Image.fromarray(plate_pic)
            return plate_pic
    """尝试在opt包中匹配名牌"""
    for opt_id in os.listdir(option_dir):
        nameplate_dir = os.path.join(option_dir, opt_id, 'namePlate')
        """跳过没有namlePlate文件的opt包"""
        if not os.path.isdir(nameplate_dir):
            continue
        for dir in os.listdir(nameplate_dir):
            if (dir == "namePlate000" + str(nameplate_id)):
                plate_pic_dir = os.path.join(nameplate_dir, dir, nameplate_name)
                plate_pic = imageio.imread(plate_pic_dir)
                plate_pic = Image.fromarray(plate_pic)
                return plate_pic

"""返回称号字符串"""
def get_trophy(trophy_id):
    trophy_name = "Trophy.xml"
    A000_dir = 'F:/SDHD - CHUNITHM SUN PLUS/HDD/data/A000'
    option_dir = 'F:/SDHD - CHUNITHM SUN PLUS/HDD/bin/option'
    """尝试在A000下匹配名牌，格式trophy006285"""
    trophy_dir = os.path.join(A000_dir, 'trophy')
    for dir in os.listdir(trophy_dir):
        if (dir == "trophy00" + str(trophy_id)):
            trophy_data_dir = os.path.join(trophy_dir, dir, trophy_name)
            tree = ET.parse(trophy_data_dir)
            root = tree.getroot()
            trophy=root.find("./name/str").text
            rare=root.find('rareType').text
            return trophy,rare
    """尝试在opt包中匹配名牌"""
    for opt_id in os.listdir(option_dir):
        trophy_dir = os.path.join(option_dir, opt_id, 'trophy')
        """跳过没有trophy文件的opt包"""
        if not os.path.isdir(trophy_dir):
            continue
        for dir in os.listdir(trophy_dir):
            if (dir == "trophy00" + str(trophy_id)):
                trophy_data_dir = os.path.join(trophy_dir, dir, trophy_name)
                tree = ET.parse(trophy_data_dir)
                root = tree.getroot()
                trophy = root.find("./name/str").text
                rare = root.find('rareType').text
                return trophy, rare

"""称号稀有度转换"""
def trophy_rarity_to_color(rare):
    rare_mapping = {
        0: "normal",
        1: "bronze",
        2: "silver",
        3: "gold",
        4: "gold",
        5: "platina",
        6: "platina",
        7: "rainbow",
        8: 'ongeki',
        9: 'staff',
        10: 'ongeki'
    }
    return rare_mapping.get(rare, None)
"""返回角色信息图片，角色名-等级-rating-名牌-使用角色-称号"""
def get_user_info_pic(db_file_path):
    pic = Image.open('assets/chu_nameplate.png')
    conn = sqlite3.connect(db_file_path)
    # 创建一个游标对象，用于执行SQL语句
    cursor = conn.cursor()
    """查询数据库导出角色名-等级-rating-名牌-使用角色-称号"""
    cursor.execute(
        'SELECT user_name,level,player_rating,nameplate_id,character_id,trophy_id FROM chusan_user_data')
    rows = cursor.fetchall()
    for row in rows:
        user_name, level, player_rating, nameplate_id, character_id, trophy_id=row
    """绘制rating图片"""
    rank_img=rank_pic(player_rating)
    """获取角色图片"""
    chara_pic=find_chara_pic(character_id)
    """获取名牌图片"""
    nameplate_pic=find_nameplate_pic(nameplate_id)
    """获取称号与稀有度"""
    trophy,rare=get_trophy(trophy_id)
    """粘贴nameplate模板到名牌上"""
    nameplate_pic.paste(pic, (0, 0), pic.split()[3])
    """缩放角色图片并且粘贴到名牌上"""
    chara_pic=chara_pic.resize((82, 82))
    nameplate_pic.paste(chara_pic, (471, 89), chara_pic.split()[3])
    """缩放rating图片并粘贴"""
    rating = rank_img.resize((int(rank_img.size[0] / 1.25), int(rank_img.size[1] / 1.25)))
    nameplate_pic.paste(rating, (222, 147), rating.split()[3])
    """绘制角色名与等级"""
    draw = ImageDraw.Draw(nameplate_pic)
    font_style = ImageFont.truetype("fonts/SourceHanSansCN-Bold.otf", 30)
    draw.text((184, 100), str(level), fill=(0, 0, 0), font=font_style)
    font_style = ImageFont.truetype("fonts/ヒラギノ角ゴ ( Hira Kaku) Pro W6.otf", 30)
    draw.text((228, 107), str(user_name), fill=(0, 0, 0), font=font_style)
    """绘制称号"""
    rare = int(rare)
    rare=trophy_rarity_to_color(rare)
    trophy_pic_dir="assets/trophy/"+rare+".png"
    trophy_pic = Image.open(trophy_pic_dir)
    nameplate_pic.paste(trophy_pic, (145, 46), trophy_pic.split()[3])
    font_style = ImageFont.truetype("fonts/KOZGOPRO-BOLD.OTF", 23)
    left_bound = 157
    right_bound = 547

    # 计算文本大小
    text_width, text_height = draw.textsize(trophy, font=font_style)

    # 确定文本的x坐标和宽度
    if text_width < right_bound - left_bound:
        # 如果文本没有超过边界，则居中显示
        x = left_bound + (right_bound - left_bound - text_width) // 2
        text_to_draw = trophy
    else:
        # 如果文本超过边界，对齐到左边界并截断超出部分
        x = left_bound
        # 计算可以显示的文本长度
        while text_width > right_bound - left_bound:
            trophy_name = trophy_name[:-1]
            text_width, text_height = draw.textsize(trophy_name, font=font_style)
        text_to_draw = trophy_name

    # 绘制文本
    draw.text((x, 54), text_to_draw, fill=(0, 0, 0), font=font_style)
    return nameplate_pic
