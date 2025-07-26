#!/usr/bin/env python3
"""
Advanced Filtering Examples for KulanJobs Scraper
This script demonstrates various filtering capabilities for targeted job scraping.
"""

from kulanjobs_scraper import KulanJobsScraper
import json

def example_wash_consultancy():
    """Example: Find WASH consultancy jobs in East Africa."""
    print("🔍 Example 1: WASH Consultancy Jobs in East Africa")
    print("-" * 50)
    
    scraper = KulanJobsScraper(delay=1)
    
    filters = {
        'themes': ['WASH'],
        'require_project_keywords': True,
        'geographic_focus': ['Kenya', 'Uganda', 'Ethiopia', 'Somalia'],
        'max_days_ago': 30
    }
    
    jobs = scraper.scrape_all_jobs(max_pages=3, filters=filters)
    
    if jobs:
        scraper.save_to_json("wash_consultancy_jobs.json")
        print(f"✅ Found {len(jobs)} WASH consultancy jobs")
        
        for i, job in enumerate(jobs[:3]):
            print(f"\n{i+1}. {job['title']}")
            print(f"   Organization: {job['organization']}")
            print(f"   Location: {job['location']}")
            print(f"   Posted: {job['date_posted']}")
    else:
        print("❌ No WASH consultancy jobs found")
    
    return jobs

def example_health_evaluation():
    """Example: Find health evaluation and assessment jobs."""
    print("\n🔍 Example 2: Health Evaluation & Assessment Jobs")
    print("-" * 50)
    
    scraper = KulanJobsScraper(delay=1)
    
    filters = {
        'themes': ['Health'],
        'require_project_keywords': True,  # Must contain evaluation/assessment keywords
        'max_days_ago': 20
    }
    
    jobs = scraper.scrape_all_jobs(max_pages=3, filters=filters)
    
    if jobs:
        scraper.save_to_json("health_evaluation_jobs.json")
        print(f"✅ Found {len(jobs)} health evaluation jobs")
        
        for i, job in enumerate(jobs[:3]):
            print(f"\n{i+1}. {job['title']}")
            print(f"   Organization: {job['organization']}")
            print(f"   Location: {job['location']}")
            print(f"   Posted: {job['date_posted']}")
    else:
        print("❌ No health evaluation jobs found")
    
    return jobs

def example_livelihoods_displacement():
    """Example: Find livelihoods and displacement jobs."""
    print("\n🔍 Example 3: Livelihoods & Displacement Jobs")
    print("-" * 50)
    
    scraper = KulanJobsScraper(delay=1)
    
    filters = {
        'themes': ['Livelihoods', 'Displacement & Protection'],
        'geographic_focus': ['Horn of Africa', 'Somalia', 'Kenya'],
        'max_days_ago': 25
    }
    
    jobs = scraper.scrape_all_jobs(max_pages=3, filters=filters)
    
    if jobs:
        scraper.save_to_json("livelihoods_displacement_jobs.json")
        print(f"✅ Found {len(jobs)} livelihoods/displacement jobs")
        
        for i, job in enumerate(jobs[:3]):
            print(f"\n{i+1}. {job['title']}")
            print(f"   Organization: {job['organization']}")
            print(f"   Location: {job['location']}")
            print(f"   Posted: {job['date_posted']}")
    else:
        print("❌ No livelihoods/displacement jobs found")
    
    return jobs

def example_recent_consultancies():
    """Example: Find all recent consultancy jobs (last 20 days)."""
    print("\n🔍 Example 4: Recent Consultancy Jobs (Last 20 Days)")
    print("-" * 50)
    
    scraper = KulanJobsScraper(delay=1)
    
    filters = {
        'require_project_keywords': True,  # Must be consultancy/evaluation type
        'max_days_ago': 20
    }
    
    jobs = scraper.scrape_all_jobs(max_pages=3, filters=filters)
    
    if jobs:
        scraper.save_to_json("recent_consultancy_jobs.json")
        print(f"✅ Found {len(jobs)} recent consultancy jobs")
        
        # Group by theme
        theme_counts = {}
        for job in jobs:
            job_text = f"{job['title']} {job['description']}".lower()
            
            # Check which themes this job matches
            for theme, keywords in scraper.thematic_keywords.items():
                if any(keyword in job_text for keyword in keywords):
                    theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        print("\nJobs by theme:")
        for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {theme}: {count}")
        
        print("\nSample jobs:")
        for i, job in enumerate(jobs[:5]):
            print(f"{i+1}. {job['title']} - {job['organization']}")
    else:
        print("❌ No recent consultancy jobs found")
    
    return jobs

def example_custom_boolean_search():
    """Example: Custom boolean-like search combining multiple criteria."""
    print("\n🔍 Example 5: Custom Boolean Search")
    print("(WASH OR Health) AND (Evaluation OR Assessment) AND East Africa")
    print("-" * 50)
    
    scraper = KulanJobsScraper(delay=1)
    
    # First get all jobs
    all_jobs = scraper.scrape_all_jobs(max_pages=2)
    
    # Apply custom boolean logic
    matching_jobs = []
    
    for job in all_jobs:
        job_text = f"{job['title']} {job['description']} {job['location']}".lower()
        
        # (WASH OR Health)
        wash_match = any(keyword in job_text for keyword in scraper.thematic_keywords['WASH'])
        health_match = any(keyword in job_text for keyword in scraper.thematic_keywords['Health'])
        theme_match = wash_match or health_match
        
        # AND (Evaluation OR Assessment)
        project_match = any(keyword in job_text for keyword in ['evaluation', 'assessment', 'consultancy', 'baseline', 'endline'])
        
        # AND East Africa
        geo_match = any(keyword in job_text for keyword in ['kenya', 'uganda', 'ethiopia', 'somalia', 'east africa', 'horn of africa'])
        
        # Check date (last 30 days)
        days_ago = scraper.parse_date(job.get('date_posted'))
        date_match = days_ago is None or days_ago <= 30
        
        if theme_match and project_match and geo_match and date_match:
            matching_jobs.append(job)
    
    if matching_jobs:
        # Save results
        with open('custom_boolean_search_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'search_criteria': '(WASH OR Health) AND (Evaluation OR Assessment) AND East Africa',
                'total_jobs': len(matching_jobs),
                'jobs': matching_jobs
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Found {len(matching_jobs)} jobs matching custom criteria")
        
        for i, job in enumerate(matching_jobs[:3]):
            print(f"\n{i+1}. {job['title']}")
            print(f"   Organization: {job['organization']}")
            print(f"   Location: {job['location']}")
            print(f"   Posted: {job['date_posted']}")
    else:
        print("❌ No jobs found matching custom criteria")
    
    return matching_jobs

def main():
    """Run all filtering examples."""
    print("🚀 KulanJobs Advanced Filtering Examples")
    print("=" * 60)
    
    try:
        # Run all examples
        wash_jobs = example_wash_consultancy()
        health_jobs = example_health_evaluation()
        livelihoods_jobs = example_livelihoods_displacement()
        recent_jobs = example_recent_consultancies()
        custom_jobs = example_custom_boolean_search()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 FILTERING SUMMARY")
        print("=" * 60)
        print(f"WASH Consultancy Jobs: {len(wash_jobs) if wash_jobs else 0}")
        print(f"Health Evaluation Jobs: {len(health_jobs) if health_jobs else 0}")
        print(f"Livelihoods/Displacement Jobs: {len(livelihoods_jobs) if livelihoods_jobs else 0}")
        print(f"Recent Consultancy Jobs: {len(recent_jobs) if recent_jobs else 0}")
        print(f"Custom Boolean Search: {len(custom_jobs) if custom_jobs else 0}")
        
        total_unique = len(set(
            job['url'] for job_list in [wash_jobs, health_jobs, livelihoods_jobs, recent_jobs, custom_jobs] 
            if job_list for job in job_list
        ))
        print(f"\nTotal Unique Jobs Found: {total_unique}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user.")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    main()

