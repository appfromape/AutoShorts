# AutoShorts

According to MPVV1 (MoneyPrinter Version 1) & MPV2 (MoneyPrinter Version 2), adapted to use the edge-tts module to generate Traditional Chinese Shorts videos.

> **Note:** AutoShorts needs Python 3.9 up to function effectively.
> Watch the YouTube video [here]()

## Features

- [x] YouTube Shorts Automater

## Installation

```bash
# Download this project
git clone https://github.com/appfromape/AutoShorts.git
cd AutoShorts

# Copy .env.example and fill out values
cp .env.example .env

# Create a virtual environment
python -m venv venv

# Activate the virtual environment - Windows
.\venv\Scripts\activate

# Activate the virtual environment - Unix
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt
```

## Usage

```bash
# Run the backend server
cd Backend
python main.py
```

## Acknowledgments

- [MoneyPrinter](https://github.com/FujiwaraChoki/MoneyPrinter)
- [MoneyPrinterV2](https://github.com/FujiwaraChoki/MoneyPrinterV2)
- [edge-tts](https://github.com/rany2/edge-tts)

## Disclaimer

This project is for educational purposes only. The author will not be responsible for any misuse of the information provided. All the information on this website is published in good faith and for general information purpose only. The author does not make any warranties about the completeness, reliability, and accuracy of this information. Any action you take upon the information you find on this website , is strictly at your own risk. The author will not be liable for any losses and/or damages in connection with the use of our website.
