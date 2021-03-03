import logging

from flask_login import current_user
from wtforms import Form, ValidationError

from overhave import db
from overhave.admin.views.base import ModelViewConfigured

logger = logging.getLogger(__name__)


class TagsView(ModelViewConfigured):
    """ View for :class:`Feature` table. """

    can_view_details = False

    column_list = (
        "id",
        "value",
        "created_at",
        "created_by",
    )

    form_excluded_columns = "created_at"

    def on_model_change(self, form: Form, model: db.Tags, is_created: bool) -> None:
        if not is_created and current_user.role != db.Role.admin:
            raise ValidationError("Only administrator could change test run data!")
        model.created_by = current_user.login

    def on_model_delete(self, model: Form) -> None:
        if not (current_user.login == model.created_by or current_user.role == db.Role.admin):
            raise ValidationError("Only feature author or administrator could delete feature!")
