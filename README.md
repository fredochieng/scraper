# KulanJobs.com Web Scraper

A Python web scraper for extracting job listings from kulanjobs.com, a popular job board for East Africa.

## Features

- **Comprehensive Data Extraction**: Scrapes job title, organization, location, posting date, job type, category, and full description
- **Smart Categorization**: Automatically categorizes jobs based on content analysis
- **Rate Limiting**: Respectful scraping with configurable delays between requests
- **Error Handling**: Robust error handling for network issues and parsing errors
- **JSON Output**: Saves results in structured JSON format
- **Pagination Support**: Can scrape multiple pages of job listings
- **Summary Statistics**: Provides insights into scraped data

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd scraper
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings:
```bash
python kulanjobs_scraper.py
```

This will:
- Scrape up to 3 pages of job listings
- Save results to `kulanjobs_data.json`
- Display a summary of scraped data

### Advanced Usage

You can customize the scraper by modifying the parameters in the `main()` function:

```python
# Create scraper with custom delay (seconds between requests)
scraper = KulanJobsScraper(delay=3)

# Scrape more pages
jobs = scraper.scrape_all_jobs(max_pages=10)

# Save to custom filename
scraper.save_to_json("my_jobs_data.json")
```

### Programmatic Usage

```python
from kulanjobs_scraper import KulanJobsScraper

# Initialize scraper
scraper = KulanJobsScraper(delay=2)

# Scrape jobs
jobs = scraper.scrape_all_jobs(max_pages=5)

# Access individual job data
for job in jobs:
    print(f"Title: {job['title']}")
    print(f"Organization: {job['organization']}")
    print(f"Location: {job['location']}")
    print(f"Date Posted: {job['date_posted']}")
    print("-" * 40)

# Get summary statistics
summary = scraper.get_summary()
print(f"Total jobs: {summary['total_jobs']}")
```

## Output Format

The scraper saves data in JSON format with the following structure:

```json
{
  "scraped_at": "2025-01-26T19:21:24.123456",
  "total_jobs": 47,
  "source": "kulanjobs.com",
  "jobs": [
    {
      "url": "https://kulanjobs.com/job/electrician-4170",
      "title": "Electrician",
      "organization": "Pharo Foundation",
      "location": "Sheikh, Somaliland",
      "date_posted": "Jul 26, 2025",
      "job_type": "Fixed Term",
      "category": "Engineering",
      "description": "Job description text...",
      "scraped_at": "2025-01-26T19:21:24.123456"
    }
  ]
}
```

## Data Fields

Each job entry contains the following fields:

- **url**: Direct link to the job posting
- **title**: Job title/position name
- **organization**: Hiring organization/company name
- **location**: Job location (city, country)
- **date_posted**: When the job was posted
- **job_type**: Employment type (Full-time, Contract, etc.)
- **category**: Auto-categorized job category
- **description**: Full job description (truncated to 2000 chars)
- **scraped_at**: Timestamp when the job was scraped

## Categories

The scraper automatically categorizes jobs into:

- Education
- Healthcare
- Engineering
- Administration
- NGO/Development
- IT/Technology
- Finance
- Management

## Rate Limiting

The scraper includes built-in rate limiting to be respectful to the website:
- Default delay: 1 second between requests
- Configurable delay parameter
- Proper User-Agent headers
- Session management for efficient requests

## Error Handling

- Network timeouts and connection errors
- Invalid HTML parsing
- Missing data fields
- Graceful degradation when data is unavailable

## Logging

The scraper includes comprehensive logging:
- INFO level: Progress updates and statistics
- ERROR level: Network and parsing errors
- Timestamps for all log entries

## Legal and Ethical Considerations

- This scraper is designed for educational and research purposes
- Always respect the website's robots.txt and terms of service
- Use reasonable delays between requests
- Don't overload the server with too many concurrent requests
- Consider reaching out to the website owners for permission for large-scale scraping

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

