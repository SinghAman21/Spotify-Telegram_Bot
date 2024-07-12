import requests
import time

bot_token = "7018446126:AAF7gV7U06k3gimCBj58V_XPoOI1pnfoi3w"   #Example token
base_url = f"https://api.telegram.org/bot{bot_token}"
get_update_url = f"{base_url}/getUpdates"
offset = 0

while True:
    try:
        params = {
            "offset": offset,
            "limit": 100,
            "timeout": 30
        }
        response = requests.get(get_update_url, params=params).json()

        if "result" in response:
            for update in response["result"]:
                if "message" in update and "text" in update["message"]:
                    song_url = update["message"]["text"]
                    chat_id = update["message"]["chat"]["id"]

                    # API CALLING
                    url = "https://spotify-downloader9.p.rapidapi.com/downloadSong"
                    querystring = {"songId": song_url}
                    headers = {
                        "x-rapidapi-key": "1162fa6edbmsh4e3ada3ee7a56eap10e77ajsn2a5e57cad3bc",
                        "x-rapidapi-host": "spotify-downloader9.p.rapidapi.com"
                    }

                    response = requests.get(url, headers=headers, params=querystring).json()

                    # DATA FETCHING
                    if "data" in response:
                        artist_name = response["data"]["artist"]
                        song_name = response["data"]["title"]
                        downloadable = response["data"]["downloadLink"]
                        cover = response["data"]["cover"]
                    
                    
                        '''
                        for data in response:
                            if "data" in data and "artist" in response["data"]:
                                artist_name = (response["data"]["artist"])
                                song_name = (response["data"]["title"])
                                downloadable = (response["data"]["downloadLink"])
                                cover = (response["data"]["cover'])  there is issue for this using for loop so its better to use the below code
                        '''


                        return_text = f"{song_name} by {artist_name}\nDownload your song: {downloadable}\nPS: Link will expire soon!!"
                        
                        # Send the photo with the caption
                        send_photo_url = f"{base_url}/sendPhoto"
                        photo_params = {
                            "chat_id": chat_id,
                            "photo": cover,
                            "caption": return_text
                        }
                        photo_response = requests.get(send_photo_url, params=photo_params).json()

                        # Download the audio file
                        audio_content = requests.get(downloadable).content
                        audio_file = {'audio': ('audio.mp3', audio_content)}
                        send_audio_url = f"{base_url}/sendAudio"
                        audio_params = {
                            "chat_id": chat_id
                        }
                        audio_response = requests.post(send_audio_url, data=audio_params, files=audio_file).json()
                    
                    elif song_url == "/start":
                        send_message_url = f"{base_url}/sendMessage"
                        text_params = {
                            "chat_id": chat_id,
                            "text": "Please paste the link of the song you wish to download"
                        }
                        response = requests.get(send_message_url, params=text_params).json()

                    else:
                        send_message_url = f"{base_url}/sendMessage"
                        text_params = {
                            "chat_id": chat_id,
                            "text": "Please check the URL of the song"
                        }
                        response = requests.get(send_message_url, params=text_params).json()

                # Update offset
                offset = update["update_id"] + 1

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(10)  # Wait for 10 seconds before retrying

    # Pause briefly to reduce load
    time.sleep(1)
