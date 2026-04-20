from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {'key': self.key, 'title': self.title, 'content': self.content, 'order': self.order}

    @classmethod
    def create_default_sections(cls):
        defaults = [
            ('hero_title', 'Kenneth Lepas', 1),
            ('hero_subtitle', 'Final-year B.Sc. Computer Science Student | Software Engineer | Network Security | Data Analyst', 2),
            ('hero_bio', 'Final-year undergraduate at Egerton University with hands-on experience in software development, networking, cybersecurity, and data analytics. Certified by IBM, Microsoft, Cisco, and ICT Authority Kenya.', 2.1),
            ('hero_achievements', 'Certified CCNA & Ethical Hacker, 10+ Professional Certifications, End-to-End System Developer', 2.2),
            ('about_profile', 'Final-year Bachelor of Science in Computer Science student at Egerton University (Graduating Nov 2026). I combine a strong technical foundation in Software Engineering, Networking, and Cybersecurity with a user-centric approach gained through Human-Centered Design training. Fully available and eager to contribute to a professional environment immediately.', 3),
            ('professional_statement', 'Dedicated Software Engineering professional with a focus on Network Security and Data Analytics. Certified in CCNA, Ethical Hacking, and Data Science. I have successfully completed all academic coursework and am pending graduation in November 2026. Committed to building secure, scalable, and practical user-centered solutions.', 4),
            ('education_content', 'BSc. Computer Science, Egerton University (2022 – Nov 2026 Expected). Key Modules: Programming, Networking, Data Science, Software Development, and Database Systems. | KCSE, Kolanya Boys High School (2018 – 2021). Mean Grade: B+', 4.1),
            ('experience_content', 'ICT Attachment, Department of ICT and E-Government, Kakamega County HQ (Jan – Mar 2025). Supported ICT infrastructure operations, maintained government systems and networks, and assisted in e-government service delivery. Gained hands-on exposure to public sector ICT management and network troubleshooting.', 4.2),
            ('leadership_content', 'Christian Union Leader at Kolanya Boys High School. | Technical Project Group Leader at Egerton University. | Participant in Egerton-MSU Cross-Institutional Collaborative Program.', 4.3),
            ('hobbies_content', 'Chess (Strategic discipline), Nature walks (Reflection and wellbeing), Football (Recreational play).', 4.4),
            ('contact_email', 'kennethlepas@gmail.com', 5),
            ('contact_phone', '0115408612', 6),
            ('contact_address', '50100, Matungu, Kenya', 7),
            ('github_url', 'https://github.com/kennethlepas', 8),
            ('linkedin_url', 'https://linkedin.com/in/kennethlepas', 9),
            ('twitter_url', 'https://twitter.com/kennethlepas', 10),
            ('resume_url', '/static/certificates/cv.pdf', 11),
            ('technical_skills', 'Python, Flask, JavaScript, SQL, TypeScript, React Native, Firebase, Node.js, C#, .NET, TCP/IP, VLANs, Routing & Switching, Ethical Hacking, Penetration Testing, Nmap, Metasploit, Power BI, Data Analytics, Human-Centered Design, Enterprise Design Thinking, Artificial Intelligence', 12),
            ('profile_picture_url', '/static/certificates/profile.jpeg', 13),
        ]
        for key, content, order in defaults:
            existing = cls.query.filter_by(key=key).first()
            if existing:
                existing.content = content
                existing.order = order
            else:
                db.session.add(cls(key=key, title=key.replace('_', ' ').title(), content=content, order=order))
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    icon = db.Column(db.String(50))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {'platform': self.platform, 'url': self.url, 'icon': self.icon}

    @classmethod
    def create_default_links(cls):
        defaults = [
            ('GitHub', 'https://github.com/kennethlepas', 'fab fa-github', 1),
            ('LinkedIn', 'https://linkedin.com/in/kennethlepas', 'fab fa-linkedin-in', 2),
            ('Twitter', 'https://twitter.com/kennethlepas', 'fab fa-twitter', 3),
            ('Email', 'mailto:kennethlepas@gmail.com', 'fas fa-envelope', 4),
        ]
        for platform, url, icon, order in defaults:
            existing = cls.query.filter_by(platform=platform).first()
            if existing:
                existing.url = url
                existing.icon = icon
                existing.order = order
            else:
                db.session.add(cls(platform=platform, url=url, icon=icon, order=order, is_active=True))
        db.session.commit()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.String(500))
    github_link = db.Column(db.String(300))
    demo_link = db.Column(db.String(300))
    image_url = db.Column(db.String(300))
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'technologies': self.technologies.split(',') if self.technologies else [],
            'github_link': self.github_link,
            'demo_link': self.demo_link,
            'image_url': self.image_url
        }

    @classmethod
    def create_default_projects(cls):
        defaults = [
            ('BloodLink App', 'Comprehensive blood donation ecosystem featuring a mobile application for donors/recipients and a web-based administrative dashboard for hospital management.', 'React Native, Firebase, Node.js, TypeScript', 'https://github.com/kennethlepas/BloodLink-app', '', '', 1),
            ('NyumbaniFix App', 'Professional home repair and services platform encompassing a mobile application for booking and a web-based admin panel for service tracking.', 'TypeScript, Python, Flask', 'https://github.com/kennethlepas/nyumbanifixv1', '', '', 2),
            ('MkulimaHub', 'Digital platform providing smallholder farmers with precision agriculture tools, real-time market data, and access to advisory services. Applied human-centered design for low-digital-literacy users.', 'Python, Flask, SQLite', 'https://github.com/kennethlepas/MkulimaHub', '', '', 3),
            ('Sewage Billing System', 'A specialized billing and management system for sewage utility organizations, automating invoicing and customer record keeping.', 'C#, .NET, SQL Server', 'https://github.com/kennethlepas/SEWAGE-BILLING', '', '', 4),
            ('Data Analytics Comprehensive analysis', 'A repository showcasing advanced data processing and visualization projects using real-world datasets like diabetes and churn, and statistical models.', 'Python, Jupyter Notebook, Power BI', 'https://github.com/kennethlepas/DSA-DataAnalytics', '', '', 5),
        ]
        for title, desc, tech, github, demo, img, order in defaults:
            existing = cls.query.filter_by(title=title).first()
            if existing:
                existing.description = desc
                existing.technologies = tech
                existing.github_link = github
                existing.demo_link = demo
                existing.order = order
            else:
                db.session.add(cls(title=title, description=desc, technologies=tech, github_link=github, demo_link=demo, image_url=img, order=order))
        db.session.commit()

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    issuer = db.Column(db.String(200))
    date_earned = db.Column(db.String(50))
    credential_id = db.Column(db.String(100))
    pdf_filename = db.Column(db.String(200))
    skills = db.Column(db.String(500))
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'issuer': self.issuer,
            'date_earned': self.date_earned,
            'credential_id': self.credential_id,
            'pdf_filename': self.pdf_filename,
            'skills': self.skills.split(',') if self.skills else []
        }

    @classmethod
    def create_default_certifications(cls):
        defaults = [
            ('Human-Centered Design Training', 'Egerton University & Michigan State University', 'March 2026', '', 'hcd.jpg', 'User Research, Prototyping, Empathy Mapping, User Testing', 1),
            ('Complete Network Hacking Course 2026', 'Udemy', 'March 2026', 'UC-71fbd1b4-5701-414b-a45c-4b61a7a4d6e3', 'hacking_udemy.pdf', 'Network Security, Penetration Testing, Wireshark, Metasploit', 2),
            ('Data Analytics Training', 'ICT Authority Kenya & Data Breed Africa', 'March 2026', 'ICTA-1773559998-6084-39808', 'ict_analytics.pdf', 'Data Visualization, SQL, Python, Power BI, Statistical Analysis', 3),
            ('Ethical Hacking', 'Cisco Networking Academy', 'Feb 2026', '', 'hacking_cisco.pdf', 'Cybersecurity, Nmap, Vulnerability Assessment, Network Defense', 4),
            ('CCNAv7: Switching, Routing, and Wireless Essentials', 'Cisco Networking Academy', 'Aug 2024', '', 'ccna2.pdf', 'VLANs, STP, Routing Protocols, Wireless Security', 5),
            ('CCNAv7: Introduction to Networks', 'Cisco Networking Academy', 'Apr 2024', '', 'ccna1.pdf', 'TCP/IP, IP Addressing, Network Topology, Cisco IOS', 6),
            ('Introduction to Data Science', 'Kenyatta University via Cisco NetAcad', 'May 2024', '', 'datascience_cisco.pdf', 'Machine Learning Foundations, Data Wrangling, Exploratory Data Analysis', 7),
            ('Product Management 101', 'Simplilearn SkillUp', 'Dec 2025', '9533677', 'product_manager.pdf', 'Agile, Roadmap, Market Analysis, User Stories', 8),
            ('Professional Recommendation', 'Recommendation from Industry Mentor', '2026', '', 'recommendation.pdf', 'Professionalism, Reliability, Communication', 9),
            ('Academic Transcript', 'Egerton University', '2026', '', 'transcript.png', 'Software Engineering, Algorithms, Database Systems', 10),
            ('AI', 'ICT Authority Kenya & Pathways Technologies', 'April 2026', 'ICTA-1776709514-6162-39808', 'ai_certificate.pdf', 'Artificial Intelligence, Generative AI, Prompt Engineering, LLMs', 11),
            ('Enterprise Design Thinking Practitioner', 'IBM SkillsBuild', 'April 2026', 'XbC8qNW3', 'design.pdf', 'Design Thinking, Collaboration, Problem Solving', 12),
            ('Financial Literacy Training', 'LifeSmart', '2026', '', 'smart.jpeg', 'Personal Finance, Budgeting, Investment', 13),
        ]
        for name, issuer, date, cred_id, pdf_filename, skills, order in defaults:
            existing = cls.query.filter_by(name=name).first()
            if existing:
                existing.issuer = issuer
                existing.date_earned = date
                existing.credential_id = cred_id
                existing.pdf_filename = pdf_filename
                existing.skills = skills
                existing.order = order
            else:
                db.session.add(cls(name=name, issuer=issuer, date_earned=date, credential_id=cred_id, pdf_filename=pdf_filename, skills=skills, order=order))
        db.session.commit()

class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_admin': self.is_admin
        }