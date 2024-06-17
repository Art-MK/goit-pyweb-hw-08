# models.py
import mongoengine as me
import connect

class Contact(me.Document):
    full_name = me.StringField(required=True)
    email = me.EmailField(required=True)
    phone_number = me.StringField(required=True)
    preferred_method = me.StringField(choices=['email', 'sms'], default='email')
    email_sent = me.BooleanField(default=False)
    sms_sent = me.BooleanField(default=False)
