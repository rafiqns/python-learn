from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models import Chapter, SubChapter
from forms import ChapterForm, SubChapterForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    chapters = Chapter.query.order_by(Chapter.order).all()
    return render_template('index.html', chapters=chapters)

@main.route('/chapter/<int:chapter_id>')
def chapter_detail(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    subchapters = SubChapter.query.filter_by(chapter_id=chapter_id).order_by(SubChapter.order).all()
    
    # Cek apakah konten pro dan pengguna tidak pro
    if chapter.is_pro and (not current_user.is_authenticated or not current_user.is_pro):
        flash('Konten ini hanya tersedia untuk pengguna Pro', 'warning')
        return render_template('chapter_detail.html', chapter=chapter, subchapters=subchapters, is_pro_content=True)
    
    return render_template('chapter_detail.html', chapter=chapter, subchapters=subchapters, is_pro_content=False)

@main.route('/subchapter/<int:subchapter_id>')
def subchapter_detail(subchapter_id):
    subchapter = SubChapter.query.get_or_404(subchapter_id)
    chapter = Chapter.query.get(subchapter.chapter_id)
    
    # Cek apakah konten pro dan pengguna tidak pro
    if (subchapter.is_pro or chapter.is_pro) and (not current_user.is_authenticated or not current_user.is_pro):
        flash('Konten ini hanya tersedia untuk pengguna Pro', 'warning')
        return render_template('subchapter_detail.html', subchapter=subchapter, chapter=chapter, is_pro_content=True)
    
    return render_template('subchapter_detail.html', subchapter=subchapter, chapter=chapter, is_pro_content=False)

@main.route('/pro')
def pro_info():
    return render_template('pro_info.html') 