from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models import User, Chapter, SubChapter, Payment
from forms import ChapterForm, SubChapterForm
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    users_count = User.query.count()
    chapters_count = Chapter.query.count()
    subchapters_count = SubChapter.query.count()
    pro_users_count = User.query.filter_by(is_pro=True).count()
    
    return render_template('admin/dashboard.html', 
                          users_count=users_count,
                          chapters_count=chapters_count,
                          subchapters_count=subchapters_count,
                          pro_users_count=pro_users_count)

@admin.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/admin/chapters')
@login_required
@admin_required
def admin_chapters():
    chapters = Chapter.query.order_by(Chapter.order).all()
    return render_template('admin/chapters.html', chapters=chapters)

@admin.route('/admin/chapter/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_chapter():
    form = ChapterForm()
    if form.validate_on_submit():
        chapter = Chapter(
            title=form.title.data,
            description=form.description.data,
            order=form.order.data,
            is_pro=form.is_pro.data
        )
        db.session.add(chapter)
        db.session.commit()
        flash('Bab baru berhasil dibuat!', 'success')
        return redirect(url_for('admin.admin_chapters'))
    return render_template('admin/chapter_form.html', form=form, title='Buat Bab Baru')

@admin.route('/admin/chapter/<int:chapter_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    form = ChapterForm()
    
    if form.validate_on_submit():
        chapter.title = form.title.data
        chapter.description = form.description.data
        chapter.order = form.order.data
        chapter.is_pro = form.is_pro.data
        db.session.commit()
        flash('Bab berhasil diperbarui!', 'success')
        return redirect(url_for('admin.admin_chapters'))
    
    elif request.method == 'GET':
        form.title.data = chapter.title
        form.description.data = chapter.description
        form.order.data = chapter.order
        form.is_pro.data = chapter.is_pro
    
    return render_template('admin/chapter_form.html', form=form, title='Edit Bab')

@admin.route('/admin/chapter/<int:chapter_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Bab berhasil dihapus!', 'success')
    return redirect(url_for('admin.admin_chapters'))

@admin.route('/admin/subchapters/<int:chapter_id>')
@login_required
@admin_required
def admin_subchapters(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    subchapters = SubChapter.query.filter_by(chapter_id=chapter_id).order_by(SubChapter.order).all()
    return render_template('admin/subchapters.html', chapter=chapter, subchapters=subchapters)

@admin.route('/admin/subchapter/new/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def new_subchapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    form = SubChapterForm()
    
    if form.validate_on_submit():
        subchapter = SubChapter(
            chapter_id=chapter_id,
            title=form.title.data,
            content=form.content.data,
            order=form.order.data,
            is_pro=form.is_pro.data
        )
        db.session.add(subchapter)
        db.session.commit()
        flash('Sub-bab baru berhasil dibuat!', 'success')
        return redirect(url_for('admin.admin_subchapters', chapter_id=chapter_id))
    
    return render_template('admin/subchapter_form.html', form=form, chapter=chapter, title='Buat Sub-Bab Baru')

@admin.route('/admin/subchapter/<int:subchapter_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_subchapter(subchapter_id):
    subchapter = SubChapter.query.get_or_404(subchapter_id)
    form = SubChapterForm()
    
    if form.validate_on_submit():
        subchapter.title = form.title.data
        subchapter.content = form.content.data
        subchapter.order = form.order.data
        subchapter.is_pro = form.is_pro.data
        db.session.commit()
        flash('Sub-bab berhasil diperbarui!', 'success')
        return redirect(url_for('admin.admin_subchapters', chapter_id=subchapter.chapter_id))
    
    elif request.method == 'GET':
        form.title.data = subchapter.title
        form.content.data = subchapter.content
        form.order.data = subchapter.order
        form.is_pro.data = subchapter.is_pro
    
    return render_template('admin/subchapter_form.html', form=form, chapter=subchapter.chapter, title='Edit Sub-Bab')

@admin.route('/admin/subchapter/<int:subchapter_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_subchapter(subchapter_id):
    subchapter = SubChapter.query.get_or_404(subchapter_id)
    chapter_id = subchapter.chapter_id
    db.session.delete(subchapter)
    db.session.commit()
    flash('Sub-bab berhasil dihapus!', 'success')
    return redirect(url_for('admin.admin_subchapters', chapter_id=chapter_id))

@admin.route('/admin/payments')
@login_required
@admin_required
def admin_payments():
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('admin/payments.html', payments=payments) 