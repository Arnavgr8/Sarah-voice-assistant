# Sarah - Voice Assistant

Sarah is a Python-based voice assistant that can help you with various tasks including system operations, web searches, entertainment, and information retrieval.

## Features

### System Operations
- Launch applications (Chrome, VS Code, Word, etc.)
- Check system status (battery, time)
- Control system functions

### Information Retrieval
- Web searches
- Wikipedia lookups
- Location information
- News updates
- Weather information

### Entertainment
- Play music on YouTube
- Tell jokes
- Search and display song lyrics

### Document Management
- Read PDF files

### Social Features
- Open social media platforms
- Send WhatsApp messages

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `config` folder and add `paths.json` for custom application paths

## Usage

Run the main script:
```bash
python sarah.py
```

### Voice Commands

- "Open [application_name]" - Launch applications
- "What's the time" - Check current time
- "Battery status" - Check battery level
- "Play [song_name]" - Play music on YouTube
- "Tell me a joke" - Get a random joke
- "Search for [query]" - Web search
- "Wikipedia [topic]" - Search Wikipedia
- "Read PDF [filename]" - Read PDF content
- "News update" - Get latest news
- "Weather in [city]" - Get weather information

## System Requirements

- Python 3.6 or higher
- Windows operating system
- Internet connection for web-based features
- Microphone for voice input
- Speakers for voice output

## Dependencies

Key dependencies are listed in `requirements.txt`. Main packages include:
- SpeechRecognition - For voice recognition
- pyttsx3 - For text-to-speech
- PyPDF2 - For PDF reading
- pywhatkit - For YouTube and WhatsApp features
- wikipedia - For Wikipedia searches
- beautifulsoup4 - For web scraping
- requests - For HTTP requests
- pywin32 - For Windows system operations

## Project Structure

```
Sarah/
├── config/           # Configuration files
├── core/             # Core functionality
│   ├── app_scanner.py    # Application detection
│   ├── speech.py         # Voice I/O
│   ├── system.py         # System operations
│   └── web.py           # Web interactions
├── features/         # Feature modules
│   ├── document.py      # Document operations
│   ├── entertainment.py # Entertainment features
│   ├── information.py   # Information retrieval
│   ├── lyrics.py        # Lyrics search
│   ├── news.py          # News updates
│   └── social.py        # Social media features
├── sarah.py         # Main script
└── settings.py      # Global settings
```

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.