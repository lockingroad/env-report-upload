from model.models import db, ReportUploadModel


class ReportUploadModelDao():
    def updateCreateUploadModel(self, pdf_origin_name, pdf_name, pdf_number):
        modified_model = ReportUploadModel.query.filter(
            (ReportUploadModel.pdf_number == pdf_number)).first()
        if not modified_model:
            modified_model = ReportUploadModel(pdf_name=pdf_name, pdf_origin_name=pdf_origin_name,
                                               pdf_number=pdf_number)
            db.session.add(modified_model)
        else:
            modified_model.pdf_origin_name = pdf_origin_name
            modified_model.pdf_name = pdf_name
        db.session.commit()
        return modified_model

    def deleteUploadModel(self, id):
        uploadModel = ReportUploadModel.query.get(id)
        db.session.delete(uploadModel)
        db.session.commit()
        return uploadModel
