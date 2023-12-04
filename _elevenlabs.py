from elevenlabs import clone, generate, play, set_api_key, VOICES_CACHE, voices
from elevenlabs.api import History
import os

#Setting up the API key for eleven labs
os.environ['ELEVENLABS_API_KEY'] = '3f27c5fbf1021f91573bc0fbe9fbd1b7'

#This function will serve to generate audio for our podcast. The voice will be custom.
#It will help in cloning voives of different people for us to use in the podcast
def with_custom_voice(podcaster, guest, Description, prompt, file_path):

    name = f'Podcast between {podcaster} and {guest}'
    temp = name.replace(' ','_')
    audio_path = f'{temp}.mp3'

    Voice = clone(name = f'Podcast between {podcaster} and {guest}', description = Description, files = [file_path,],)

    audio = generate(text = prompt, voice= Voice)

    play(audio)

    try:
        with open(audio_path, 'wb') as f:
            f.write(audio)
    except Exception as e:
        print(e)

    return ""

#Now we shall create a function to generate the voives for our podcast. These voices are premade and trained bu ElevenLabs
def with_premade_voice(prompt, voice):
    audio_path = f'{voice}.mp3'

    audio = generate(text = prompt, voice = voice, model = 'eleven_monolingual_v1')

    try:
        with open(audio_path, 'wb') as f:
            f.write(audio)
        return audio_path
    except Exception as e:
        print(e)

        return ""
    
#Now to create a helper function. This will assist in getting all available voices
def get_voices():

    names =[]

    v_list = voices()

    for v in v_list:
        names.append(v.name)
    return names





