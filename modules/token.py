import webbrowser
import requests
import http.server
import threading
import urllib.parse

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if 'code' in params:
            self.server.auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            self.wfile.write("""
                <html>
                    <head>
                        <script>
                            setTimeout(() => { window.close(); }, 1000);
                        </script>
                    </head>
                    <body>
                        <p>¡Autorizaci&oacute;n completada! Puedes cerrar esta ventana.</p>
                    </body>
                </html>
            """.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("Error al obtener el código de autorización.".encode('utf-8'))

# Check if the token is valid
def validation(token):
    url = 'https://id.twitch.tv/oauth2/validate'

    headers = {
        'Authorization': f'OAuth {token}'
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200:
            return True
        else:
            print(f"Error {data['status']}: {data['message']}")
    except requests.RequestException as error:
        print(f"Error: {error}")

    return False

# Get an access token, redirecting the user to the authorization page
def get_authorization(client_id, client_secret, redirect_uri, scope):
    auth_endpoint = 'https://id.twitch.tv/oauth2/authorize'
    encoded_scopes = urllib.parse.quote(' '.join(scope))
    auth_url = f"{auth_endpoint}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={encoded_scopes}"
    server_port = 3000
    server = http.server.HTTPServer(('localhost', server_port), OAuthHandler)
    server.auth_code = None

    # Start the server to capture the redirection
    #webbrowser.open(auth_url)
    print(auth_url)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    # Wait until the authorization code is received
    while server.auth_code is None:
        pass

    return get_access_token(server.auth_code, client_id, client_secret, redirect_uri)

# Switch the obtainded authorization code for an access token
def get_access_token(auth_code, client_id, client_secret, redirect_uri):
    url = 'https://id.twitch.tv/oauth2/token'

    parameters = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    try:
        response = requests.post(url, params=parameters)
        data = response.json()

        if response.status_code == 200:
            return data['access_token']
        else:
            print(f"Error {data['status']}: {data['message']}")
    except requests.RequestException as error:
        print(f"Error: {error}")

    return None