import requests
import http.server
import threading
import urllib.parse

class Token:
    def __init__(self, client_id, client_secret, scope, redirect_uri, server_port = 3000):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.server_port = server_port

    # Check if the token is valid
    @staticmethod
    def validation(token: str) -> bool:
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
    
    # Switch a authorization code for an access token
    def get_access_token(self, auth_code: str) -> str:
        url = 'https://id.twitch.tv/oauth2/token'

        parameters = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }

        try:
            response = requests.post(url, params=parameters)
            data = response.json()

            if response.status_code == 200:
                return data
            else:
                print(f"Error {data['status']}: {data['message']}")
        except requests.RequestException as error:
            print(f"Error: {error}")

        return None
    
    # Refresh an expired token to get a new one 
    def refresh_access_token(self, refresh_token: str) -> dict:
        url = 'https://id.twitch.tv/oauth2/token'

        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response = requests.post(url, params=params, headers=headers)
            data = response.json()

            if response.status_code == 200:
                return data
            else:
                print(f"Error {data['status']}: {data['message']}")
        except requests.RequestException as error:
            print(f"Error: {error}")

    
    # Generate a link to user can authorise the application and get a code to generate a token
    def generate_auth_url(self) -> str:
        url = 'https://id.twitch.tv/oauth2/authorize'
        encoded_scopes = urllib.parse.quote(' '.join(self.scope))
        auth_url = f'{url}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope={encoded_scopes}'
        return auth_url
    
    # Run a local server to handle the redirect from the auth URL
    def get_authorization(self) -> str:
        try:
            server = http.server.HTTPServer(('localhost', self.server_port), OAuthHandler)
            server.auth_code = None
            server.auth_event = threading.Event()
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()

            # Wait until the authorization code is received
            server.auth_event.wait()

            return self.get_access_token(server.auth_code)
        except Exception as error:
            print(f"Error: {error}")

# class responsible for processing incoming requests
class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if 'code' in params:
            self.server.auth_code = params['code'][0]
            self.server.auth_event.set()
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
                        <p>¡Autorización completada! Puedes cerrar esta ventana.</p>
                    </body>
                </html>
            """.encode('utf-8'))

            # Turn off the server after proceesing the request
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("Error al obtener el código de autorización.".encode('utf-8'))