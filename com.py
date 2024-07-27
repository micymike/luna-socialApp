from app import app, db

@app.route('/recreate_tables')
def recreate_tables():
    with app.app_context():
        db.drop_all()
        db.create_all()
    return 'Tables recreated successfully!'