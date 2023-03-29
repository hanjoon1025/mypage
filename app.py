from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from pymongo import MongoClient
import certifi
from bson.objectid import ObjectId

db = client.dbsparta

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/toon' )
def review():    
    return render_template('toon.html')

##################################################################
@app.route("/review:commentid", methods=["POST"])
def comment_del():

    del_pw = request.form['pw_give']
    del_id = request.form['commentid_give']

    # print(del_id)   
    # print(del_pw) 
    find_one = db.comment.find_one({'_id': ObjectId(del_id),'pw':del_pw})  #comment 이름의 DB에서 Id, pw값일치하는 것 찾기

    # print(find_one) 

    if (None != find_one):    #Id값과 pw 확인하여 하나라도 다르면 None이 출력. -> else문으로.           
        db.comment.delete_one({'_id': ObjectId(del_id),'pw':del_pw})  
        return jsonify({'msg':'삭제완료'})
    else:        
        return jsonify({'msg':'pw가 일치하지 않습니다.'})    
####################메인화면 시작하면 보내는 GET#####################################

@app.route("/webtoon", methods=["GET"])
def webtoon_get():
    toon_lists = list(db.toons.find({}))      #toon 이란 이름의 DB에 저장된 것들 메인페이지로
    for mv in toon_lists:
        mv["_id"] = str(mv["_id"])  #이렇게 하니 id 값도 넘어감
    return jsonify({'result':toon_lists})
#########################################################################

@app.route("/tooncomment", methods=["GET"])
def tooncomment_get():
    tooncommnet_list = db.toons.find_one({'name':'bobby'})

    # toon_lists = list(db.toons.find({}))      #toon 이란 이름의 DB에 저장된 것들 메인페이지로
    # for mv in toon_lists:
    #     mv["_id"] = str(mv["_id"])  #이렇게 하니 id 값도 넘어감
    # return jsonify({'result':tooncommnet_list})

@app.route("/toonrender", methods=["POST"])
def toon_get():
    objectId = request.form['objectId_give']
    toon = db.toons.find_one({'_id':ObjectId(objectId) } )
    print(toon)
    return jsonify({'result':toon})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
    
