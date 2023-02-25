from flask import send_from_directory, jsonify
from baseapp import app, api
from model.models import db
from flask_rest_paginate import Pagination
from api.report_resource import ReportListApi, ReportUploadApi, ReportDelApi
from base.api import account_resource

upload_folder = './'  # 上传文件需要保存的目录
allowed_extensions = ['pdf', 'docx']  # 允许上传的文件格式
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 上传文件的最大值

with app.app_context():
    db.create_all()


@app.route('/<filename>')
def show_upload_file(filename):
    """
    显示上传的文件并下载
    :param filename: 上传文件名称
    :return: 下载文件
    """
    download_path = './'
    return send_from_directory(download_path, filename)  # as_attachment=True可以实现下载


# 业务 api
api.add_resource(ReportUploadApi, '/api/v1/upload')
api.add_resource(ReportListApi, '/api/v1/upload/list')
api.add_resource(ReportDelApi, '/api/v1/delpdf/<int:upload_id>')

# 账号 api
api.add_resource(account_resource.PeopleApi, '/api/v1/profile')
api.add_resource(account_resource.LoginApi, '/api/v1/sign_in')
api.add_resource(account_resource.RegisterApi, '/api/v1/sign_up')

pagination = Pagination(app, db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6016, debug=True)
