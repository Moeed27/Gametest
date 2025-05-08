"""
This file defines the route to generate the weekly carbon analysis for a login user.
"""
from datetime import date, timedelta
from flask import Blueprint, render_template, jsonify, url_for, redirect
from flask_login import current_user, login_required
from database.enums import LogTypes

# Define a Blueprint for graph analysis
graph_analysis_bp = Blueprint("graph", __name__, template_folder="templates")


@graph_analysis_bp.route("/dashboard/<int:year>/<int:week>")
@login_required
def dashboard(year, week):
    """
    Render the dashboard page for the analysis of given year and week.
    The graph_analysis/graph.html will redirect to the /weekly_emissions/<int:year>/<int:week> route.

    Args:
        year (int): The year of the analysis to render.
        week (int): The week of the analysis to render.

    Returns:
        HTML template of the graph page.
    """
    return render_template("graph_analysis/graph.html", year=year, week=week)


def get_week_range(year, week):
    """
    Calculate the start and end date for a given week and year.

    Args:
        year (int): ISO year.
        week (int): ISO week.

    Returns:
        tuple: Start date and end date.
    """
    start = date.fromisocalendar(year, week, 1)
    end = start + timedelta(days=6)
    return start, end


@graph_analysis_bp.route("/weekly_emissions/<int:year>/<int:week>")
@login_required
def get_weekly_emissions(year, week):
    """
    API endpoint that returns weekly carbon emission data for the logged-in user

    Args:
        year (int): The year of the analysis to render.
        week (int): The week of the analysis to render.

    Returns:
        JSON: information to render in the page
    """
    try:
        # Get start and end dates of a given week
        start_date, end_date = get_week_range(year, week)
    except Exception as e:
        # Return error when inputting invalid week or year
        return jsonify({"error": f"Invalid week/year: {e}"}), 400
    # Define the days of the week in order
    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    daily_totals = {day: 0 for day in weekday_order}
    breakdown = {"Transport": 0, "Appliance": 0}

    # use method of a user object to get the log entries of the given week
    logs = current_user.get_carbon_entries(start_date, end_date)

    # Calculate daily total emissions
    for log in logs:
        weekday = log.start_time.strftime("%A")
        carbon = log.get_carbon()
        daily_totals[weekday] += carbon

        if log.template_type == LogTypes.trip:
            breakdown["Transport"] += carbon
        elif log.template_type == LogTypes.appliance:
            breakdown["Appliance"] += carbon

    return jsonify(
        {
            "labels": weekday_order,
            "daily_emissions": [round(daily_totals[day], 2) for day in weekday_order],
            "breakdown_labels": list(breakdown.keys()),
            "breakdown_data": [round(val, 2) for val in breakdown.values()],
            "start_date": str(start_date),
            "end_date": str(end_date),
            "year": year,
            "week": week,
        }
    )


@graph_analysis_bp.route("/report")
@login_required
def redirect_to_latest_week():
    """
    Redirects to the last week report based on the current visiting time.

    Returns:
        Redirect to the graph.dashboard URL with most recent completed year and week.
    """
    today = date.today()
    year, week, _ = today.isocalendar()

    if week == 1:
        # If current week is the first week of the year, get last week from the previous year
        year -= 1
        last_day = date(year, 12, 28)
        week = last_day.isocalendar()[1]
    else:
        week -= 1

    return redirect(url_for("graph.dashboard", year=year, week=week - 1))
