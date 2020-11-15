import requests
from flask import Blueprint

api_bp = Blueprint('api', __name__)



@api_bp.route('/get_page_by_mid/<mid>')
def get_page_by_mid(mid):
    url = "https://api.bilibili.com/x/space/arc/search?mid="+mid
    response = requests.get(url).json()
    return response
    # return render_template('play_list.html', list=models_to_dict(PlayList.select()))

