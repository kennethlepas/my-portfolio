from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, Section, Project, Certification, UserMessage, SocialLink, User
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'Kenn@2459.')
app.config['ADMIN_EMAIL'] = os.environ.get('ADMIN_EMAIL', 'kennethlepas@gmail.com')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    if Section.query.count() == 0:
        Section.create_default_sections()
    if SocialLink.query.count() == 0:
        SocialLink.create_default_links()
    if Project.query.count() == 0:
        Project.create_default_projects()
    if Certification.query.count() == 0:
        Certification.create_default_certifications()
    
    # Create default admin user
    if User.query.filter_by(email=app.config['ADMIN_EMAIL']).count() == 0:
        admin = User(
            email=app.config['ADMIN_EMAIL'],
            password_hash=generate_password_hash(app.config['ADMIN_PASSWORD'])
        )
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin.html')

@app.route('/static/certificates/<filename>')
def serve_certificate(filename):
    return send_from_directory('static/certificates', filename)

@app.route('/api/sections')
def get_sections():
    sections = Section.query.all()
    return jsonify([s.to_dict() for s in sections])

@app.route('/api/social-links')
def get_social_links():
    links = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.order).all()
    return jsonify([l.to_dict() for l in links])

@app.route('/api/projects')
def get_projects():
    projects = Project.query.order_by(Project.order).all()
    return jsonify([p.to_dict() for p in projects])

@app.route('/api/certifications')
def get_certifications():
    certs = Certification.query.order_by(Certification.order).all()
    return jsonify([c.to_dict() for c in certs])

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.json
    message = UserMessage(
        name=data.get('name'),
        email=data.get('email'),
        message=data.get('message')
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Message sent successfully!'})

@app.route('/api/admin/messages')
@login_required
def get_admin_messages():
    messages = UserMessage.query.order_by(UserMessage.created_at.desc()).all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'email': m.email,
        'message': m.message,
        'created_at': m.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for m in messages])

@app.route('/api/admin/certifications', methods=['POST'])
@login_required
def add_certification():
    data = request.json
    new_cert = Certification(
        name=data.get('name'),
        issuer=data.get('issuer'),
        date_earned=data.get('date_earned'),
        credential_id=data.get('credential_id'),
        pdf_filename=data.get('pdf_filename'),
        order=Certification.query.count() + 1
    )
    db.session.add(new_cert)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Certification added successfully!'})

@app.route('/api/admin/sections', methods=['POST'])
@login_required
def update_section():
    data = request.json
    key = data.get('key')
    content = data.get('content')
    
    section = Section.query.filter_by(key=key).first()
    if section:
        section.content = content
        db.session.commit()
        return jsonify({'success': True, 'message': f'Section {key} updated!'})
    return jsonify({'error': 'Section not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)