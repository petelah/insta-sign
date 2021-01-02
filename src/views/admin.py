from flask import Blueprint, request, abort, render_template, redirect, url_for
from flask_login import current_user, login_required
from src.models import Business, SignIn
from src import db
from src.services import new_post_svc, single_post_svc, get_user_by_username, add_comment_svc, save_profile_settings_svc, sign_in_svc, delete_post_svc, business_register_svc

admin_view = Blueprint('admin_view', __name__, url_prefix="/")


@admin_view.route('/admin', methods=['GET', "POST"])
@login_required
def root():
	if not current_user.admin:
		return redirect(url_for('main_view.root'))
	unverified_businesses = Business.query.filter_by(verified=False).all()
	sign_in_count = SignIn.query.count()
	return render_template('admin.html', businesses=unverified_businesses, sc=sign_in_count)


@admin_view.route('/admin/approve/<string:business_name>', methods=["GET", "POST"])
@login_required
def approve(business_name):
	if not current_user.admin:
		return redirect(url_for('main_view.root'))
	business = Business.query.filter_by(business_name=business_name).first_or_404()
	business.verified = True
	db.session.commit()
	return redirect(url_for('admin_view.root'))


@admin_view.route('/admin/dump_db', methods=["GET", "POST"])
@login_required
def dump():
	if not current_user.admin:
		return redirect(url_for('main_view.root'))