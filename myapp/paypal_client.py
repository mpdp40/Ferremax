from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

class PayPalClient:
    def __init__(self):
        self.client_id = 'AfjWw16xI3aGBAMWyf-kYWpUYLQpezAjH26UidNNlQhTFoGHHBocl8ZbVVJeo0eSdndUAmdEyXQ0iNJ7'
        self.client_secret = 'EOI01wPO3L4By8_SdQ72aW0s9vLt9NXdTrHFZDuWEHbmxi3ZGiun_HQeL6r3BjGEzmM4yoBUhAwc4LR7'

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment) 