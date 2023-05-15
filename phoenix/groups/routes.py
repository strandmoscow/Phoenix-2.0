from flask import Blueprint, redirect, render_template, session, request, flash, url_for

from .. import db, auth
from ..registration.models import Account
from flask_login import login_user, login_required, current_user
from .models import Group
from ..account.models import Trainer
from ..student.models import Students
from .forms import GroupForm1, GroupForm2, GroupForm3

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

    print(sts)
    return render_template('groups/group.html', group=gr, grinf=grinf, students=sts, num_students=len(sts),
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


@groups.route("/group_edit/<int:group_id>", methods=['GET', 'POST'])
@login_required
def group_edit(group_id):
    gp = Group.query.get_or_404(group_id)
    form = GroupForm2(obj=Group.query.get_or_404(group_id))

    if form.validate_on_submit():
        form.populate_obj(Group.query.get_or_404(group_id))
        gp.group_trainer_id = form.group_trainer.data
        db.session.commit()
        flash('Информация о группе успешно обновлена', 'success')
        return redirect(url_for('groups.singlegroup', group_id=group_id))

    # Установить выбранное значение для поля group_trainer
    form.group_trainer.data = gp.group_trainer_id

    return render_template('groups/group_edit.html', form=form, cu=current_user.get_id())


@groups.route("/add_students/<int:group_id>", methods=['GET', 'POST'])
@login_required
def add_students(group_id):
    sts_gp = Group.query.get_or_404(group_id)
    form = GroupForm3()

    if form.validate_on_submit():
        selected_students = form.students.data
        for account_id in selected_students:
            acc = Account.query.filter_by(account_id=account_id).first()
            if acc:
                student = Students.query.filter(Students.student_id == acc.account_student_id).first()
                if student:
                    student.student_group_id = group_id

        db.session.commit()

        flash('Студенты успешно добавлены в группу', 'success')
        return redirect(url_for('groups.singlegroup', group_id=group_id))

    return render_template('groups/add_students.html', group=sts_gp, form=form,
                           cu=current_user.get_id())


@groups.route("/remove_student/<int:group_id>/<int:student_id>", methods=['GET', 'POST'])
@login_required
def remove_student(group_id, student_id):
    st_group = Group.query.get_or_404(group_id)
    student = Students.query.get_or_404(student_id)

    if student.student_group_id == group_id:
        student.student_group_id = None
        db.session.commit()
        flash('Студент успешно удален из группы', 'success')
    else:
        flash('Студент не состоит в данной группе', 'error')

    return redirect(url_for('groups.singlegroup', group_id=group_id))


@groups.route("/remove_group/<int:group_id>", methods=['GET', 'POST'])
@login_required
def remove_group(group_id):
    group_del = Group.query.get_or_404(group_id)

    db.session.delete(group_del)
    db.session.commit()

    flash('Группа успешно удалена', 'success')

    return redirect(url_for('groups.group', cu=current_user.get_id()))
