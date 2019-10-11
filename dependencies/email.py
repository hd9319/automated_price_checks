import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config.settings import EMAIL_SETTINGS

class Email(object):
	def __init__(self, email_type):
		self._smtp_host = EMAIL_SETTINGS['SMTP_HOST']
		self._smtp_port = EMAIL_SETTINGS['SMTP_PORT']
		self._email = EMAIL_SETTINGS['EMAIL_ADDRESS']
		self._password = EMAIL_SETTINGS['PASSWORD']

	@staticmethod
	def _get_recipients(email_type):
		""" Retrieve recipients list based on type of email.

		Parameters
		----------
		email_type : str
		    Type of email

		Returns
		-------
		logging.Logger
		    Logger with RotatingFileHandler and StreamHandler
		"""

		if email_type in EMAIL_SETTINGS['RECIPIENTS'].keys():
			return EMAIL_SETTINGS['RECIPIENTS'][email_type]

		raise Exception('Invalid Email Type: %s' % email_type)


	@staticmethod
	def _get_template(subject, **data):
		""" Generate email body for message.

		Parameters
		----------
		subject : str
		    Subject category of email concern.
		data : multi-args
			Used to retrieve content to populate templates.

		Returns
		-------
		html : str
		    HTML template of email message.
		"""
		
		html = """
				<html>
				  <body>
				    <p>%s<br>
				       %s
				    </p>
				  </body>
				</html>
				"""

		if subject == 'PRICE':
			html = """
				<html>
				  <body>
				    <p>%s<br>
				       Competitor price is lower: <br>
				       <a href="%s">Source</a>
				    </p>
				  </body>
				</html>
				"""
			 html = html % ('PRICE NOTIFICATION', data['url_source'])
			return html
		elif subject == 'SYSTEM_ERRORS':
			 html = html % ('ERROR NOTIFICATION', data['error_message'])
			return html
		elif subject == 'TEST':
			html = html % ('TEST NOTIFICATION', data['test_message'])
			return html
		else: 
			return None

	def send_email(self, email_type, **kwargs):
		""" Sends an email to the relevant parties.

		Parameters
		----------
		email_type : str
		    Subject category of email concern.
		kwargs : multi-args
			Used to pass content to templates.

		Returns
		-------
		None
		"""

		recipients = self._get_recipients(email_type)
		message = self._generate_message(email_type, **kwargs)

		# Create secure connection with server and send email
		with smtplib.SMTP(self._smtp_host, self._stmp) as server:
			server.starttls()
			server.login(self._email, self._password)
			server.sendmail(
			    self._email, self.recipients, message.as_string()
			)
		
	def _generate_message(self, subject, **kwargs):
		""" Generate message for email delivery.

		Parameters
		----------
		subject : str
		    Subject category of email concern.
		kwargs : multi-args
			Used to pass content to templates.

		Returns
		-------
		message : MIMEMultipart
		    Email message containing subject, recipients and body.
		"""
		message = MIMEMultipart("alternative")
		message["Subject"] = subject
		message["From"] = self._email
		message["To"] = ', '.join(self.recipients)
		
		# Validate Email Message
		html_message = self._get_template(subject, **kwargs)
		if not html_message:
			html_message = self._get_template('Error', error_message='Invalid request.')

		message.attach(MIMEText(html_message))

		return message

	def test(self):
		"""
		Sends a test email.
		"""
		self.send_email(subject='TEST', test_message='This is a test message.')



