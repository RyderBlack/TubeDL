
# TubeDL

TubeDL is a simple and efficient Tube downloader with a modern GUI that allows users to download videos in either MP3 or MP4 format.


## Features

- Clean and modern user interface
- Download Tube videos as MP3 or MP4
- Multiple quality options for both formats
- Simple and intuitive design
- Downloads saved in organized folder structure

## Prerequisites

Before you begin, ensure you have met the following requirements:
* Python 3.8 or higher installed
* FFmpeg installed on your system
* Internet connection

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/RyderBlack/TubeDL.git
cd TubeDL
```

### 2. Install FFmpeg:

#### Windows:
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Or use Chocolatey: `choco install ffmpeg`
- Or use Scoop: `scoop install ffmpeg`

#### MacOS:
```bash
brew install ffmpeg
```

#### Linux:
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 4. If tkinter is missing:
#### Windows:
- Reinstall Python with tcl/tk option checked

#### Linux:
```bash
sudo apt-get install python3-tk
```

#### MacOS:
```bash
brew install python-tk
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter a Tube URL in the input field
3. Select your desired format (MP3 or MP4)
4. Click the Download button
5. Find your downloaded files in the 'downloads' folder

## File Structure

```
TubeDL/
│
├── main.py           # Main application file
├── requirements.txt  # Python dependencies
├── README.md        # This file
└── downloads/       # Downloaded files directory
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Dependencies

- customtkinter
- yt-dlp
- ffmpeg-python

## Known Issues

- Some videos might not be available for download due to YT's restrictions
- Download speed depends on your internet connection
- Some high-quality videos might take longer to process

## Troubleshooting

### Common Issues:

1. **FFmpeg not found**
   - Make sure FFmpeg is properly installed and added to your system's PATH

2. **Download fails**
   - Check your internet connection
   - Verify the Tube link is valid
   - Ensure you have write permissions in the downloads directory

3. **GUI doesn't launch**
   - Verify tkinter is properly installed
   - Check Python version compatibility

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact


Project Link: [https://github.com/RyderBlack/TubeDL](https://github.com/RyderBlack/TubeDL)

## Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
