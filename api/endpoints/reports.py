from flask import abort, jsonify, request
from api.endpoints import api_views
from models import storage
from models.user import User
from models.report import Report

@api_views.route("/<user_id>/reports", strict_slashes=False)
def reports(user_id):
    """Returns all subordinates reports"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    report_json = [[report.to_dict() for report in reports] for reports in Report.compile(user)]
    return jsonify(report_json)

@api_views.route("/<user_id>/reports/<subordinate_id>", strict_slashes=False)
def sub_reports(user_id, subordinate_id):
    """Returns a single subordinate's reports"""
    user = storage.get(User, user_id)
    subordinate = storage.get(User, subordinate_id)
    if not user or not subordinate:
        abort(404)
    report_json = [[report.to_dict() for report in reports] for reports in Report.compile(user, subordinate)]
    return jsonify(report_json)

@api_views.route("/<user_id>/reports", methods=["POST"], strict_slashes=False)
def create_report(user_id):
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
    return jsonify({})
