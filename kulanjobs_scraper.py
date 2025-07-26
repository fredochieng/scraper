#!/usr/bin/env python3
"""
KulanJobs.com Web Scraper
Scrapes job listings from kulanjobs.com and saves them to JSON format.

Features:
- Extracts job title, category, posting date, organization, job type
- Handles pagination
- Saves results to JSON file
- Includes error handling and rate limiting
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KulanJobsScraper:
    def __init__(self, base_url="https://kulanjobs.com", delay=1):
        self.base_url = base_url
        self.delay = delay  # Delay between requests to be respectful
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.jobs = []
    
    def get_page(self, url):
        """Fetch a page with error handling and rate limiting."""
        try:
            time.sleep(self.delay)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_job_links(self, soup):
        """Extract job links from the jobs listing page."""
        job_links = []
        
        # Look for job title links - they appear to be in h3 tags with links
        job_title_links = soup.find_all('a', href=re.compile(r'/job/'))
        
        for link in job_title_links:
            href = link.get('href')
            if href:
                full_url = urljoin(self.base_url, href)
                job_links.append(full_url)
        
        return list(set(job_links))  # Remove duplicates
    
    def parse_job_details(self, job_url):
        """Parse individual job page to extract details."""
        response = self.get_page(job_url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_data = {
            'url': job_url,
            'title': '',
            'organization': '',
            'location': '',
            'date_posted': '',
            'job_type': '',
            'category': '',
            'description': '',
            'scraped_at': datetime.now().isoformat()
        }
        
        try:
            # Extract job title - usually the first heading or in title
            title_elem = soup.find('h1') or soup.find('h2') or soup.find('h3')
            if title_elem:
                job_data['title'] = title_elem.get_text(strip=True)
            else:
                # Fallback to page title
                title_tag = soup.find('title')
                if title_tag:
                    job_data['title'] = title_tag.get_text(strip=True).split(' - ')[0]
            
            # Extract organization - often appears after the job title
            # Look for patterns like "Company Name" or organization info
            text_content = soup.get_text()
            
            # Try to find organization in structured format
            org_patterns = [
                r'([A-Z][A-Za-z\s&\(\)\.]+(?:Foundation|Organization|Council|International|Relief|School|Company|Ltd|Inc|Corp))',
                r'Position:\s*([^,\n]+)',
                r'Organization:\s*([^,\n]+)',
                r'Company:\s*([^,\n]+)'
            ]
            
            for pattern in org_patterns:
                match = re.search(pattern, text_content)
                if match:
                    job_data['organization'] = match.group(1).strip()
                    break
            
            # Extract location
            location_patterns = [
                r'Location:\s*([^,\n]+)',
                r'([A-Za-z\s]+,\s*[A-Za-z\s]+)(?:\s*Date Posted)',
                r'Sheikh|Somaliland|Somalia|Kenya|Ethiopia|Rwanda|Nairobi|London'
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text_content)
                if match:
                    job_data['location'] = match.group(1).strip() if match.groups() else match.group(0)
                    break
            
            # Extract date posted
            date_patterns = [
                r'Date Posted:\s*([^,\n]+)',
                r'Posted:\s*([^,\n]+)',
                r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, text_content)
                if match:
                    job_data['date_posted'] = match.group(1).strip() if match.groups() else match.group(0)
                    break
            
            # Extract job type - look for contract type, employment type
            job_type_patterns = [
                r'Contract Type:\s*([^,\n]+)',
                r'Employment Type:\s*([^,\n]+)',
                r'Job Type:\s*([^,\n]+)',
                r'(Full[- ]?time|Part[- ]?time|Contract|Temporary|Permanent|Fixed Term)'
            ]
            
            for pattern in job_type_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    job_data['job_type'] = match.group(1).strip() if match.groups() else match.group(0)
                    break
            
            # Extract category - try to determine from content
            category_keywords = {
                'Education': ['teacher', 'education', 'school', 'training', 'academic'],
                'Healthcare': ['medical', 'health', 'doctor', 'nurse', 'clinic'],
                'Engineering': ['engineer', 'technical', 'electrician', 'plumber', 'maintenance'],
                'Administration': ['admin', 'secretary', 'clerk', 'office', 'administrative'],
                'NGO/Development': ['ngo', 'development', 'humanitarian', 'relief', 'foundation'],
                'IT/Technology': ['it', 'technology', 'software', 'computer', 'network'],
                'Finance': ['finance', 'accounting', 'accountant', 'financial'],
                'Management': ['manager', 'management', 'director', 'supervisor', 'coordinator']
            }
            
            content_lower = text_content.lower()
            for category, keywords in category_keywords.items():
                if any(keyword in content_lower for keyword in keywords):
                    job_data['category'] = category
                    break
            
            # Extract description - get main content
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content and clean it
            description = soup.get_text()
            # Clean up whitespace
            description = re.sub(r'\s+', ' ', description).strip()
            # Limit description length
            job_data['description'] = description[:2000] + '...' if len(description) > 2000 else description
            
        except Exception as e:
            logger.error(f"Error parsing job details for {job_url}: {e}")
        
        return job_data
    
    def scrape_jobs_page(self, page_url):
        """Scrape jobs from a single page."""
        logger.info(f"Scraping page: {page_url}")
        
        response = self.get_page(page_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        job_links = self.extract_job_links(soup)
        
        logger.info(f"Found {len(job_links)} job links on page")
        
        page_jobs = []
        for job_url in job_links:
            logger.info(f"Scraping job: {job_url}")
            job_data = self.parse_job_details(job_url)
            if job_data:
                page_jobs.append(job_data)
        
        return page_jobs
    
    def scrape_all_jobs(self, max_pages=5):
        """Scrape jobs from multiple pages."""
        logger.info("Starting KulanJobs scraping...")
        
        # Start with the main jobs page
        base_jobs_url = f"{self.base_url}/jobs"
        
        for page in range(1, max_pages + 1):
            if page == 1:
                page_url = base_jobs_url
            else:
                page_url = f"{base_jobs_url}?page={page}"
            
            page_jobs = self.scrape_jobs_page(page_url)
            
            if not page_jobs:
                logger.info(f"No jobs found on page {page}, stopping pagination")
                break
            
            self.jobs.extend(page_jobs)
            logger.info(f"Scraped {len(page_jobs)} jobs from page {page}")
        
        logger.info(f"Total jobs scraped: {len(self.jobs)}")
        return self.jobs
    
    def save_to_json(self, filename="kulanjobs_data.json"):
        """Save scraped jobs to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'scraped_at': datetime.now().isoformat(),
                    'total_jobs': len(self.jobs),
                    'source': 'kulanjobs.com',
                    'jobs': self.jobs
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Data saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            return False
    
    def get_summary(self):
        """Get summary statistics of scraped data."""
        if not self.jobs:
            return "No jobs scraped yet."
        
        summary = {
            'total_jobs': len(self.jobs),
            'organizations': len(set(job['organization'] for job in self.jobs if job['organization'])),
            'categories': {},
            'job_types': {},
            'locations': {}
        }
        
        for job in self.jobs:
            # Count categories
            category = job.get('category', 'Unknown')
            summary['categories'][category] = summary['categories'].get(category, 0) + 1
            
            # Count job types
            job_type = job.get('job_type', 'Unknown')
            summary['job_types'][job_type] = summary['job_types'].get(job_type, 0) + 1
            
            # Count locations
            location = job.get('location', 'Unknown')
            summary['locations'][location] = summary['locations'].get(location, 0) + 1
        
        return summary

def main():
    """Main function to run the scraper."""
    scraper = KulanJobsScraper(delay=2)  # 2 second delay between requests
    
    try:
        # Scrape jobs (limit to 3 pages for initial run)
        jobs = scraper.scrape_all_jobs(max_pages=3)
        
        if jobs:
            # Save to JSON
            scraper.save_to_json("kulanjobs_data.json")
            
            # Print summary
            summary = scraper.get_summary()
            print("\n" + "="*50)
            print("SCRAPING SUMMARY")
            print("="*50)
            print(f"Total jobs scraped: {summary['total_jobs']}")
            print(f"Unique organizations: {summary['organizations']}")
            print(f"\nTop categories:")
            for category, count in sorted(summary['categories'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {category}: {count}")
            print(f"\nTop job types:")
            for job_type, count in sorted(summary['job_types'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {job_type}: {count}")
            print(f"\nTop locations:")
            for location, count in sorted(summary['locations'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {location}: {count}")
            
        else:
            print("No jobs were scraped. Please check the website structure or network connection.")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
        if scraper.jobs:
            scraper.save_to_json("kulanjobs_data_partial.json")
            print("Partial data saved.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()

