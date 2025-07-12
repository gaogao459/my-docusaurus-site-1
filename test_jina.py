#!/usr/bin/env python3
"""
Simple test script for Jina.ai API
"""

import requests
import sys

def test_jina_api():
    """Test Jina.ai Reader API"""
    
    url = "https://help.make.com/learn-the-basics"
    jina_url = f"https://r.jina.ai/{url}"
    
    print(f"Testing Jina.ai API...")
    print(f"Target URL: {url}")
    print(f"Jina URL: {jina_url}")
    
    try:
        print("Making request...")
        response = requests.get(jina_url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"Success! Content length: {len(content)} characters")
            print(f"First 200 characters:")
            print("-" * 50)
            print(content[:200])
            print("-" * 50)
            return content
        else:
            print(f"Error: HTTP {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return None
            
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Connection failed")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    test_jina_api() 