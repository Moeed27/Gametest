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
        new_appliance = ApplianceTemplate(template_name=appliance_name, wattage=wattage, user_id=userid, is_public=is_public)
        new_carbon_log = CarbonLog(template_type=LogTypes.appliance, start_time=start_time, end_time=end_time, user_id=userid)
        db.session.add(new_appliance)
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
        if mode_name == 'Car (Petrol)':
            carbon_per_km = 165
        elif mode_name == 'Car (Diesel)':
            carbon_per_km = 170
        elif mode_name == 'Train':
            carbon_per_km = 32
        elif mode_name == 'Bus':
            carbon_per_km = 75
        elif mode_name == 'Plane':
            carbon_per_km = 246
        elif mode_name == 'Motorbike':
            carbon_per_km = 80
        elif mode_name == 'Bicycle':
            carbon_per_km = 21
        is_public = form.is_public.data == "True"
        start_time = form.start_time.data
        end_time = form.end_time.data
        distance_unit = form.distance_unit.data
        distance = form.distance.data
        if distance_unit == 'Miles':
            distance = distance * 1.609
        new_transport = JourneyTemplate(template_name=mode_name, user_id=current_user.get_id(), is_public=is_public,
                                        carbon_per_km=carbon_per_km)
        db.session.add(new_transport)
        db.session.commit()
        new_carbon_log = CarbonLog(template_type=LogTypes.trip, start_time=start_time, end_time=end_time,
                                   user_id=userid, journey_distance=distance, template_id=new_transport.template_id)
        db.session.add(new_carbon_log)
        db.session.commit()
        flash('Transport form successfully submitted')
    return render_template('data_entry/transport.html', form=form)