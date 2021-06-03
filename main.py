# coding=utf-8
# coding=gbk
import base64
import io
import sys

import synonyms
from flask import request, jsonify, render_template, Flask
from wordcloud import WordCloud

app = Flask(__name__,
            template_folder="./frontend",
            static_folder="./frontend/static")


# 真正调用词云库生成图片
def get_word_cloud(dic):
    font = "./pingfang.ttf"
    # pil_img = WordCloud(width=500, height=500, font_path=font).generate(text=text).to_image()

    pil_img = WordCloud(width=800, height=300, background_color="white", font_path=font,
                        prefer_horizontal=1.0).generate_from_frequencies(
        dic).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return img_base64


@app.route('/words', methods=["GET"])
def resp():
    """获取近义词"""
    char = request.args.get("char")
    size = request.args.get("size")
    if not size:
        size = 10
    result = synonyms.nearby(char, int(size))
    dic = []
    for i, v in enumerate(result[0]):
        d = {"word": v, "score": str(result[1][i])}
        dic.append(d)
    return jsonify(dic)


@app.route('/word/cloud/generate', methods=["POST"])
def cloud():
    """生成词云图片接口，以base64格式返回"""
    text = request.json.get("word")
    result = synonyms.nearby(text, 20)
    dic = dict(zip(result[0], result[1]))
    res = get_word_cloud(dic)
    return res


@app.route('/')
@app.route('/index')
def index():
    """主页面"""
    return render_template('index.html')


if __name__ == '__main__':
    port = 1234
    argv = sys.argv
    if len(argv) > 1:
        port = int(argv[1])
    # app.debug = True
    app.run(host='0.0.0.0', port=port)
