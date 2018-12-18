import os

import requests
import spotipy.util as util
from cred_auth import spotify_credencials as cred
from cred_auth import api_key_vagalume

token = util.prompt_for_user_token(cred['user'], cred['scope'], client_id=cred['client_id'],
                                   client_secret=cred['client_secret'],
                                   redirect_uri=cred['redirect_uri'])

api_key = api_key_vagalume
letra_tmp = ''


def letra():
    try:
        resp_current_song = requests.get('https://api.spotify.com/v1/me/player/currently-playing',
                                         headers={'Authorization': f'Bearer {token}'}).json()
        artista = resp_current_song['item']['artists'][0]['name']
        musica = resp_current_song['item']['name']
        musica = musica[:musica.lower().find('(feat.')]
    except:
        return "Não ouvindo musica no momento"

    global letra_tmp
    if musica in letra_tmp:
        return letra_tmp
    try:
        print(f"Pesquisando {musica} - {artista}...")
        resp_letra = requests.get(
            f'https://api.vagalume.com.br/search.php?art={artista}&mus={musica}&apikey={api_key}')
        resp_letra = resp_letra.json()
        letra_txt = resp_letra['mus'][0]['text']
    except Exception as inst:
        return f"Ocorreu um erro, ...tipo {type(inst)}"

    letra_tmp = '\n\n' + musica + '\n\n' + letra_txt + '\n\n'
    return letra_tmp


if __name__ == "__main__":
    while True:
        proxima = input('Aperte enter pra ver letra da musica atual ou escreva x pra sair: ')
        if proxima == '':
            os.system('cls')
            print(letra())
        elif proxima == 'x':
            break
