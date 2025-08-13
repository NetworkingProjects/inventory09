
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Optional, Email

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class AssetForm(FlaskForm):
    invoice_no = StringField("Invoice No", validators=[Optional()])
    invoice_date = DateField("Invoice Date", validators=[Optional()])
    serial_number = StringField("Serial Number", validators=[Optional()])
    purchase_order_no = StringField("Purchase Order No", validators=[Optional()])
    received_date = DateField("Received Date", validators=[Optional()])
    owner_email = StringField("Owner Email", validators=[Optional(), Email()])
    description = TextAreaField("Description", validators=[Optional()])

    manufacturer = SelectField("Manufacturer", choices=[], validators=[Optional()], validate_choice=False)
    model = StringField("Model", validators=[Optional()])
    vendor = SelectField("Vendor", choices=[], validators=[Optional()], validate_choice=False)
    mfg_country = SelectField("Mfg Country", choices=[("",""),("United States","United States"),("Germany","Germany"),("Japan","Japan"),("India","India"),("China","China"),("Taiwan","Taiwan")], validators=[Optional()], validate_choice=False)
    hsn_code = StringField("HSN Code", validators=[Optional()])
    is_bonded = SelectField("Is Bonded", choices=[("",""),("y","Yes"),("n","No"),("na","N/A")], validators=[Optional()], validate_choice=False)
    last_calibrated = DateField("Last Calibrated", validators=[Optional()])
    next_calibration = DateField("Next Calibration", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])
    entry_no = StringField("Entry No", validators=[Optional()])
    returnable_no = SelectField("Returnable", choices=[("",""),("y","Yes"),("n","No"),("na","N/A")], validators=[Optional()], validate_choice=False)
    cap_x = SelectField("Cap X", choices=[("",""),("y","Yes"),("n","No"),("na","N/A")], validators=[Optional()], validate_choice=False)
    amortization_period = StringField("Amortization Period", validators=[Optional()])

    team = SelectField("Team", choices=[], validators=[Optional()], validate_choice=False)

    recipient_name = HiddenField("Recipient Name")
    recipient_email = HiddenField("Recipient Email")

    category = SelectField("Category", choices=[], validators=[Optional()], validate_choice=False)
    sub_category = SelectField("Sub Category", choices=[], validators=[Optional()], validate_choice=False)
    location = SelectField("Location", choices=[], validators=[Optional()], validate_choice=False)

    submit = SubmitField("Save")
