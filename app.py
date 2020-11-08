from flask import Flask, render_template, jsonify, json
from playhouse.shortcuts import model_to_dict

from model import PlayList, Video

app = Flask(__name__)


def models_to_dict(models):
    return [model_to_dict(model) for model in models]


@app.route('/')
def hello_world():
    list = PlayList.select()
    return render_template('play_list.html', list=models_to_dict(list))

@app.route("/play/<int:play_id>")
def play(play_id):
    play = PlayList.select().where(PlayList.id == play_id).first()
    videos = Video.select().where(Video.play_list_id == play_id)
    return render_template("play.html", play=play, videos=models_to_dict(videos))

if __name__ == '__main__':
    app.debug = True
    app.run()
