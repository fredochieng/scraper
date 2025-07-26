# KulanJobs.com Web Scraper

A Python web scraper for extracting job listings from kulanjobs.com, a popular job board for East Africa.

## Features

- **Comprehensive Data Extraction**: Scrapes job title, organization, location, posting date, job type, category, and full description
- **🎯 Advanced Filtering System**: Filter jobs by themes, project types, geography, and posting date
- **🏷️ Thematic Keywords**: Built-in support for WASH, Health, Livelihoods, and Displacement & Protection sectors
- **📋 Project Type Filtering**: Target consultancy, evaluation, assessment, and research positions
- **🌍 Geographic Filtering**: Focus on specific countries or regions (East Africa, Horn of Africa, etc.)
- **📅 Date Filtering**: Find jobs posted within specified timeframes (e.g., last 20 days)
- **🔍 Boolean-like Search**: Combine multiple criteria for precise targeting
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

### Advanced Usage with Filtering

The scraper supports powerful filtering capabilities to target specific types of jobs:

```python
from kulanjobs_scraper import KulanJobsScraper

# Create scraper
scraper = KulanJobsScraper(delay=2)

# Example 1: WASH consultancy jobs in East Africa (last 20 days)
filters = {
    'themes': ['WASH'],
    'require_project_keywords': True,
    'geographic_focus': ['Kenya', 'Uganda', 'Ethiopia', 'Somalia'],
    'max_days_ago': 20
}
jobs = scraper.scrape_all_jobs(max_pages=3, filters=filters)

# Example 2: Health evaluation jobs
filters = {
    'themes': ['Health'],
    'require_project_keywords': True,
    'max_days_ago': 30
}
jobs = scraper.scrape_all_jobs(max_pages=3, filters=filters)

# Example 3: Multiple themes with geographic focus
filters = {
    'themes': ['Livelihoods', 'Displacement & Protection'],
    'geographic_focus': ['Horn of Africa', 'Somalia'],
    'max_days_ago': 25
}
jobs = scraper.scrape_all_jobs(max_pages=3, filters=filters)
```

### Filter Options

**Thematic Filters (`themes`):**
- `'WASH'` - Water, sanitation, hygiene jobs
- `'Health'` - Public health, medical, nutrition jobs  
- `'Livelihoods'` - Agriculture, economic empowerment, food security
- `'Displacement & Protection'` - Refugee, IDP, humanitarian protection

**Project Type Filter (`require_project_keywords`):**
- `True` - Only jobs containing consultancy, evaluation, assessment, research keywords
- `False` - Include all job types (default)

**Geographic Filter (`geographic_focus`):**
- List of countries/regions: `['Kenya', 'Uganda', 'Ethiopia', 'Somalia']`
- Regional terms: `['East Africa', 'Horn of Africa', 'Sub-Saharan Africa']`

**Date Filter (`max_days_ago`):**
- Number of days: `20` (jobs posted in last 20 days)
- `None` - No date restriction (default)

### Example Scripts

**`filtered_scraping_examples.py`** - Comprehensive examples of filtering:
```bash
python filtered_scraping_examples.py
```

This script demonstrates:
- WASH consultancy jobs in East Africa
- Health evaluation and assessment positions
- Livelihoods and displacement jobs
- Recent consultancy opportunities (last 20 days)
- Custom boolean-like searches

**`example_usage.py`** - Basic usage examples:
```bash
python example_usage.py
```

### Programmatic Usage

```python
from kulanjobs_scraper import KulanJobsScraper

# Initialize scraper
scraper = KulanJobsScraper(delay=2)

# Scrape with filters
filters = {
    'themes': ['WASH', 'Health'],
    'require_project_keywords': True,
    'max_days_ago': 20
}
jobs = scraper.scrape_all_jobs(max_pages=5, filters=filters)

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
