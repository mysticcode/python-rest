from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # def __repr__(self):
    #     return f"Video(name ={name})"


# db.create_all()

names = {"tim": {"age": 10, "gender": "male"},
         "b": {"age": 10, "gender": "male"}
         }

video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="name of video is required", required=True)
video_put_args.add_argument(
    "views", type=int, help="views of video is optional")
video_put_args.add_argument(
    "likes", type=int, help="likes of video is optional")

videos = {}


def abort_if_not_exist(video_id):
    if video_id not in videos:
        abort(404, message="video id not found")


def abort_if_video_exist(video_id):
    if video_id in videos:
        abort(409, message="video already exisits with that ID")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        # abort_if_not_exist(video_id)
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="video not avialble")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        # request.form["likes"]
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video id not avialble")
        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        # print(args)
        # abort_if_video_exist(video_id)
        # videos[video_id] = args
        return video, 201

    def delete(self, video_id):
        abort_if_not_exist(video_id)
        del videos[video_id]
        return '', 204


api.add_resource(Video, "/video/<int:video_id>")


class HelloWorld(Resource):
    def get(self, name, test):
        # return {"data": name, "param2": test}
        return names[name]

    def post(self):
        return {"data": "Hellow post"}


api.add_resource(HelloWorld, "/hellow/<string:name>/<int:test>")

if __name__ == "__main__":
    app.run(debug=True)
