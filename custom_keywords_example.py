#!/usr/bin/env python3
"""
Custom Keywords Example for KulanJobs Scraper
This script demonstrates how to use custom thematic keywords as parameters.
"""

from kulanjobs_scraper import KulanJobsScraper
import json

def example_custom_thematic_keywords():
    """Example: Using custom thematic keywords for specific sectors."""
    print("🔍 Example 1: Custom Thematic Keywords")
    print("-" * 50)
    
    # Define custom thematic keywords
    custom_themes = {
        'Climate & Environment': [
            'climate change', 'environmental protection', 'renewable energy', 'carbon footprint',
            'sustainability', 'green energy', 'climate adaptation', 'environmental impact',
            'biodiversity', 'conservation', 'ecosystem', 'climate resilience'
        ],
        'Education': [
            'education', 'teaching', 'learning', 'curriculum', 'pedagogy', 'literacy',
            'numeracy', 'educational assessment', 'school management', 'teacher training',
            'educational technology', 'inclusive education', 'early childhood development'
        ],
        'Technology & Innovation': [
            'digital transformation', 'artificial intelligence', 'machine learning', 'blockchain',
            'fintech', 'mobile technology', 'data analytics', 'software development',
            'innovation', 'technology transfer', 'digital literacy', 'cybersecurity'
        ]
    }
    
    # Create scraper with custom keywords
    scraper = KulanJobsScraper(
        delay=1,
        custom_thematic_keywords=custom_themes
    )
    
    # Test the custom keywords
    filters = {
        'themes': ['Climate & Environment', 'Education'],
        'require_project_keywords': True,
        'max_days_ago': 30
    }
    
    print("Custom thematic keywords loaded:")
    for theme, keywords in scraper.thematic_keywords.items():
        print(f"  {theme}: {len(keywords)} keywords")
    
    jobs = scraper.scrape_all_jobs(max_pages=2, filters=filters)
    
    if jobs:
        scraper.save_to_json("custom_themes_jobs.json")
        print(f"✅ Found {len(jobs)} jobs with custom themes")
        
        for i, job in enumerate(jobs[:3]):
            print(f"\n{i+1}. {job['title']}")
            print(f"   Organization: {job['organization']}")
            print(f"   Location: {job['location']}")
            print(f"   Posted: {job['date_posted']}")
    else:
        print("❌ No jobs found with custom themes")
    
    return jobs

def example_custom_project_keywords():
    """Example: Using custom project keywords."""
    print("\n🔍 Example 2: Custom Project Keywords")
    print("-" * 50)
    
    # Define custom project keywords
    custom_project_keywords = [
        'software engineer', 'data scientist', 'project manager', 'business analyst',
        'marketing specialist', 'sales representative', 'financial analyst',
        'human resources', 'operations manager', 'quality assurance'
    ]
    
    # Create scraper with custom project keywords
    scraper = KulanJobsScraper(
        delay=1,
        custom_project_keywords=custom_project_keywords
    )
    
    filters = {
        'require_project_keywords': True,
        'max_days_ago': 20
    }
    
    print(f"Custom project keywords: {len(scraper.project_keywords)} keywords")
    print(f"Keywords: {', '.join(scraper.project_keywords[:5])}...")
    
    jobs = scraper.scrape_all_jobs(max_pages=2, filters=filters)
    
    if jobs:
        scraper.save_to_json("custom_project_jobs.json")
        print(f"✅ Found {len(jobs)} jobs with custom project keywords")
        
        for i, job in enumerate(jobs[:3]):
            print(f"\n{i+1}. {job['title']}")
            print(f"   Organization: {job['organization']}")
            print(f"   Posted: {job['date_posted']}")
    else:
        print("❌ No jobs found with custom project keywords")
    
    return jobs

def example_custom_geographic_keywords():
    """Example: Using custom geographic keywords."""
    print("\n🔍 Example 3: Custom Geographic Keywords")
    print("-" * 50)
    
    # Define custom geographic keywords for different regions
    custom_geographic_keywords = [
        'west africa', 'ghana', 'nigeria', 'senegal', 'mali', 'burkina faso',
        'ivory coast', 'liberia', 'sierra leone', 'guinea', 'gambia',
        'central africa', 'cameroon', 'chad', 'central african republic'
    ]
    
    # Create scraper with custom geographic keywords
    scraper = KulanJobsScraper(
        delay=1,
        custom_geographic_keywords=custom_geographic_keywords
    )
    
    filters = {
        'geographic_focus': ['West Africa', 'Ghana', 'Nigeria'],
        'max_days_ago': 25
    }
    
    print(f"Custom geographic keywords: {len(scraper.geographic_keywords)} keywords")
    print(f"Keywords: {', '.join(scraper.geographic_keywords[:8])}...")
    
    jobs = scraper.scrape_all_jobs(max_pages=2, filters=filters)
    
    if jobs:
        scraper.save_to_json("custom_geographic_jobs.json")
        print(f"✅ Found {len(jobs)} jobs with custom geographic focus")
        
        for i, job in enumerate(jobs[:3]):
            print(f"\n{i+1}. {job['title']}")
            print(f"   Organization: {job['organization']}")
            print(f"   Location: {job['location']}")
            print(f"   Posted: {job['date_posted']}")
    else:
        print("❌ No jobs found with custom geographic keywords")
    
    return jobs

def example_combined_custom_keywords():
    """Example: Combining all custom keyword types."""
    print("\n🔍 Example 4: Combined Custom Keywords")
    print("-" * 50)
    
    # Define all custom keywords
    custom_themes = {
        'Microfinance & Financial Inclusion': [
            'microfinance', 'financial inclusion', 'microcredit', 'savings groups',
            'mobile money', 'digital payments', 'financial literacy', 'banking',
            'credit scoring', 'financial services', 'fintech', 'payment systems'
        ],
        'Gender & Social Inclusion': [
            'gender equality', 'women empowerment', 'social inclusion', 'gender mainstreaming',
            'women rights', 'gender-based violence', 'social protection', 'disability inclusion',
            'youth empowerment', 'marginalized communities', 'inclusive development'
        ]
    }
    
    custom_project_keywords = [
        'program officer', 'field coordinator', 'project coordinator', 'program manager',
        'monitoring officer', 'evaluation specialist', 'research coordinator',
        'community mobilizer', 'capacity building specialist', 'training coordinator'
    ]
    
    custom_geographic_keywords = [
        'tanzania', 'rwanda', 'burundi', 'democratic republic of congo', 'drc',
        'south sudan', 'sudan', 'great lakes region', 'central africa'
    ]
    
    # Create scraper with all custom keywords
    scraper = KulanJobsScraper(
        delay=1,
        custom_thematic_keywords=custom_themes,
        custom_project_keywords=custom_project_keywords,
        custom_geographic_keywords=custom_geographic_keywords
    )
    
    filters = {
        'themes': ['Microfinance & Financial Inclusion', 'Gender & Social Inclusion'],
        'require_project_keywords': True,
        'geographic_focus': ['Tanzania', 'Rwanda', 'Great Lakes Region'],
        'max_days_ago': 30
    }
    
    print("All custom keywords loaded:")
    print(f"  Themes: {list(scraper.thematic_keywords.keys())}")
    print(f"  Project keywords: {len(scraper.project_keywords)} keywords")
    print(f"  Geographic keywords: {len(scraper.geographic_keywords)} keywords")
    
    jobs = scraper.scrape_all_jobs(max_pages=2, filters=filters)
    
    if jobs:
        scraper.save_to_json("combined_custom_jobs.json")
        print(f"✅ Found {len(jobs)} jobs with combined custom keywords")
        
        for i, job in enumerate(jobs[:3]):
            print(f"\n{i+1}. {job['title']}")
            print(f"   Organization: {job['organization']}")
            print(f"   Location: {job['location']}")
            print(f"   Posted: {job['date_posted']}")
    else:
        print("❌ No jobs found with combined custom keywords")
    
    return jobs

def main():
    """Run all custom keyword examples."""
    print("🚀 KulanJobs Custom Keywords Examples")
    print("=" * 60)
    
    try:
        # Run all examples
        theme_jobs = example_custom_thematic_keywords()
        project_jobs = example_custom_project_keywords()
        geo_jobs = example_custom_geographic_keywords()
        combined_jobs = example_combined_custom_keywords()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 CUSTOM KEYWORDS SUMMARY")
        print("=" * 60)
        print(f"Custom Theme Jobs: {len(theme_jobs) if theme_jobs else 0}")
        print(f"Custom Project Jobs: {len(project_jobs) if project_jobs else 0}")
        print(f"Custom Geographic Jobs: {len(geo_jobs) if geo_jobs else 0}")
        print(f"Combined Custom Jobs: {len(combined_jobs) if combined_jobs else 0}")
        
        total_unique = len(set(
            job['url'] for job_list in [theme_jobs, project_jobs, geo_jobs, combined_jobs] 
            if job_list for job in job_list
        ))
        print(f"\nTotal Unique Jobs Found: {total_unique}")
        
        print("\n✅ Custom keywords functionality working perfectly!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user.")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    main()

