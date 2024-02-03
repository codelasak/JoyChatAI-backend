import requests

def convert_audio_to_text_sestek(audio_file):
    try:
        url = "https://srapi.knovvu.com/v1/speech/dictation/request"

        headers = {
            'Content-Type': 'audio/wave',
            'ModelName': 'Turkish',
            'ModelVersion': '1',
            'Tenant': 'Default',
            'SendAudioDownloadLink': 'true',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkYxQUVGOUFCMUYzQzBEMUU2MzczMzdBQTdENzU3MzdBMjQ1RkY0MkJSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6IjhhNzVxeDg4RFI1amN6ZXFmWFZ6ZWlSZjlDcyJ9.eyJuYmYiOjE3MDY5NTUzMTIsImV4cCI6MTczODQ5MTMxMiwiaXNzIjoiL2xkbS1pZGVudGl0eSIsImF1ZCI6IkxkbV9JbnRlZ3JhdGlvbiIsImNsaWVudF9pZCI6InRpY2FyZXRlZHUuQXBpQ2xpZW50LkxzZzdSbFhUQWstekViN2l0LTNSM1EiLCJpYXQiOjE3MDY5NTUzMTIsInNjb3BlIjpbIkxkbV9JbnRlZ3JhdGlvbiJdfQ.EXR2Cm0X9CljG6hbpqz3wLipGRy6wSIKH44kk7J9f5CnzfaLUIHVKAevp8Z8Uu3ycJqJvi3MEMl7wT85AF2RNs-kDOAdQiHHvR5phqLIDeOUGurKJWlGqDH_9SpVxzOxf2jJfN21dz-p8czujNqsHYEwcCVXxQvqt6IC_zEVs66grZskNtaQk0J2w3uJ61QXIOmorbT_thmvYwq3bJQyJsrBvuIg1r-MOx9ASAhE9XpTO5AuM9sGnML8zugu2-X704W5b6dOKAsBZbn_VUF4g7X7S-KER1EfykyMrZV3J4UKPBtWRXE9Dre9tKYU7z_6yGHzbGVgtXe2JDCSusDWWJ_EqCgatK4Sn4mCJgh_QmWaqc6ztFaXB-vFI6KSeeDGKlJD6YIRbjs4gL2HEiAYyXSLHg87PaWQ6cgJjKRxJpfLtvAotyY9vKJi6i4Ao1jq9xMJo88EMCvsgHtE0Ng3CdHcYqqkR80EvxJBi4hH5NZGiKq26qjeZ3vm4zrF7u3fEK3jjxoTXVym7r6JMg4wk3Rqcyj2kGwLpqgXzTfLz1tLofUySnv6zGDDMXVWdz5l57tqaixUwJzHRarPEq_eSeLkRHXOX4l1k4dHpttFxkrLrArN6w4xdTCFIXvALd6Xi7v0mQUSjGHaYAkE2vT-_Pr0PMGXf2CbgksUXuIqg_8'
        }

        response = requests.post(url, headers=headers, data=audio_file)

        if response.status_code == 200:
            result_json = response.json()
            result_text = result_json.get('resultText')
            return result_text

        else:
            print(f"Error in convert_audio_to_text: {response.status_code}, {response.text}")
            return None

    except ValueError as ve:
        # Handle short audio file error
        print(f"Error in convert_audio_to_text: {ve}")
        return None

    except Exception as e:
        # Handle other exceptions
        print(f"Error in convert_audio_to_text: {e}")
        return None