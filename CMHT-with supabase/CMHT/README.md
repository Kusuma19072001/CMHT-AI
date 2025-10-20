# College Voice Assistant

A voice-enabled web application that helps users find faculty room locations by speaking to the assistant.

## Features

- Voice recognition using browser's built-in Speech Recognition API
- Faculty room database with common professor names
- Simple and intuitive web interface
- Real-time voice processing

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- A modern web browser with microphone support (Chrome, Firefox, Safari, Edge)

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:8080
```

4. Allow microphone access when prompted by your browser.

## How to Use

1. Click the "🎤 Speak" button
2. Ask about a faculty member's room location (e.g., "Where is Dr. Smith's office?")
3. The assistant will respond with the room location

## Supported Faculty Members

The assistant currently knows about these faculty members:
- Dr. Smith (Computer Science)
- Dr. Johnson (Mathematics)
- Dr. Williams (Physics)
- Dr. Brown (Chemistry)
- Dr. Davis (Biology)
- Dr. Miller (Engineering)
- Dr. Wilson (Business)
- Dr. Moore (Arts)

## Customization

You can add more faculty members by editing the `faculty_rooms` dictionary in `app.py`.

## Troubleshooting

- Make sure your browser supports Speech Recognition API
- Ensure microphone permissions are granted
- Check that the Flask server is running on port 5000
- If using HTTPS, you may need to use a local development certificate

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

Note: Speech Recognition works best in Chrome and may have limited functionality in other browsers. 