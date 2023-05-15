from flask import Blueprint, redirect, render_template, session, request, flash, url_for
from ..registration.models import account as accountdata
from .. import db, auth
from flask_login import login_user, login_required, current_user
from .models import group as groupdata
from ..account.models import trainer
from ..students.models import students
from .forms import GroupForm1, GroupForm2, GroupForm3

groups = Blueprint('groups', __name__, template_folder='templates', static_folder='static')


@groups.route("/group", methods=['GET', 'POST'])
@login_required
def group():
    groups = db.session.query(groupdata.group_name, accountdata.account_id, accountdata.account_surname,
                              accountdata.account_name, db.func.count(students.student_id), groupdata.group_id) \
        .join(trainer, groupdata.group_trainer_id == trainer.trainer_id) \
        .join(accountdata, trainer.trainer_id == accountdata.account_trainer_id) \
        .outerjoin(students, groupdata.group_id == students.student_group_id) \
        .group_by(groupdata.group_name, accountdata.account_id, accountdata.account_surname,
                  accountdata.account_name, groupdata.group_id) \
        .all()

    return render_template('groups/groups.html', groups=groups, cu=current_user.get_id())


@groups.route("/group/<int:group_id>", methods=['GET', 'POST'])
@login_required
def singlegroup(group_id):
    gr = groupdata.query.get(group_id)
    grinf = db.session.query(groupdata.group_name, accountdata.account_id, accountdata.account_surname,
                             accountdata.account_name, accountdata.account_patronymic) \
        .join(trainer, groupdata.group_trainer_id == trainer.trainer_id) \
        .join(accountdata, trainer.trainer_id == accountdata.account_trainer_id) \
        .filter(groupdata.group_id == group_id) \
        .all()
    sts = db.session.query(accountdata.account_id, accountdata.account_surname, accountdata.account_name,
                           accountdata.account_patronymic, students.student_id). \
        join(students, accountdata.account_student_id == students.student_id). \
        join(groupdata, students.student_group_id == groupdata.group_id) \
        .filter(groupdata.group_id == group_id) \
        .all()

    num_students = db.session.query(students.student_id) \
        .join(groupdata, groupdata.group_id == students.student_group_id) \
        .filter(groupdata.group_id == group_id) \
        .count()
    return render_template('groups/group.html', group=gr, grinf=grinf, students=sts, num_students=num_students,
                           cu=current_user.get_id())


@groups.route("/group_add", methods=['GET', 'POST'])
@login_required
def group_add():
    form = GroupForm1()

    if form.validate_on_submit():
        g = groupdata(
            group_name=form.group_name.data,
            group_trainer_id=form.group_trainer.data,
        )

        db.session.add(g)
        db.session.commit()

        selected_students = form.group_students.data
        for account_id in selected_students:
            acc = accountdata.query.filter_by(account_id=account_id).first()
            if acc:
                student = students.query.filter(students.student_id == acc.account_student_id).first()
                if student:
                    student.student_group_id = g.group_id

        db.session.commit()

        flash('Группа успешно создана', 'success')
        return redirect("group")

    return render_template('groups/group_add.html', form=form, cu=current_user.get_id())


@groups.route("/group_edit/<int:group_id>", methods=['GET', 'POST'])
@login_required
def group_edit(group_id):
    gp = groupdata.query.get_or_404(group_id)
    form = GroupForm2(obj=groupdata.query.get_or_404(group_id))

    if form.validate_on_submit():
        form.populate_obj(groupdata.query.get_or_404(group_id))
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
    sts_gp = groupdata.query.get_or_404(group_id)
    form = GroupForm3()

    if form.validate_on_submit():
        selected_students = form.students.data
        for account_id in selected_students:
            acc = accountdata.query.filter_by(account_id=account_id).first()
            if acc:
                student = students.query.filter(students.student_id == acc.account_student_id).first()
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
    st_group = groupdata.query.get_or_404(group_id)
    student = students.query.get_or_404(student_id)

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
    group_del = groupdata.query.get_or_404(group_id)

    db.session.delete(group_del)
    db.session.commit()

    flash('Группа успешно удалена', 'success')

    return redirect(url_for('groups.group', cu=current_user.get_id()))
