#  -*- encoding: utf-8 -*-

import time

import requests

from clients.database import DatabaseClient
from common.aes_cipher import AESCipher
from common.constants_and_variables import BotVariables, BotConstants


class GetAthleteToken(object):

    def __init__(self):
        self.database_client = DatabaseClient()
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.aes_cipher = AESCipher(self.bot_variables.crypt_key_length, self.bot_variables.crypt_key)

    def refresh_and_update_token(self, athlete_id, refresh_token):
        response = requests.post(self.bot_constants.API_TOKEN_EXCHANGE, data={
            'client_id': int(self.bot_variables.client_id),
            'client_secret': self.bot_variables.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }).json()

        self.database_client.write_operation(self.bot_constants.QUERY_UPDATE_TOKEN.format(
            access_token=self.aes_cipher.encrypt(response['access_token']),
            refresh_token=self.aes_cipher.encrypt(response['refresh_token']),
            expires_at=response['expires_at'],
            athlete_id=athlete_id
        ))

        return response['access_token']

    def get_token(self, athlete_id):
        access_token = None
        result = self.database_client.read_operation(self.bot_constants.QUERY_FETCH_TOKEN.format(athlete_id=athlete_id))
        if result:
            access_token = self.aes_cipher.decrypt(result[0])
            refresh_token = self.aes_cipher.decrypt(result[1])
            expires_at = result[2]

            if int(time.time()) > expires_at:
                access_token = self.refresh_and_update_token(athlete_id, refresh_token)

        return access_token
