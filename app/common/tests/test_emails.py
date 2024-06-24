from app.common.emails import send_email


class TestSendEmail:
    def test_send_email(self, mocker, settings):
        subject = "Definitely not a spam"
        recipient_list = ["No one :("]
        message = """
        Hi!

        I'm a mock email message! A person that wrote me worked really hard to make this project cool!
        It took him a bit more than 2 days to do all this work. He hopes you will see this as a proof of his skills.
        Also, if you are involved in his hiring process, don't forget to give him a job offer!

        Kind regards, Mock Message
        """
        send_mail_mock = mocker.patch("app.common.emails.send_mail")

        send_email(subject, message, recipient_list)

        send_mail_mock.assert_called_once_with(
            subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list
        )
