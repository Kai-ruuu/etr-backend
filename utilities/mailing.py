from backend.enums.user import Role
from backend.utilities.environment import envs, envi

import smtplib
import logging
from pydantic import EmailStr
from email.message import EmailMessage

def mail(to: str, subject: str, body: str, html: str | None = None) -> None:
   message = EmailMessage()
   message["From"] = envs("SYSTEM_EMAIL")
   message["To"] = to
   message["Subject"] = subject

   message.set_content(body)

   if html:
      message.add_alternative(html, subtype="html")

   try:
      with smtplib.SMTP(envs("SYSTEM_SMTP_HOST"), envi("SYSTEM_SMTP_PORT")) as server:
         server.starttls()
         server.login(envs("SYSTEM_EMAIL"), envs("SYSTEM_EMAIL_PASSWORD"))
         server.send_message(message)
         logging.info("[MAILING] Email sent successfully.")
   except Exception as e:
      logging.error(f"[MAILING] Email send failed: {e}")

def get_indefinite_article_for(next_word: str):
   return "an" if next_word[0].lower() in "aeiou" else "a"

def mail_admin_welcome(new_admin_dict: dict, temporary_password: str, sysad_email: EmailStr):
   first = new_admin_dict.get("first_name", "")
   middle = new_admin_dict.get("middle_name") or ""
   last = new_admin_dict.get("last_name", "")
   full_name = f"{first} {middle + ' ' if middle else ''}{last}".strip()

   new_admin_email = new_admin_dict.get("email")
   new_admin_role = Role.as_display(new_admin_dict.get("role"))
   article = get_indefinite_article_for(new_admin_role)

   body = (
      f"You've been assigned by our System Administrator as {article} {new_admin_role}.\n"
      f"Your temporary password is: {temporary_password}\n"
      f"If this was a mistake, contact our System Administrator at {sysad_email}\n"
      f"Best Regards - E-trace Team"
   )

   html_body = f"""
   <html>
   <body style="font-family: Arial, sans-serif; line-height: 1.6;">
      <h2>Welcome to E-trace, {full_name}!</h2>

      <p>You've been assigned by our System Administrator as 
      <strong>{article} {new_admin_role}</strong>.</p>

      <p>Please use this temporary password to log in:</p>

      <div style="
         background: #f4f4f4;
         padding: 10px 15px;
         border-radius: 5px;
         display: inline-block;
         font-weight: bold;
         font-size: 1.1rem;
      ">{temporary_password}</div>

      <p style="margin-top: 20px;">
         After logging in, it is strongly recommended to change your password 
         to fully secure your account.
      </p>

      <p>If this was a mistake, please contact our System Administrator: 
      <a href="mailto:{sysad_email}">{sysad_email}</a></p>

      <br>
      <p>Best Regards,<br><strong>E-trace Team</strong></p>
   </body>
   </html>
   """

   mail(
      to=new_admin_email,
      subject=f"Welcome to E-trace, {full_name}!",
      body=body,
      html=html_body
   )

def mail_reset_link(reset_token: str, user_email: EmailStr):
   reset_url = f'{envs("FRONT_END_URL")}/auth/reset-password?token={reset_token}'

   body = (
      "A password reset was requested for your account.\n"
      f"Click the link below to reset your password:\n{reset_url}\n\n"
      "If you did not request this, you can safely ignore the email.\n"
      "Best Regards - E-trace Team"
   )

   html_body = f"""
   <html>
   <body style="font-family: Arial, sans-serif; line-height: 1.6;">

      <h2>Password Reset Request</h2>

      <p>We received a request to reset your password.  
      Click the button below to continue:</p>

      <a href="{reset_url}" 
         style="
            display: inline-block;
            padding: 12px 18px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
         ">
         Reset Password
      </a>

      <p style="margin-top: 20px;">
         Or copy & paste this link into your browser:<br>
         <a href="{reset_url}">{reset_url}</a>
      </p>

      <p>If you did not request a password change, no action is required.</p>

      <br>
      <p>Best Regards,<br><strong>E-trace Team</strong></p>
   </body>
   </html>
   """

   mail(
      to=user_email,
      subject="Reset Your Password - E-trace",
      body=body,
      html=html_body
   )
