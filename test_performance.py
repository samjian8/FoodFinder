#!/usr/bin/env python3
"""
Performance test script for FoodFinder pipeline with 30km radius
"""
import requests
import time
import json

def test_pipeline_performance():
    # Test coordinates (you can change these to your preferred location)
    test_lat = 43.4723  # Waterloo, ON (example)
    test_lng = -80.5449
    test_radius = 30000  # 30km in meters
    
    print("🚀 Testing FoodFinder Pipeline Performance")
    print(f"📍 Location: {test_lat}, {test_lng}")
    print(f"📏 Radius: {test_radius/1000}km")
    print("-" * 50)
    
    url = f"http://localhost:8000/recommend?lat={test_lat}&lng={test_lng}&radius={test_radius}"
    
    try:
        # Measure total request time
        start_time = time.time()
        response = requests.get(url, timeout=30)
        total_time = time.time() - start_time
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ SUCCESS!")
            print(f"⏱️  Total request time: {total_time:.3f} seconds")
            print(f"🏪 Restaurants found: {len(results)}")
            print(f"📊 Results per second: {len(results)/total_time:.2f}")
            
            print("\n📋 Recommendations:")
            categories = ["Best Overall", "Best Value", "Hidden Gem"]
            for i, restaurant in enumerate(results):
                category = categories[i] if i < len(categories) else f"Option {i+1}"
                name = restaurant.get('name', 'Unknown')
                rating = restaurant.get('rating', 'N/A')
                print(f"  {i+1}. {category}: {name} (⭐ {rating})")
                
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"⏰ Request timed out after 30 seconds")
    except requests.exceptions.ConnectionError:
        print(f"🔌 Could not connect to server. Is it running on localhost:8000?")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

def run_multiple_tests(count=3):
    """Run multiple tests to get average performance"""
    print(f"\n🔄 Running {count} performance tests...")
    times = []
    
    for i in range(count):
        print(f"\nTest {i+1}/{count}:")
        start = time.time()
        
        try:
            response = requests.get("http://localhost:8000/recommend?lat=43.4723&lng=-80.5449&radius=30000", timeout=30)
            if response.status_code == 200:
                test_time = time.time() - start
                times.append(test_time)
                print(f"  ✅ Completed in {test_time:.3f}s")
            else:
                print(f"  ❌ Failed with status {response.status_code}")
        except Exception as e:
            print(f"  💥 Error: {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n📈 Performance Summary:")
        print(f"  Average: {avg_time:.3f}s")
        print(f"  Fastest: {min_time:.3f}s")
        print(f"  Slowest: {max_time:.3f}s")

if __name__ == "__main__":
    print("Make sure your FastAPI server is running on localhost:8000")
    print("Run: uvicorn main:app --reload")
    input("Press Enter when ready...")
    
    test_pipeline_performance()
    
    # Ask if user wants to run multiple tests
    run_more = input("\nRun multiple tests for average performance? (y/n): ")
    if run_more.lower() == 'y':
        run_multiple_tests()