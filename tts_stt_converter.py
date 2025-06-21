"""
Text-Speech Converter Tool (TTS & STT)
--------------------------------------

This tool allows:
- Text to Speech conversion using gTTS
- Speech to Text conversion using SpeechRecognition

Features:
- CLI arguments with argparse
- Error handling (PermissionError, FileNotFoundError)
- Logging (professional format)
- Configurable paths and settings
- Modular functions with docstrings
"""

import os
import sys
import argparse
import configparser
import logging
import shutil
from gtts import gTTS
import speech_recognition as sr
 

# Load Config
config = configparser.ConfigParser()
config.read('config.ini')

# Setup Logging
log_file = config.get('Logging', 'log_file', fallback='logs/converter.log')
log_level = config.get('Logging', 'log_level', fallback='INFO')

os.makedirs(os.path.dirname(log_file), exist_ok=True)

logger = logging.getLogger('TextSpeechLogger')
logger.setLevel(getattr(logging, log_level, logging.INFO))

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
logger.addHandler(console_handler)

def convert_text_to_speech(text: str, output_path: str):
    """Convert text to speech and save as mp3"""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        logging.info(f'Speech saved to: {output_path}')
        print(f'Speech saved to: {output_path}')

    except PermissionError as pe:
        logger.error(f'Permission denied while saving file: {pe}')
    except Exception as err:
        logger.error(f"Unexpected error occured in TTS: {err}")

def convert_speech_to_text(audio_path: str, output_path: str, language='en'):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as file:
            audio = recognizer.record(file)
        text = recognizer.recognize_google(audio, language= language)
        with open (output_path, 'w', encoding='utf-8') as f:
            f.write(text)

    except FileNotFoundError as err:
        logger.error(f'Audio file not found: {err}')
    except sr.UnknownValueError:
        logger.error('Speech was unintelligible.') 
    except sr.RequestError as re:
        logger.error(f'Sppech recognition API error: {re}')
    except Exception as err:
        logger.error(f'Unexpected error in STT: {err}')

def parse_cli_args():
    """Parse CLI arguments using argparse."""
    parser = argparse.ArgumentParser(description='Text to Speech and Speech to Text converter tool.')
    subpersers = parser.add_subparsers(dest='command', help="Choose 'tts' or 'stt'")

    tts_parser = subpersers.add_parser('tts', help='Convert text to speech')
    tts_parser.add_argument('--text', type=str, required=True, help='Text to convert to speech')

    stt_parser = subpersers.add_parser('stt', help='Convert speech to text')
    stt_parser.add_argument('--audio', type=str, required=True, help='Path to audio file(.wav)')
    stt_parser.add_argument('--lang', type=str, default='en', help='Language code for recognition (default: en)')

    return parser.parse_args()

def main():
    """Main controller function"""
    args = parse_cli_args()

    if args.command == 'tts':
        output_file = config.get('TTS', 'output_file', fallback='output/speech_output.mp3')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        convert_text_to_speech(args.text, output_file)

    elif args.command == 'stt':
        output_file = config.get('STT', 'output_file', fallback='output/text_output.txt')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        convert_speech_to_text(args.audio, output_file, args.lang)

    else:
        print("❌ Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()