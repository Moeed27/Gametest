from inspect import currentframe

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database.tables import ApplianceTemplate, JourneyTemplate, CarbonLog
from data_entry.forms import TypeForm, ApplianceForm, TransportForm
from database.enums import LogTypes
from config import db

data_entry_bp = Blueprint('data_entry', __name__, template_folder='templates')

@data_entry_bp.route('/form', methods=['GET', 'POST'])
@login_required
def type_off_form():
    form = TypeForm()
    if form.validate_on_submit():
        if form.type.data == 'Appliance':
            return redirect(url_for('data_entry.appliance'))
        elif form.type.data == 'Transport':
            return redirect(url_for('data_entry.transport'))
    return render_template('data_entry/form.html', form=form)


@data_entry_bp.route('/appliance', methods=['GET', 'POST'])
@login_required
def appliance():
    form = ApplianceForm()
    if form.validate_on_submit():
        userid = current_user.get_id()
        appliance_name = form.appliance.data
        wattage = form.wattage.data
        is_public = form.is_public.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        new_appliance = ApplianceTemplate(appliance_name=appliance_name, wattage=wattage, user_id=userid, is_public=is_public)
        db.session.add(new_appliance)
        new_carbon_log = CarbonLog(template_type=LogTypes.appliance, start_time=start_time, end_time=end_time, user_id=userid)
        db.session.add(new_carbon_log)
        db.session.commit()
        flash('Appliance form successfully submitted')
    return render_template('data_entry/appliance.html', form=form)

@data_entry_bp.route('/transport', methods=['GET', 'POST'])
@login_required
def transport():
    form = TransportForm()
    if form.validate_on_submit():
        userid = current_user.get_id()
        mode_name=form.transport.data
        carbon_per_km = 0
        if mode_name == 'car':
            carbon_per_km = 132
        elif mode_name == 'train':
            carbon_per_km = 32
        elif mode_name == 'bus':
            carbon_per_km = 93
        is_public = form.is_public.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        new_transport = JourneyTemplate(mode_name=mode_name, user_id=current_user.get_id(), is_public=is_public,
                                        carbon_per_km=carbon_per_km)
        new_carbon_log = CarbonLog(template_type=LogTypes.appliance, start_time=start_time, end_time=end_time,
                                   user_id=userid, is_public=is_public)
        db.session.add(new_transport)
        db.session.add(new_carbon_log)
        db.session.commit()
        flash('Transport form successfully submitted')
    return render_template('data_entry/transport.html', form=form)