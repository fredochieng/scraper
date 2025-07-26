#!/usr/bin/env python3
"""
Example usage of the KulanJobs scraper
This script demonstrates how to use the scraper and shows sample output.
"""

from kulanjobs_scraper import KulanJobsScraper
import json

def main():
    print("KulanJobs.com Scraper - Example Usage")
    print("=" * 50)
    
    # Initialize the scraper
    scraper = KulanJobsScraper(delay=2)  # 2 second delay between requests
    
    print("Starting to scrape jobs from kulanjobs.com...")
    print("This may take a few minutes depending on the number of jobs...")
    
    try:
        # Scrape jobs from first 2 pages (for demo purposes)
        jobs = scraper.scrape_all_jobs(max_pages=2)
        
        if jobs:
            print(f"\n✅ Successfully scraped {len(jobs)} jobs!")
            
            # Save to JSON file
            filename = "sample_kulanjobs_data.json"
            if scraper.save_to_json(filename):
                print(f"✅ Data saved to {filename}")
            
            # Display some sample jobs
            print("\n📋 Sample Jobs:")
            print("-" * 50)
            
            for i, job in enumerate(jobs[:3]):  # Show first 3 jobs
                print(f"\n{i+1}. {job['title']}")
                print(f"   Organization: {job['organization']}")
                print(f"   Location: {job['location']}")
                print(f"   Date Posted: {job['date_posted']}")
                print(f"   Job Type: {job['job_type']}")
                print(f"   Category: {job['category']}")
                print(f"   URL: {job['url']}")
            
            # Show summary statistics
            summary = scraper.get_summary()
            print(f"\n📊 Summary Statistics:")
            print("-" * 30)
            print(f"Total Jobs: {summary['total_jobs']}")
            print(f"Unique Organizations: {summary['organizations']}")
            
            print(f"\nTop Categories:")
            for category, count in sorted(summary['categories'].items(), 
                                        key=lambda x: x[1], reverse=True)[:5]:
                print(f"  • {category}: {count}")
            
            print(f"\nTop Job Types:")
            for job_type, count in sorted(summary['job_types'].items(), 
                                        key=lambda x: x[1], reverse=True)[:5]:
                print(f"  • {job_type}: {count}")
            
            print(f"\nTop Locations:")
            for location, count in sorted(summary['locations'].items(), 
                                        key=lambda x: x[1], reverse=True)[:5]:
                print(f"  • {location}: {count}")
                
        else:
            print("❌ No jobs were scraped. Please check your internet connection.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user.")
        if scraper.jobs:
            scraper.save_to_json("partial_kulanjobs_data.json")
            print("Partial data saved to partial_kulanjobs_data.json")
    
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()

