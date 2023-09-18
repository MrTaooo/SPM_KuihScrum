#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
import json
import amqp_setup
import pika

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from os import environ
from dotenv import load_dotenv

load_dotenv()
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']


monitorBindingKey = '*.success'


def receiveSuccessLog():
    amqp_setup.check_setup()

    queue_name = 'Success_queue'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def callback(channel, method, properties, body):
    print("\nReceived an success log by " + __file__)
    processSuccessLog(json.loads(body))
    print()  # print a new line feed


def processSuccessLog(success):
    print("Recording an success log:")
    print(success)
    send_success_notification(order)  # Send success notification to users


def send_success_notification(data):
    # code = data.get('code', 0)
    # message = data.get('message', '')

    # # Extract email address from data (assuming it's included)
    # email = data.get('email', '')

    # print("Test data (START)")
    # print(data)
    # print("Test data (END)")
    # code = data['code']
    try:
        message = data['message']
        paymentStatus = message['paymentStatus']

        buyerEmail = data['buyerEmail']
        seller_Emails = data['sellerEmails']

        if paymentStatus == 'Payment_Successful':
            subjectBuyer = "Purchase Successful"
            messageBuyer = f"You have purchased {message['purchaseSummary']['checkoutDescription']}. Total amount is ${message['purchaseSummary']['totalAmount']}USD"

            subjectSeller = "Purchase Successful"
            messageSeller = f"We are excited to inform you that your item has been successfully sold on our platform! Congratulations on making a sale, and we appreciate your trust in using our services."

        else:
            return {"error": "Invalid status code"}, 400

        # Send email using SendGrid
        send_email(buyerEmail, subjectBuyer, messageBuyer)

        for eachSellerEmail in seller_Emails:
            send_email(eachSellerEmail, subjectSeller, messageSeller)

        return {
            "code": 201,
            "message": "Email sent"
        }

    except:
        return {
            "code": 400,
            "message": "Email fail to send"
        }


def send_email(to_email, subject, content):
    message = Mail(
        from_email="lintao199@gmail.com",
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        # print("TEST (START)")
        # print(sg)
        # print("BREAK")
        # print(response)
        # print("TEST (END)")

        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        print("Error sending email")
    print()  # print a new line feed


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    receiveSuccessLog()
