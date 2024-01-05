from flask import Flask, render_template, request, redirect, url_for, session
import os
import pathlib
import requests
from app import dao, login
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user

# import requests
# from flask import Flask, session, abort, redirect, request
# from google.oauth2 import id_token
# from google_auth_oauthlib.flow import Flow
# from pip._vendor import cachecontrol
# import google.auth.transport.requests


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')
@app.route("/login", methods=['get','post'])
def login_user_process():
    if request.method.__eq__('POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        user = dao.auth_user(email=email, password=password)
        if user:
            login_user(user=user)
            next = request.args.get('next')
            return redirect("/" if next is None else next)

    return render_template("login.html")



@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route('/logout')
def process_logout_user():
    logout_user()
    return redirect("/login")


@app.route('/register',  methods=['get','post'])
def register_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             email=request.form.get('email'),
                             password=password, err_msg=err_msg)
            except:
                err_msg = 'Hệ thống đang bận, vui lòng thử lại sau!'
            else:
                return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp! Vui lòng nhập lại"
    return render_template('register.html', err_msg=err_msg)

@app.route('/info')
def informaintion():
    return render_template('info.html')

@app.route('/info/<int:user_id>', methods=['get','post'])
def update(user_id):
    err_msg = ""
    if request.method.__eq__('POST'):
        try:
            dao.update_info(namSinh=request.form.get('namSinh'),
                            sdt=request.form.get('sdt'),
                            diaChi=request.form.get('diaChi'),
                            avatar=request.files.get('avatar'),
                            Patient_id=user_id)
        except:
            err_msg = 'Hệ thống đang bận, vui lòng thử lại sau!'
        else:
            err_msg= "Cập nhật thành công"
            return redirect('/info')




#
# app = Flask("Google Login App")
# app.secret_key = "CodeSpecialist.com"
#
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
#
# GOOGLE_CLIENT_ID = "33674737284-srfbp7srvi8ie2m0sr426fved0hjq2tp.apps.googleusercontent.com"
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
#
# flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
#     redirect_uri="http://127.0.0.1:5000/callback"
# )
#
#
# def login_is_required(function):
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:
#             return abort(401)  # Authorization required
#         else:
#             return function()
#
#     return wrapper
#
#
# @app.route("/login")
# def login():
#     authorization_url, state = flow.authorization_url()
#     session["state"] = state
#     return redirect(authorization_url)
#
#
# @app.route("/callback")
# def callback():
#     flow.fetch_token(authorization_response=request.url)
#
#     if not session["state"] == request.args["state"]:
#         abort(500)  # State does not match!
#
#     credentials = flow.credentials
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)
#
#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token,
#         request=token_request,
#         audience=GOOGLE_CLIENT_ID
#     )
#
#     session["google_id"] = id_info.get("sub")
#     session["name"] = id_info.get("name")
#     return redirect("/protected_area")
#
#
# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")
#
#
# @app.route("/")
# def index():
#     return "Hello World <a href='/login'><button>Login</button></a>"
#
#
# @app.route("/protected_area")
# @login_is_required
# def protected_area():
#     return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"
#
# @app.route("/user-login/google")
# def loginWithGoogle():
#     # Find out what URL to hit for Google login
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]
#
#     # Use library to construct the request for Google login and provide
#     # scopes that let you retrieve user's profile from Google
#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)
#
#
# @app.route("/user-login/google/callback")
# def callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get("code")
#
#     # Find out what URL to hit to get tokens that allow you to ask for
#     # things on behalf of a user
#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
#
#     # Prepare and send a request to get tokens! Yay tokens!
#     token_url, headers, body = client.prepare_token_request(
#         token_endpoint,
#         authorization_response=request.url,
#         redirect_url=request.base_url,
#         code=code
#     )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )
#
#     # Parse the tokens!
#     client.parse_request_body_response(json.dumps(token_response.json()))
#
#     # Now that you have tokens (yay) let's find and hit the URL
#     # from Google that gives you the user's profile information,
#     # including their Google profile image and email
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)
#
#     # You want to make sure their email is verified.
#     # The user authenticated with Google, authorized your
#     # app, and now you've verified their email through Google!
#     if userinfo_response.json().get("email_verified"):
#         # unique_id = userinfo_response.json()["sub"]
#         users_email = userinfo_response.json()["email"]
#         picture = userinfo_response.json()["picture"]
#         users_name = userinfo_response.json()["given_name"]
#     else:
#         return "User email not available or not verified by Google.", 400
#
#     if AccountPatient.query.filter(AccountPatient.email == users_email).first():
#         account_patient = AccountPatient.query.filter(AccountPatient.email == users_email).first()
#     else:
#         # Doesn't exist? Add it to the database.
#         if not utils.exist_user(users_email):
#             # Create a user in your db with the information provided by Google
#             patient = Patient(name=users_name, email=users_email, avatar=picture)
#             db.session.add(patient)
#         else:
#             if Patient.query.filter(Patient.email == users_email).first():
#                 patient = Patient.query.filter(Patient.email == users_email).first()
#             else:
#                 customer = Customer.query.filter(Customer.email == users_email).first()
#                 patient = utils.customerToPatient(customer, avatar=picture)
#
#         password = utils.create_password(users_email)
#         account_patient = AccountPatient(active=True, email=patient.email, password=password, patient=patient)
#         db.session.add(account_patient)
#         db.session.commit()
#
#     # Begin user session by logging the user in
#     login_user(account_patient)
#
#     # Send user back to homepage
#     return redirect("/")






if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
