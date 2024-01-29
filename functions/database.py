import os
import json
import random

# Save messages for retrieval later on
def get_recent_messages():

  # Define the file name
  file_name = "stored_data.json"
  learn_instruction = {"role": "system", 
                       "content": "3-12 yaş arasındaki Otizmli çocuklara yönelik bir eğitim robotusun. Senin adın JoyBot. Cevaplarını 15 kelime altında tutmaya özen göster. Sadecce Türkçe konuş. Sohbeti devam ettirmek için iletişimde kullanılan olumlu sonuç (positive consequence) ve request  for repair / conversitional repair metorlarını kullanarak sohbeti devam ettir."}
  
  # Initialize messages
  messages = []

  # Add Random Element
  x = random.uniform(0, 1)
  if x < 0.2:
    learn_instruction["content"] = learn_instruction["content"] + "çocuğun sevdiği hobileri bul ve sohbeti devam ettir"
  elif x < 0.5:
    learn_instruction["content"] = learn_instruction["content"] + "Çocuğun duygu durumunu öğren ve sohbeti devam ettir"
  else:
    learn_instruction["content"] = learn_instruction["content"] + ""

  # Append instruction to message
  messages.append(learn_instruction)

  # Get last messages
  try:
    with open(file_name) as user_file:
      data = json.load(user_file)
      
      # Append last 5 rows of data
      if data:
        if len(data) < 5:
          for item in data:
            messages.append(item)
        else:
          for item in data[-5:]:
            messages.append(item)
  except:
    pass

  
  # Return messages
  return messages


# Save messages for retrieval later on
def store_messages(request_message, response_message):

  # Define the file name
  file_name = "stored_data.json"

  # Get recent messages
  messages = get_recent_messages()[1:]

  # Add messages to data
  user_message = {"role": "user", "content": request_message}
  assistant_message = {"role": "assistant", "content": response_message}
  messages.append(user_message)
  messages.append(assistant_message)

  # Save the updated file
  with open(file_name, "w") as f:
    json.dump(messages, f)


# Save messages for retrieval later on
def reset_messages():

  # Define the file name
  file_name = "stored_data.json"

  # Write an empty file
  open(file_name, "w")
