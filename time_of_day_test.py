#!/usr/bin/env python3
"""
Time-of-Day Feature Test for Flappy Bird & Dragon Game
This test analyzes the time-of-day cycling feature implementation.
"""

import requests
import re
import sys
from datetime import datetime

class TimeOfDayFeatureTester:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.html_content = ""

    def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            success = test_func()
            if success:
                self.tests_passed += 1
                print(f"✅ Passed")
            else:
                print(f"❌ Failed")
            return success
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def fetch_game_content(self):
        """Fetch the game HTML content"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                self.html_content = response.text
                return True
            return False
        except:
            return False

    def test_time_of_day_config(self):
        """Test if time-of-day configuration is properly defined"""
        if not self.html_content:
            return False
        
        # Check for timeOfDayConfig object
        if "timeOfDayConfig" not in self.html_content:
            print("❌ timeOfDayConfig object not found")
            return False
        
        # Check for all four time periods
        time_periods = ['day', 'afternoon', 'night', 'morning']
        for period in time_periods:
            if f"{period}:" not in self.html_content:
                print(f"❌ Time period '{period}' not found in config")
                return False
        
        # Check for time period names
        expected_names = ['🌞 Siang', '🌅 Sore', '🌙 Malam', '🌅 Pagi']
        for name in expected_names:
            if name not in self.html_content:
                print(f"❌ Time period name '{name}' not found")
                return False
        
        print("✅ All time periods and names found")
        return True

    def test_sky_gradients(self):
        """Test if sky gradients are defined for each time period"""
        if not self.html_content:
            return False
        
        # Check for gradient colors
        gradient_checks = [
            ('#87CEEB', '#98D8E8'),  # Day - blue
            ('#FF6B35', '#F7931E'),  # Afternoon - orange/sunset
            ('#191970', '#000080'),  # Night - dark blue
            ('#FFB6C1', '#FFA07A'),  # Morning - pink/dawn
        ]
        
        for start_color, end_color in gradient_checks:
            if start_color not in self.html_content or end_color not in self.html_content:
                print(f"❌ Gradient colors {start_color} -> {end_color} not found")
                return False
        
        print("✅ All sky gradient colors found")
        return True

    def test_cloud_colors(self):
        """Test if cloud colors are defined for different times"""
        if not self.html_content:
            return False
        
        # Check for cloud color configurations
        cloud_color_patterns = [
            'rgba(255, 255, 255, 0.8)',  # Day clouds
            'rgba(255, 182, 193, 0.9)',  # Afternoon clouds
            'rgba(220, 220, 220, 0.6)',  # Night clouds
            'rgba(255, 255, 255, 0.7)',  # Morning clouds
        ]
        
        for color in cloud_color_patterns:
            if color not in self.html_content:
                print(f"❌ Cloud color '{color}' not found")
                return False
        
        print("✅ All cloud colors found")
        return True

    def test_update_time_function(self):
        """Test if updateTimeOfDay function is properly implemented"""
        if not self.html_content:
            return False
        
        # Check for updateTimeOfDay function
        if "function updateTimeOfDay()" not in self.html_content:
            print("❌ updateTimeOfDay function not found")
            return False
        
        # Check for score-based time calculation
        if "Math.floor(score / 10)" not in self.html_content:
            print("❌ Score-based time calculation not found")
            return False
        
        # Check for modulo operation for cycling
        if "% 4" not in self.html_content:
            print("❌ Cycling logic (% 4) not found")
            return False
        
        # Check for time array
        if "['day', 'afternoon', 'night', 'morning']" not in self.html_content:
            print("❌ Time periods array not found")
            return False
        
        print("✅ updateTimeOfDay function properly implemented")
        return True

    def test_score_integration(self):
        """Test if time update is integrated with score system"""
        if not self.html_content:
            return False
        
        # Check if updateTimeOfDay is called when score changes
        score_update_pattern = r'score\+\+.*updateTimeOfDay\(\)'
        if not re.search(score_update_pattern, self.html_content, re.DOTALL):
            print("❌ updateTimeOfDay not called when score increases")
            return False
        
        print("✅ Time update integrated with score system")
        return True

    def test_stars_for_night(self):
        """Test if stars are implemented for night time"""
        if not self.html_content:
            return False
        
        # Check for drawStars function
        if "function drawStars()" not in self.html_content:
            print("❌ drawStars function not found")
            return False
        
        # Check if stars are drawn during night time
        if "currentTimeOfDay === 'night'" not in self.html_content:
            print("❌ Night time check for stars not found")
            return False
        
        # Check for star positions
        if "starPositions" not in self.html_content:
            print("❌ Star positions not defined")
            return False
        
        print("✅ Stars implementation found for night time")
        return True

    def test_time_display_element(self):
        """Test if time display element is properly configured"""
        if not self.html_content:
            return False
        
        # Check for timeOfDay element
        if 'id="timeOfDay"' not in self.html_content:
            print("❌ timeOfDay element not found")
            return False
        
        # Check for timeOfDayElement variable
        if "timeOfDayElement" not in self.html_content:
            print("❌ timeOfDayElement variable not found")
            return False
        
        # Check for text content update
        if "timeOfDayElement.textContent" not in self.html_content:
            print("❌ Time display update not found")
            return False
        
        print("✅ Time display element properly configured")
        return True

    def test_background_drawing(self):
        """Test if background drawing uses time-of-day configuration"""
        if not self.html_content:
            return False
        
        # Check for drawBackground function
        if "function drawBackground()" not in self.html_content:
            print("❌ drawBackground function not found")
            return False
        
        # Check if it uses timeOfDayConfig
        if "timeOfDayConfig[currentTimeOfDay]" not in self.html_content:
            print("❌ Background doesn't use time-of-day config")
            return False
        
        # Check for gradient creation
        if "createLinearGradient" not in self.html_content:
            print("❌ Gradient creation not found")
            return False
        
        print("✅ Background drawing uses time-of-day configuration")
        return True

def main():
    print("🌅 Starting Time-of-Day Feature Tests for Flappy Bird Game")
    print("=" * 70)
    
    # Setup
    tester = TimeOfDayFeatureTester()
    
    # Fetch game content first
    if not tester.fetch_game_content():
        print("❌ Failed to fetch game content from server")
        return 1
    
    print("✅ Successfully fetched game content")
    
    # Run time-of-day specific tests
    tester.run_test("Time-of-Day Configuration", tester.test_time_of_day_config)
    tester.run_test("Sky Gradients", tester.test_sky_gradients)
    tester.run_test("Cloud Colors", tester.test_cloud_colors)
    tester.run_test("Update Time Function", tester.test_update_time_function)
    tester.run_test("Score Integration", tester.test_score_integration)
    tester.run_test("Stars for Night", tester.test_stars_for_night)
    tester.run_test("Time Display Element", tester.test_time_display_element)
    tester.run_test("Background Drawing", tester.test_background_drawing)
    
    # Print results
    print(f"\n📊 Time-of-Day Feature Tests Summary:")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All time-of-day feature tests passed!")
        print("\n📋 Expected Behavior Summary:")
        print("• Score 0-9: 🌞 Siang (Day) - Blue background")
        print("• Score 10-19: 🌅 Sore (Afternoon) - Orange/sunset background")
        print("• Score 20-29: 🌙 Malam (Night) - Dark blue background + stars")
        print("• Score 30-39: 🌅 Pagi (Morning) - Pink/dawn background")
        print("• Score 40+: Cycles back to 🌞 Siang (Day)")
        return 0
    else:
        print("⚠️  Some time-of-day feature tests failed. Check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())