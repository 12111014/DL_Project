import json

from flask import Flask, request, send_file, render_template
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
    save_data(data)
    return "Image uploaded successfully!"


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


# 保存数据
def save_data(data):
    print(data)
    st = datetime.now()
    image_info = ImageInfo(group_id=data["group_id"],
                           group_index=data["group_index"],
                           start_time=st,
                           type=data["type"])
    db.session.add(image_info)
    db.session.commit()



# 接受模型输出的图像结果
@app.route("/upload_image", methods=["POST"])
def upload_image():
    image_file = request.files["image"]
    image_path = os.path.join("static/images", image_file.filename)
    image_file.save(image_path)
    return "Image uploaded successfully!"


if __name__ == '__main__':
    app.run(debug=True, port=8083)