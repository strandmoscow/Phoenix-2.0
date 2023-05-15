from flask import Blueprint, redirect, render_template, session, request, flash
from ..registration.models import Account
from .. import db, auth
from flask_login import login_user, login_required, current_user
from .models import Group
from ..account.models import Trainer
from ..students.models import Students
from .forms import GroupForm1

groups = Blueprint('groups', __name__, template_folder='templates', static_folder='static')


@groups.route("/", methods=['GET', 'POST'])
@login_required
def group():
    groups = db.session.query(Group.group_name, Account.account_id, Account.account_surname,
                              Account.account_name, db.func.count(Students.student_id), Group.group_id) \
        .join(Trainer, Group.group_trainer_id == Trainer.trainer_id) \
        .join(Account, Trainer.trainer_id == Account.account_trainer_id) \
        .outerjoin(Students, Group.group_id == Students.student_group_id) \
        .group_by(Group.group_name, Account.account_id, Account.account_surname,
                  Account.account_name, Group.group_id) \
        .all()

    return render_template('groups/groups.html', groups=groups, cu=current_user.get_id())


@groups.route("/<int:group_id>", methods=['GET', 'POST'])
@login_required
def singlegroup(group_id):
    gr = Group.query.get(group_id)
    grinf = db.session.query(Group.group_name, Account.account_id, Account.account_surname,
                             Account.account_name, Account.account_patronymic) \
        .join(Trainer, Group.group_trainer_id == Trainer.trainer_id) \
        .join(Account, Trainer.trainer_id == Account.account_trainer_id) \
        .filter(Group.group_id == group_id) \
        .all()
    sts = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                           Account.account_patronymic). \
        join(Students, Account.account_student_id == Students.student_id). \
        join(Group, Students.student_group_id == Group.group_id) \
        .filter(Group.group_id == group_id) \
        .all()

    num_students = db.session.query(Students.student_id) \
        .join(Group, Group.group_id == Students.student_group_id) \
        .filter(Group.group_id == group_id) \
        .count()
    return render_template('groups/group.html', group=gr, grinf=grinf, Students=sts, num_students=num_students,
                           cu=current_user.get_id())


@groups.route("/group_add", methods=['GET', 'POST'])
@login_required
def group_add():
    form = GroupForm1()

    if form.validate_on_submit():
        g = Group(
            group_name=form.group_name.data,
            group_trainer_id=form.group_trainer.data,
        )

        db.session.add(g)
        db.session.commit()

        selected_students = form.group_students.data
        for account_id in selected_students:
            acc = Account.query.filter_by(account_id=account_id).first()
            if acc:
                student = Students.query.filter(Students.student_id == acc.account_student_id).first()
                if student:
                    student.student_group_id = g.group_id

        db.session.commit()

        flash('Группа успешно создана', 'success')
        return redirect("group")

    return render_template('groups/group_add.html', form=form, cu=current_user.get_id())
