from flask_restful import Api, fields, Resource, marshal_with, marshal, reqparse, request
from baseapp import pagination, app
from model.models import ReportUploadModel
from flask import flash, jsonify
import os
import uuid
from controlers import ReportUploadModelDao
from base.common import login_required, verify_token

parser = reqparse.RequestParser()
parser.add_argument('num', type=str, required=False, location='args')

upload_fields = {
    'id': fields.Integer,
    'pdf_name': fields.String,
    'pdf_number': fields.String,
    'pdf_origin_name': fields.String
}

allowed_extensions = ['pdf', 'docx']  # 允许上传的文件格式


# pdf 文件列表
class ReportListApi(Resource):
    def get(self):
        args = parser.parse_args()
        arg_num = args['num']
        if arg_num:
            lookfor = gen_lookfor(arg_num)
            return pagination.paginate(ReportUploadModel.query.filter(ReportUploadModel.pdf_number.ilike(lookfor)),
                                       upload_fields)
        else:
            return pagination.paginate(ReportUploadModel,
                                       upload_fields)


def gen_lookfor(needle):
    if '*' in needle or '_' in needle:
        looking_for = needle.replace('_', '__') \
            .replace('*', '%') \
            .replace('?', '_')
    else:
        looking_for = '%{0}%'.format(needle)
    return looking_for


# pdf 上传
class ReportUploadApi(Resource):
    method_decorators = {'post': [login_required]}

    def post(self):
        if 'file' not in request.files:
            print('Please Select File')
            return jsonify(success=False, msg="arg error1")
        f = request.files['file']
        if not allowed_file(f.filename):
            print('Please Select Correct File')
            return jsonify(success=False, msg="arg error2")
        if 'number' not in request.form:
            return jsonify(success=False, msg="arg error3")
        arg_number = request.form['number']
        suffix_name = os.path.splitext(f.filename)[-1][1:]
        gen_file_name = "{}_{}.{}".format(arg_number, uuid.uuid1().hex, suffix_name)
        if f and allowed_file(f.filename):
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], gen_file_name)
            ReportUploadModelDao().updateCreateUploadModel(pdf_name=gen_file_name, pdf_origin_name=f.filename,
                                                           pdf_number=arg_number)
            f.save(save_path)
            return jsonify(success=True, msg="upload pdf success")


def allowed_file(filename):
    """
    上传文件的格式要求
    :param filename:文件名称
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.')[1].lower() in allowed_extensions


# pdf 删除
class ReportDelApi(Resource):
    method_decorators = {'put': [login_required]}

    def put(self, upload_id):
        model = ReportUploadModelDao().deleteUploadModel(upload_id)
        if model:
            return jsonify(success=True, msg="delete pdf success")
        else:
            return jsonify(success=False, msg="delete pdf fail")
