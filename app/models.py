
from .extensions import db
from flask_login import UserMixin

ROLE_SUPERADMIN = "superadmin"
ROLE_ADMIN = "admin"
ROLE_USER = "user"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default=ROLE_USER)

    def has(self, perm):
        if self.role == ROLE_SUPERADMIN:
            return True
        if self.role == ROLE_ADMIN:
            return perm in {"create","update","export","user_management"}
        return perm in set()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class VendorM(db.Model):
    __tablename__ = 'vendor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class LocationM(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    __table_args__ = (db.UniqueConstraint('name','email', name='uq_recipient_name_email'),)

class CategoryM(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class SubCategoryM(db.Model):
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('CategoryM', backref='subcategories')
    __table_args__ = (db.UniqueConstraint('name','category_id', name='uq_subcat_name_cat'),)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(120))
    invoice_date = db.Column(db.Date)
    serial_number = db.Column(db.String(120))
    purchase_order_no = db.Column(db.String(120))
    received_date = db.Column(db.Date)
    owner_email = db.Column(db.String(255))
    description = db.Column(db.Text)
    manufacturer = db.Column(db.String(120))
    model = db.Column(db.String(120))
    vendor = db.Column(db.String(120))
    mfg_country = db.Column(db.String(120))
    hsn_code = db.Column(db.String(120))
    is_bonded = db.Column(db.String(3))
    last_calibrated = db.Column(db.Date)
    next_calibration = db.Column(db.Date)
    notes = db.Column(db.Text)
    entry_no = db.Column(db.String(120))
    returnable_no = db.Column(db.String(3))
    cap_x = db.Column(db.String(3))
    amortization_period = db.Column(db.String(20))
    team = db.Column(db.String(120))
    recipient_name = db.Column(db.String(120))
    recipient_email = db.Column(db.String(255))
    category = db.Column(db.String(120))
    sub_category = db.Column(db.String(120))
    location = db.Column(db.String(120))

def seed_defaults():
    from werkzeug.security import generate_password_hash
    if not User.query.first():
        admin = User(name="Super Admin", email="admin@example.com",
                     password_hash=generate_password_hash("admin123"), role=ROLE_SUPERADMIN)
        db.session.add(admin)
    if not Team.query.first():
        db.session.add_all([Team(name=n) for n in ["Validation","Platform","Manufacturing","R&D"]])
    if not Manufacturer.query.first():
        db.session.add_all([Manufacturer(name=n) for n in ["Tektronix","Keysight","R&S","Hakko","Saleae"]])
    if not VendorM.query.first():
        db.session.add_all([VendorM(name=n) for n in ["TechVendor","InstruMart","MeasureCo","SolderPro","LogicVendor"]])
    if not LocationM.query.first():
        db.session.add_all([LocationM(name=n) for n in ["Bangalore","Hyderabad","Pune","Chennai"]])
    if not CategoryM.query.first():
        te = CategoryM(name="Test Equipment")
        tools = CategoryM(name="Tools")
        db.session.add_all([te, tools]); db.session.flush()
        db.session.add_all([SubCategoryM(name="Oscilloscope", category_id=te.id),
                            SubCategoryM(name="Analyzer", category_id=te.id),
                            SubCategoryM(name="Multimeter", category_id=te.id),
                            SubCategoryM(name="Soldering", category_id=tools.id)])
    db.session.commit()
