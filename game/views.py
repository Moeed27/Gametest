from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database.tables import User, Friend

game_bp = Blueprint('game', __name__, template_folder='templates')

@game_bp.route('/leaderboard')
@login_required
def leaderboard():

    user_list = User.query.all()
    all_friends = []
    all_friends_ordered = []
    
    for i in range(1, len(user_list)):
        if (Friend.check_friends(current_user.user_id, user_list[i].user_id)):
            all_friends.append(user_list[i])

    for i in range(1,len(all_friends)):
        initial_user = all_friends[i]
        initialval = all_friends[i].ecopoints
        j = i-1

        while j >= 0 and initialval < all_friends[j].ecopoints:
            all_friends[j + 1] = all_friends[j]
            j -= 1
        all_friends[j + 1] = initial_user
        
    for i in range (len(all_friends)-1,-1,-1):

        all_friends_ordered.append(all_friends[i])

    return render_template('game/leaderboard.html', users = all_friends_ordered, len=len(all_friends_ordered))