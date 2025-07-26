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
        
        # Define thematic keywords for filtering
        self.thematic_keywords = {
            'WASH': [
                'wash', 'water supply', 'sanitation', 'hygiene promotion', 'hygiene behavior change',
                'water resource management', 'wastewater', 'handwashing', 'open defecation',
                'wash infrastructure', 'menstrual hygiene management', 'faecal sludge management',
                'water', 'sanitation', 'hygiene'
            ],
            'Health': [
                'public health', 'primary health care', 'maternal and child health', 'reproductive health',
                'nutrition', 'non-communicable diseases', 'ncds', 'mental health and psychosocial support',
                'mhpss', 'sexual and reproductive health', 'srhr', 'epidemic response',
                'community health workers', 'disease surveillance', 'health systems strengthening',
                'universal health coverage', 'uhc', 'health financing', 'health', 'medical', 'healthcare'
            ],
            'Livelihoods': [
                'livelihood support', 'food security', 'income generation', 'agriculture and farming',
                'micro-enterprise development', 'vocational training', 'economic empowerment',
                'cash transfer programming', 'market-based interventions', 'smallholder support',
                'resilience building', 'livelihoods', 'agriculture', 'farming', 'economic'
            ],
            'Displacement & Protection': [
                'internally displaced persons', 'idps', 'refugee support', 'returnee integration',
                'camp management', 'emergency shelter', 'forced migration', 'durable solutions',
                'humanitarian assistance', 'resettlement', 'transitional shelter', 'protection services',
                'displacement', 'refugee', 'protection', 'humanitarian'
            ]
        }
        
        # Project type/activity keywords
        self.project_keywords = [
            'consultancy', 'evaluation', 'baseline', 'endline', 'impact assessment', 'research',
            'feasibility study', 'technical assistance', 'capacity building', 'program design',
            'third-party monitoring', 'proposal development', 'needs assessment',
            'implementation support', 'institutional strengthening', 'data collection',
            'strategic planning', 'monitoring', 'assessment', 'consultant'
        ]
        
        # Geographic/contextual keywords
        self.geographic_keywords = [
            'kenya', 'uganda', 'ethiopia', 'somalia', 'somaliland', 'horn of africa',
            'sub-saharan africa', 'fragile contexts', 'post-conflict settings',
            'east africa', 'africa'
        ]
    
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
    
    def parse_date(self, date_str):
        """Parse date string and return days ago."""
        if not date_str:
            return None
        
        try:
            # Handle different date formats
            date_str = date_str.strip().lower()
            
            # Handle "Jul 26, 2025" format
            if ',' in date_str:
                date_obj = datetime.strptime(date_str, '%b %d, %Y')
                days_ago = (datetime.now() - date_obj).days
                return days_ago
            
            # Handle "Jul 26" format (assume current year)
            elif len(date_str.split()) == 2:
                current_year = datetime.now().year
                date_obj = datetime.strptime(f"{date_str}, {current_year}", '%b %d, %Y')
                days_ago = (datetime.now() - date_obj).days
                return days_ago
            
            # Handle relative dates like "2 days ago", "1 week ago"
            if 'day' in date_str and 'ago' in date_str:
                days = int(re.search(r'(\d+)', date_str).group(1))
                return days
            elif 'week' in date_str and 'ago' in date_str:
                weeks = int(re.search(r'(\d+)', date_str).group(1))
                return weeks * 7
            elif 'month' in date_str and 'ago' in date_str:
                months = int(re.search(r'(\d+)', date_str).group(1))
                return months * 30
                
        except Exception as e:
            logger.warning(f"Could not parse date '{date_str}': {e}")
        
        return None
    
    def matches_thematic_filter(self, job_text, themes=None):
        """Check if job matches specified thematic keywords."""
        if not themes:
            return True
        
        job_text_lower = job_text.lower()
        
        for theme in themes:
            if theme in self.thematic_keywords:
                keywords = self.thematic_keywords[theme]
                if any(keyword in job_text_lower for keyword in keywords):
                    return True
        
        return False
    
    def matches_project_filter(self, job_text, require_project_keywords=False):
        """Check if job matches project type keywords."""
        if not require_project_keywords:
            return True
        
        job_text_lower = job_text.lower()
        return any(keyword in job_text_lower for keyword in self.project_keywords)
    
    def matches_geographic_filter(self, job_text, geographic_focus=None):
        """Check if job matches geographic keywords."""
        if not geographic_focus:
            return True
        
        job_text_lower = job_text.lower()
        
        if isinstance(geographic_focus, str):
            geographic_focus = [geographic_focus]
        
        # Check for specific countries/regions
        for location in geographic_focus:
            if location.lower() in job_text_lower:
                return True
        
        # Also check against our predefined geographic keywords
        return any(keyword in job_text_lower for keyword in self.geographic_keywords)
    
    def matches_date_filter(self, date_posted, max_days_ago=None):
        """Check if job was posted within specified days."""
        if not max_days_ago:
            return True
        
        days_ago = self.parse_date(date_posted)
        if days_ago is None:
            return True  # Include jobs with unparseable dates
        
        return days_ago <= max_days_ago
    
    def matches_filters(self, job_data, filters=None):
        """Check if job matches all specified filters."""
        if not filters:
            return True
        
        job_text = f"{job_data.get('title', '')} {job_data.get('description', '')} {job_data.get('organization', '')} {job_data.get('location', '')}"
        
        # Check thematic filters
        if 'themes' in filters and filters['themes']:
            if not self.matches_thematic_filter(job_text, filters['themes']):
                return False
        
        # Check project type filters
        if 'require_project_keywords' in filters:
            if not self.matches_project_filter(job_text, filters['require_project_keywords']):
                return False
        
        # Check geographic filters
        if 'geographic_focus' in filters and filters['geographic_focus']:
            if not self.matches_geographic_filter(job_text, filters['geographic_focus']):
                return False
        
        # Check date filters
        if 'max_days_ago' in filters and filters['max_days_ago']:
            if not self.matches_date_filter(job_data.get('date_posted'), filters['max_days_ago']):
                return False
        
        return True
    
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
    
    def scrape_jobs_page(self, page_url, filters=None):
        """Scrape jobs from a single page with optional filtering."""
        logger.info(f"Scraping page: {page_url}")
        
        response = self.get_page(page_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        job_links = self.extract_job_links(soup)
        
        logger.info(f"Found {len(job_links)} job links on page")
        
        page_jobs = []
        filtered_count = 0
        
        for job_url in job_links:
            logger.info(f"Scraping job: {job_url}")
            job_data = self.parse_job_details(job_url)
            
            if job_data:
                # Apply filters if specified
                if self.matches_filters(job_data, filters):
                    page_jobs.append(job_data)
                    logger.info(f"✅ Job matches filters: {job_data['title']}")
                else:
                    filtered_count += 1
                    logger.info(f"❌ Job filtered out: {job_data['title']}")
        
        if filtered_count > 0:
            logger.info(f"Filtered out {filtered_count} jobs that didn't match criteria")
        
        return page_jobs
    
    def scrape_all_jobs(self, max_pages=5, filters=None):
        """Scrape jobs from multiple pages with optional filtering."""
        logger.info("Starting KulanJobs scraping...")
        
        if filters:
            logger.info("Applied filters:")
            if 'themes' in filters and filters['themes']:
                logger.info(f"  - Themes: {', '.join(filters['themes'])}")
            if 'require_project_keywords' in filters and filters['require_project_keywords']:
                logger.info(f"  - Require project keywords: {filters['require_project_keywords']}")
            if 'geographic_focus' in filters and filters['geographic_focus']:
                logger.info(f"  - Geographic focus: {', '.join(filters['geographic_focus']) if isinstance(filters['geographic_focus'], list) else filters['geographic_focus']}")
            if 'max_days_ago' in filters and filters['max_days_ago']:
                logger.info(f"  - Max days ago: {filters['max_days_ago']}")
        
        # Start with the main jobs page
        base_jobs_url = f"{self.base_url}/jobs"
        
        for page in range(1, max_pages + 1):
            if page == 1:
                page_url = base_jobs_url
            else:
                page_url = f"{base_jobs_url}?page={page}"
            
            page_jobs = self.scrape_jobs_page(page_url, filters)
            
            if not page_jobs:
                logger.info(f"No matching jobs found on page {page}, stopping pagination")
                break
            
            self.jobs.extend(page_jobs)
            logger.info(f"Scraped {len(page_jobs)} matching jobs from page {page}")
        
        logger.info(f"Total matching jobs scraped: {len(self.jobs)}")
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
        # Example 1: Scrape all jobs (no filters)
        print("Example 1: Scraping all jobs...")
        jobs = scraper.scrape_all_jobs(max_pages=2)
        
        if jobs:
            scraper.save_to_json("kulanjobs_all_data.json")
            print(f"✅ Scraped {len(jobs)} total jobs")
        
        # Example 2: Filter for WASH and Health jobs posted in last 20 days
        print("\nExample 2: Filtering for WASH and Health jobs (last 20 days)...")
        scraper.jobs = []  # Reset jobs list
        
        filters = {
            'themes': ['WASH', 'Health'],
            'max_days_ago': 20,
            'require_project_keywords': True
        }
        
        filtered_jobs = scraper.scrape_all_jobs(max_pages=3, filters=filters)
        
        if filtered_jobs:
            scraper.save_to_json("kulanjobs_wash_health_filtered.json")
            print(f"✅ Found {len(filtered_jobs)} WASH/Health jobs with project keywords")
            
            # Show sample results
            print("\nSample filtered jobs:")
            for i, job in enumerate(filtered_jobs[:3]):
                print(f"{i+1}. {job['title']} - {job['organization']}")
                print(f"   Posted: {job['date_posted']} | Location: {job['location']}")
        
        # Print summary
        if jobs:
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
