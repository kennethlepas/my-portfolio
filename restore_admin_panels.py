from app import app
from database import db, Project

def restore():
    with app.app_context():
        # Titles to remove (consolidated ones)
        titles_to_remove = [
            'BloodLink App',
            'NyumbaniFix App',
            'MkulimaHub'
        ]
        
        for title in titles_to_remove:
            project = Project.query.filter_by(title=title).first()
            if project:
                print(f"Removing consolidated project: {title}")
                db.session.delete(project)
        
        db.session.commit()
        
        print("Re-running create_default_projects() to restore separate entries...")
        Project.create_default_projects()
        print("Success!")

if __name__ == '__main__':
    restore()
