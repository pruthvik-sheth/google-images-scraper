
# Google Images Scraper

Google Images Scraper is a Python tool designed to scrape high-resolution images from Google Images based on provided links. It overcomes the limitations of some browser extensions that only download image thumbnails.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/google-images-scraper.git
   ```

2. Navigate to the project directory:

   ```bash
   cd google-images-scraper
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the scraper by executing the following command:

   ```bash
   python scraper.py
   ```

   This script will fetch high-resolution images from Google Images based on the provided links.

## Configuration

You can customize the behavior of the scraper by modifying the `sources.py` file.

- `CATEGORY_URLS`: Add the Google Images URLs for different categories you want to scrape.
- `IMAGE_LIMIT`: Set the maximum number of images to download per category.
- `CSV_DOWNLOAD_PATH`: Path to save CSV files containing image metadata.
- `IMAGE_DOWNLOAD_PATH`: Path to save downloaded images.
- `LABEL_SAVE_PATH`: Path to save labels or categories.
- `CATEGORIES`: List of categories to scrape.
- `SAVE_BATCH_SIZE`: Number of images to save in a batch.

## Project Structure

- `csv_downloads`: Directory to store CSV files.
- `image_downloads`: Directory to store downloaded images.
- `labels`: Directory to save labels or categories.
- `downloader.py`: Contains functions to download images.
- `email_service.py`: Provides functionality for email notifications (if needed).
- `scraper.py`: The main script to initiate the scraping process.
- `sources.py`: Configuration file to set up URLs and other parameters.

## Contributing

Contributions to Google Images Scraper are welcome and encouraged! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test thoroughly.
4. Commit your changes with descriptive commit messages.
5. Push your changes to your fork.
6. Open a pull request, explaining the changes you've made.

## License

This project is licensed under the [MIT License](LICENSE).