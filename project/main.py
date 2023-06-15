from crypt import methods
from unicodedata import name
from flask import Blueprint,render_template,current_app,request,Flask
from flask_login import login_required, current_user
from project.models import Client,CustomerTransaction
 



from . import main
# from project.dashapp import dash_app



main = Blueprint('main', __name__)


ROWS_PER_PAGE = 20


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)

    clients = Client.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    


    return render_template('index.html',clients=clients)

@main.route('/profile')
@login_required
def profile():
    return  render_template('profile.html', name=current_user.name)

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        search_query = request.form.get('client_name')

        if search_query:
            # Filter clients based on search query using SQLAlchemy filter
            filtered_clients = Client.query.filter(Client.name.ilike(f'%{search_query}%')).all()
        else:
            filtered_clients = []

        return render_template('search.html', clients=filtered_clients)

    # Render the initial search page
    return render_template('search.html', clients=[])


# @main.route('/generate_report/', methods=['GET', 'POST'])
# @login_required
# def generate_report():
#     return render_template('reports.html')




