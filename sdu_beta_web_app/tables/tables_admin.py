# Python imports
import itertools
# Django imports
from sdu_beta_web_app.models import *
import django_tables2 as tables
from django_tables2.utils import A


class StaffsTable(tables.Table):
    row_number = tables.Column(verbose_name='#', empty_values=())
    edit = tables.Column(empty_values=(),
                         linkify=('edit_staff', [A('staff.id')]), attrs={'a': {"class": "btn btn-outline-info"}}, orderable=False)
    delete = tables.Column(empty_values=(),
                           linkify=('delete_staff', [A('staff.id')]), attrs={'a': {"class": "btn btn-outline-danger"}}, orderable=False)
    # action = tables.TemplateColumn(
    #     template_name="tables_template/test.html", extra_context={'id': A('staff.id')})

    class Meta:
        model = Staffs
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('row_number', 'staff', 'staff.username', 'staff.email',
                  'gender', 'adress', 'display_image')
        order_by = ('staff',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return str(next(self.counter)+1) + '.'

    def render_edit(self):
        return 'Edit'

    def render_delete(self):
        return 'Delete'
