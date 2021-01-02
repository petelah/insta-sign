from flask import Blueprint, render_template, redirect, url_for, jsonify, make_response
from flask_login import current_user, login_required
from src.models import Business, SignIn
from src.services import dump_db
from src import db

admin_view = Blueprint('admin_view', __name__, url_prefix="/")


@admin_view.route('/admin', methods=['GET', "POST"])
@login_required
def root():
	"""
	Root admin directory, displays business stats and allows admin to verify
	businesses.
	:return: render_template object
	"""
	if not current_user.admin:
		return redirect(url_for('main_view.root'))
	unverified_businesses = Business.query.filter_by(verified=False).all()
	sign_in_count = SignIn.query.count()
	return render_template('admin.html', businesses=unverified_businesses, sc=sign_in_count)


@admin_view.route('/admin/approve/<string:business_name>', methods=["GET", "POST"])
@login_required
def approve(business_name):
	"""
	Approve business function so a business can take sign in's
	:param business_name:
	:return: render_template object
	"""
	if not current_user.admin:
		return redirect(url_for('main_view.root'))
	business = Business.query.filter_by(business_name=business_name).first_or_404()
	business.verified = True
	db.session.commit()
	return redirect(url_for('admin_view.root'))


@admin_view.route('/admin/dump_db', methods=["GET", "POST"])
@login_required
def dump():
	"""
	Dumps a backup of the database to JSON.
	:return:
	"""
	if not current_user.admin:
		return redirect(url_for('main_view.root'))
	db_dump = dump_db()
	return db_dump, 200
