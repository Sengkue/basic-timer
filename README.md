# Office Timer - Desktop Timer Application

A simple desktop timer application built with Python and Tkinter that plays a sound and flashes the screen when the timer finishes.

## Features

- ✅ Set timer in minutes and seconds
- ✅ Real-time countdown display
- ✅ Plays your `timer.mp3` file when finished
- ✅ Screen flash notification (red/white alternating)
- ✅ Clean, simple GUI with "Office Timer" title
- ✅ Start/Stop functionality
- ✅ Input validation
- ✅ Runs offline without internet

## Requirements

- Python 3.6 or higher
- Windows OS

## Installation & Setup

### Step 1: Install Python Dependencies

Open PowerShell in the timer directory and run:

```powershell
pip install -r requirements.txt
```

Or install manually:
```powershell
pip install pygame==2.5.2 pyinstaller==6.1.0
```

### Step 2: Test the Application

Run the Python script directly:
```powershell
python timer.py
```

### Step 3: Create Standalone .exe File

To convert the Python script to a standalone .exe file that can run on any Windows machine:

```powershell
pyinstaller --onefile --windowed --add-data "timer.mp3;." timer.py
```

**Alternative command (simpler):**
```powershell
pyinstaller --onefile --windowed timer.py
```

Then manually copy `timer.mp3` to the same directory as the generated .exe file.

### Step 4: Find Your .exe File

After running pyinstaller, your executable will be located at:
```
dist/timer.exe
```

### Step 5: Distribute Your Application

To distribute your timer application:

1. Copy `timer.exe` from the `dist/` folder
2. Copy `timer.mp3` to the same folder as `timer.exe`
3. Both files must be in the same directory for the sound to work

## Usage

1. Launch `timer.exe` (or run `python timer.py`)
2. Enter desired minutes and seconds (default is 5 minutes)
3. Click "Start" to begin countdown
4. Click "Stop" to cancel timer if needed
5. When time is up:
   - Screen will flash red and white
   - Your `timer.mp3` will play
   - A popup message will appear

## File Structure

```
timer/
├── timer.py          # Main application code
├── timer.mp3         # Sound file (your provided audio)
├── requirements.txt  # Python dependencies
├── README.md        # This file
└── dist/            # Generated after pyinstaller
    └── timer.exe    # Standalone executable
```

## Troubleshooting

**Sound not playing:**
- Ensure `timer.mp3` is in the same directory as `timer.exe`
- If sound still doesn't work, the app will fall back to system beep

**Application won't start:**
- Make sure you have Python 3.6+ installed
- Install pygame: `pip install pygame`
- Check that all files are in the correct locations

**Build issues:**
- Make sure pyinstaller is installed: `pip install pyinstaller`
- Try the alternative pyinstaller command above
- Ensure you're in the correct directory when running commands

## Technical Notes

- Uses Tkinter for GUI (built into Python, no extra installation needed)
- Uses pygame for MP3 audio playback
- Multi-threaded design prevents GUI freezing during countdown
- Handles both .py script execution and .exe standalone execution
- Input validation prevents invalid timer settings
- Graceful error handling with fallbacks"# basic-timer" 
