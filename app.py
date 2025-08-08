from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'replace_with_a_secure_random_key'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'hampco.web@gmail.com'
app.config['MAIL_PASSWORD'] = 'rqfw ekxe klvd unrn'
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name         = request.form['name']
        email        = request.form['email']
        project_type = request.form['project_type']
        budget       = request.form.get('budget', 'N/A')
        timeline     = request.form.get('timeline', 'N/A')
        details      = request.form['details']

        # Email to YOU
        owner_msg = Message(
            subject=f"Project Inquiry: {project_type}",
            recipients=[app.config['MAIL_USERNAME']],
            reply_to=email  # so you can reply straight to the client
        )
        owner_msg.body = f"""You have a new project inquiry:

Name: {name}
Email: {email}
Project Type: {project_type}
Estimated Budget: {budget}
Desired Timeline: {timeline}

Details:
{details}
"""

        # Confirmation email to the USER
        confirm_msg = Message(
            subject="We received your message — HampCo Web Design",
            recipients=[email]
        )
        confirm_msg.body = f"""Hi {name},

Thanks for reaching out to HampCo Web Design! I got your message and will reply soon.

Here’s what you sent:
- Project Type: {project_type}
- Budget: {budget}
- Timeline: {timeline}

Details:
{details}

If you need to add anything else, just reply to this email.

— HampCo Web Design
"""
        # Optional HTML version (nice to have)
        confirm_msg.html = f"""
        <p>Hi {name},</p>
        <p>Thanks for reaching out to <strong>HampCo Web Design</strong>! I got your message and will reply soon.</p>
        <p><strong>Your submission</strong></p>
        <ul>
          <li><strong>Project Type:</strong> {project_type}</li>
          <li><strong>Budget:</strong> {budget}</li>
          <li><strong>Timeline:</strong> {timeline}</li>
        </ul>
        <p style="white-space:pre-wrap">{details}</p>
        <p>If you need to add anything else, just reply to this email.</p>
        <p>— HampCo Web Design</p>
        """

        try:
            mail.send(owner_msg)
            mail.send(confirm_msg)
            return redirect(url_for('thank_you'))
        except Exception:
            flash("Sorry, something went wrong sending email. Please try again later.")
            return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

if __name__ == '__main__':
    app.run(debug=True)

