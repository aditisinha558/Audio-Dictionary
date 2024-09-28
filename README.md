# Personalized Audio Dictionary

An interactive dictionary application that allows users to search for word definitions, hear their pronunciations using text-to-speech, and maintain a history of searched words. The application features user registration, login, and personalized greetings.

## Features

- **User Authentication**: Register new users and login for personalized experience.
- **Word Search**: Fetch definitions and example sentences for words from the internet.
- **Text-to-Speech**: Generate and play audio pronunciations of the searched words.
- **History**: Save and view history of searched words for each user.
- **Interactive GUI**: Easy-to-use graphical interface built with Tkinter.

## Requirements

- Python 3.x
- Required Python packages:
  - `tkinter` (usually included with Python)
  - `gtts`
  - `requests`
  - `beautifulsoup4`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/personalized-audio-dictionary.git
    cd personalized-audio-dictionary
    ```

2. Create a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Register a new user or login with an existing user.
3. Enter a word to search for its definition.
4. The application will fetch the definition and create an audio file to play its pronunciation.
5. View history of searched words by clicking on "Show Searched Words".

## Project Structure

- `main.py`: Main application file containing all the logic and GUI setup.
- `users.json`: File used to store registered users and their search history.

## Screenshots

![Image](https://github.com/user-attachments/assets/e70c9e3b-94fd-4836-b4c7-653529c44bd3)
![Image](https://github.com/user-attachments/assets/be4b32cc-524e-417e-b4b4-4d9765d90e1e)
![Image](https://github.com/user-attachments/assets/c032085c-dd19-48e8-8976-f5660a7ae1d3)
![Image](https://github.com/user-attachments/assets/1ac7d2d5-5043-412f-906a-98df1d79239c)



## Acknowledgments

- [Google Text-to-Speech (gTTS)](https://pypi.org/project/gTTS/)
- [Requests: HTTP for Humans](https://pypi.org/project/requests/)
- [BeautifulSoup: Library for scraping websites](https://pypi.org/project/beautifulsoup4/)
