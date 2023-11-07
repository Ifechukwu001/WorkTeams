from flask import abort, jsonify, request
from api.endpoints import api_views
from models import storage
from models.user import User
from models.report import Report
from flask_apispec import use_kwargs, marshal_with, doc
from api import schemas


@api_views.route("/<user_id>/reports", methods=["GET"], strict_slashes=False)
@marshal_with(schemas.ReportResourceSchema(many=True))
@doc(tags=["report"], description="Returns all subordinates reports")
def reports(user_id):
    """Returns all subordinates reports"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    report_json = [[report.to_dict() for report in reports]
                   for reports in Report.compile(user)]
    [report.pop("__class__") for report in report_json]
    return jsonify(report_json)


@api_views.route("/<user_id>/reports/<subordinate_id>", methods=["GET"],
                 strict_slashes=False)
@marshal_with(schemas.ReportResourceSchema(many=True))
@doc(tags=["report"], description="Returns a single subordinate's reports")
def sub_reports(user_id, subordinate_id):
    """Returns a single subordinate's reports"""
    user = storage.get(User, user_id)
    subordinate = storage.get(User, subordinate_id)
    if not user or not subordinate:
        abort(404)
    report_json = [[report.to_dict() for report in reports]
                   for reports in Report.compile(user, subordinate)]
    [report.pop("__class__") for report in report_json]
    return jsonify(report_json)


@api_views.route("/<user_id>/reports", methods=["POST"], strict_slashes=False)
@use_kwargs(schemas.ReportCreateSchema)
@marshal_with(None, code=201)
@doc(tags=["report"], description="Creates a new report for a user")
def create_report(user_id, **kwargs):
    """Creates a new report for a user"""
    if request.content_type != "application/json":
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "summary" not in data:
        data["summary"] = ""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.create_report(summary=data["summary"])
    return jsonify({}), 201
