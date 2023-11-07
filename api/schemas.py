"""Schemas for Swagger"""
from marshmallow import Schema, fields


class UserLoginSchema(Schema):
    email = fields.Email(load_only=True)
    password = fields.Str(load_only=True)

    class Meta:
        fields = [
            "email",
            "password",
        ]


class UserIDSchema(Schema):
    user = fields.UUID(dump_only=True)

    class Meta:
        fields = [
            "user",
        ]


class UserCreateSchema(Schema):
    name = fields.Str()
    email = fields.Email()

    class Meta:
        fields = [
            "name",
            "email",
        ]


class UserResourceSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    workspace = fields.Str()
    last_login = fields.DateTime()
    is_admin = fields.Bool()
    admin_id = fields.UUID()

    class Meta:
        fields = [
            "name",
            "email",
            "workspace",
            "last_login",
            "is_admin",
            "admin_id"
        ]


class ReportCreateSchema(Schema):
    summary = fields.Str()

    class Meta:
        fields = [
            "summary",
        ]


class ReportResourceSchema(Schema):
    time_generated = fields.DateTime()
    title = fields.Str()
    summary = fields.Str()
    total_tasks = fields.Integer()
    done_tasks = fields.Integer()
    pending_tasks = fields.Integer()
    user_id = fields.UUID()

    class Meta:
        fields = [
            "time_generated",
            "title",
            "summary",
            "total_tasks",
            "done_tasks",
            "pending_tasks",
            "user_id",
        ]


class StepCreateSchema(Schema):
    info = fields.Str()

    class Meta:
        fields = [
            "info",
        ]


class StepResourceSchema(Schema):
    info = fields.Str()
    status = fields.Str(dump_default="in progress")
    task_id = fields.UUID()
    user_id = fields.UUID()

    class Meta:
        fields = [
            "info",
            "status",
            "task_id",
            "user_id",
        ]


class TaskCreateSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    deadline = fields.DateTime()
    steps = fields.List(fields.Str())

    class Meta:
        fields = [
            "title",
            "description",
            "deadline",
            "steps",
        ]


class TaskResourceSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    status = fields.Str(dump_default="in progress")
    deadline = fields.DateTime()
    user_id = fields.UUID()

    class Meta:
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "user_id",
        ]
