import requests
import time

def dancing(direction, action):
       # 192.168.9.190 Benay Telefonu
   # 192.168.180.190 Abdullah
    """url = "http://192.168.180.190/control"
    params = {'direction': direction, 'action': action}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print(f"Movement sent successfully - Direction: {direction}, Action: {action}")
        else:
            print(f"Failed to send movement - Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

        """


dance_moves = [
            ('forward', 'start'),
            ('right', 'start'),
            ('backward', 'start'),
            ('left', 'start'),
            ('stop', 'stop')
        ]

        # Loop through the dance moves
for move in dance_moves:
    dancing(*move)
    time.sleep(1)  # Adjust sleep duration as need"""