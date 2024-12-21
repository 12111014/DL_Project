import json

from flask import Flask, request, send_file, render_template, jsonify
from matplotlib import pyplot as plt
from markupsafe import Markup
import pandas as pd
import os

from db_model import db, ImageInfo
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:liby2003@localhost:5432/imageinfosys'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


# # 创建一个文件夹来保存上传的图像
# UPLOAD_FOLDER = './uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# 主页面
@app.route("/")
def index():
    return render_template("index.html")

# 图像展示页面
@app.route("/image_show")
def image_show():
    image_path = request.args.get("image_path")
    return render_template("image_show.html", image_path=image_path)

@app.route("/upload_image_data", methods=["POST"])
def upload_image_data():
    # 获取 JSON 数据
    data = request.form.to_dict()
    # 保存图片信息
    print(data)
    st = datetime.now()
    image_info = ImageInfo(group_id=data["group_id"],
                           group_index=data["group_index"],
                           start_time=data["start_time"] if "start_time" in data else st,
                           type=data["type"])
    db.session.add(image_info)
    db.session.commit()
    return "Image uploaded successfully!"

def find_unique_group_id():
    max_group_id = db.session.query(db.func.max(ImageInfo.group_id)).scalar()
    if max_group_id is None:
        return 0
    else:
        return max_group_id + 1

@app.route("/upload_group_image_data", methods=["POST"])
def upload_group_image_data():
    # 确认请求中有 JSON 数据
    if request.is_json:
        # 获取 JSON 数据
        data = request.get_json()
        data = json.loads(data)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and {'group_index', 'type', 'start_time'} <= item.keys():
                    try:
                        item['start_time'] = datetime.strptime(item['start_time'], '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        return jsonify({"error": "Invalid date format"}), 400
                else:
                    return jsonify({"error": "Invalid data format"}), 400
            group_id = str(find_unique_group_id())
            for item in data:
                image_info = ImageInfo(group_id=group_id,
                                       group_index=item["group_index"],
                                       start_time=item["start_time"],
                                       type=item["type"])
                db.session.add(image_info)
            db.session.commit()
            return jsonify({"message": "Data received successfully", "data": data}), 200
        else:
            return jsonify({"error": "Expected a list of dictionaries"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400

# 数据可视化页面
@app.route("/image_data_timeline")
def data_visualize_timeline():
    data = ImageInfo.query.all()
    datas = [{"group_id": item.group_id,
             "group_index": item.group_index,
             "start_time": str(item.start_time),
             "type": item.type} for item in data]
    datas_json = json.dumps(datas)
    print(datas_json)
    return render_template("image_data_timeline.html", data=Markup(datas_json))

@app.route("/image_data_pie")
def data_visualize_pie():
    data = ImageInfo.query.all()
    datas = [{"group_id": item.group_id,
             "group_index": item.group_index,
             "start_time": str(item.start_time),
             "type": item.type} for item in data]
    datas_json = json.dumps(datas)
    print(datas_json)
    return render_template("image_data_pie.html", data=Markup(datas_json))




# 接受模型输出的图像结果
@app.route("/upload_image", methods=["POST"])
def upload_image():
    image_file = request.files["image"]
    image_path = os.path.join("static/images", image_file.filename)
    image_file.save(image_path)
    return "Image uploaded successfully!"


if __name__ == '__main__':
    app.run(debug=True, port=8083)