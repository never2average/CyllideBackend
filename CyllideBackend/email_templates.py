import smtplib
from keys import specialEncoder,specialDecoder
from datetime import datetime,timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

emailSender="bondpriyesh@gmail.com"

def sendVerificationEmail(email,firstName):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Verify Email"
    msg['From'] = emailSender
    msg['To'] = email
    encodings=specialEncoder(email)
    action_url="localhost:5000/api/verify/"+encodings

    text="Hello There"
    html=open("email_templates_html/welcome.html").read()
    html=html.replace("{{name}}",firstName.capitalize()).replace("{{action_url}}",action_url)


    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP_SSL('smtp.gmail.com',465)
    s.login(emailSender,"viratkohli")
    s.sendmail(emailSender, email, msg.as_string())
    s.quit()


def passwordResetEmail(email,firstName,browser,osName):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Password Reset Link"
    msg['From'] = emailSender
    msg['To'] = email
    encodings=jwt.encode({"user":email,"exp":datetime.utcnow()+timedelta(hours=24)},verificationKey)
    action_url="localhost:5000/api/verify/"+str(encodings)

    text="Please Review this Page"

    html=open("email_templates_html/password_reset.html").read()
    html=html.replace("{{name}}",firstName.capitalize()).replace(
        "{{action_url}}",action_url).replace("{{browser_name}}",browser).replace("{{operating_system}}",osName).replace(
            "{{support_url}}","mailto:prasannkumar1263@gmail.com"
        )


    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP_SSL('smtp.gmail.com',465)
    s.login(emailSender,"viratkohli")
    s.sendmail(emailSender, email, msg.as_string())
    s.quit()