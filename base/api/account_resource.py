from model.models import UserModel, db
from flask_restful import Api, fields, Resource, marshal_with
from flask import request, jsonify
from base.common import login_required, verify_token, create_token
import re
from sqlalchemy import exists

"""
Resource fields for marshalling
"""
people_fields = {
    'name': fields.String,
    'phone': fields.String,
    'id': fields.Integer
}


class PeopleTestApi(Resource):
    @marshal_with(people_fields)
    def get(self, people_id):
        return UserModel.query.filter_by(id=people_id).first()

    def post(self, people_id):
        request_dic = request.json
        print(request_dic)
        return request_dic


class PeopleApi(Resource):
    method_decorators = {'get': [login_required]}

    @marshal_with(people_fields)
    def get(self):
        token = request.headers["z-token"]
        # 拿到token，去换取用户信息
        user_id = verify_token(token)
        user = UserModel.query.get(user_id)
        return user


class LoginApi(Resource):

    def post(self):
        res_dir = request.json

        if res_dir is None:
            # 这里的code，依然推荐用一个文件管理状态
            return jsonify(code=4103, msg="未接收到参数")

        # 获取前端传过来的参数
        phone = res_dir.get("phone")
        password = res_dir.get("pwd")

        # 校验参数
        if not all([phone, password]):
            return jsonify(code=4103, msg="请填写手机号或密码")

        if not re.match(r"1[23456789]\d{9}", phone):
            return jsonify(code=4103, msg="手机号有误")

        try:
            user = UserModel.query.filter_by(phone=phone).first()
        except Exception:
            return jsonify(code=4004, msg="获取信息失败")

        if user is None or user.pwd != password:
            return jsonify(code=4103, msg="手机号或密码错误")

        # 获取用户id，传入生成token的方法，并接收返回的token
        token = create_token(user.id)

        # 把token返回给前端
        return jsonify(code=0, msg="成功", data=token)


class RegisterApi(Resource):

    def post(self):
        res_dir = request.json

        if res_dir is None:
            # 这里的code，依然推荐用一个文件管理状态
            return jsonify(code=4103, msg="未接收到参数")

        # 获取前端传过来的参数
        arg_phone = res_dir.get("phone")
        arg_password = res_dir.get("pwd")

        # 校验参数
        if not all([arg_phone, arg_password]):
            return jsonify(code=4103, msg="请填写手机号或密码")

        if not re.match(r"1[23456789]\d{9}", arg_phone):
            return jsonify(code=4103, msg="手机号有误")

        try:
            account_exists = db.session.query(exists().where(UserModel.phone == arg_phone)).scalar()
            if account_exists:
                return jsonify(code=4103, msg="手机号已经被注册")
            else:
                new_user = UserModel(phone=arg_phone, pwd=arg_password)
                db.session.add(new_user)
                db.session.commit()
        except Exception:
            return jsonify(code=4004, msg="获取信息失败")

        return jsonify(code=0, msg="Registration successful")
