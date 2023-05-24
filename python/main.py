from kafka import KafkaConsumer
from kafka import KafkaProducer
import json




bootstrap_servers = ['localhost:9093']
topicName = 'test'
sasl_mechanism = 'OAUTHBEARER'
group_id = 'group_id'
security_protocol = 'SASL_PLAINTEXT'
sasl_oauth_token_provider = ''
sasl_plain_username = 'test1'
sasl_plain_password = ''
client_id = ''
client_secret = ''
# To consume latest messages and auto-commit offsets


class TokenProvider(object):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def token(self):
        token_url = 'http://loaclhost:8080/realms/kafka/protocol/openid-connect/token'
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token_json = oauth.fetch_token(token_url=token_url, client_id=self.client_id, client_secret=self.client_secret)
        token = token_json['access_token']
        print(token)
        # print(token)
        return token

# def token():
#     token = sasl_oauth_token_provider
#     # print(token)
#     return token

def cons():
    consumer = KafkaConsumer(topicName,
                             group_id=group_id,
                             bootstrap_servers=bootstrap_servers
                             # security_protocol = security_protocol,
                             # sasl_plain_username = sasl_plain_username,
                             # sasl_plain_password = sasl_plain_password,
                             # sasl_mechanism = sasl_mechanism
                                )
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                              message.offset, message.key,
                                              message.value))

    consumer.close()


# задаем адрес брокера, топик и данные для авторизации

def prod():
    # создаем продюсера с настройками авторизации
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        security_protocol=security_protocol,
        # sasl_plain_username=sasl_plain_username,
        # sasl_plain_password=sasl_plain_password,
        sasl_oauth_token_provider=TokenProvider(client_id,client_secret),
        sasl_mechanism=sasl_mechanism,

        value_serializer=lambda m: json.dumps(m).encode('ascii')
    )
    for _ in range(0, 100):
        # отправляем сообщение в топик
        msg = {'text': 'Hello, Kafka!'}
        producer.send(topicName, msg)
        producer.flush()
        print("Message sent successfully!")

prod()
# cons()