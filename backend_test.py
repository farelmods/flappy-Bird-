#!/usr/bin/env python3
"""
Backend Test for Flappy Adventure
Since this is a client-side HTML game, we test the web server serving the game.
"""

import requests
import sys

class FlappyAdventureTester:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

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

    def test_server_availability(self):
        """Test if the game server is running and accessible"""
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False

    def test_html_content(self):
        """Test if the HTML content contains expected game elements"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code != 200:
                return False
            
            content = response.text
            
            # Check for essential game elements
            required_elements = [
                "Flappy Adventure",  # New Game title
                "id=\"gameCanvas\"", # Canvas
                "id=\"login-screen\"", # Login screen
                "Game.login()",      # Login function
                "Game.start()",      # Start function
                "CHARACTERS",        # Character data
                "SKILLS",            # Skill data
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"Missing elements: {missing_elements}")
                return False
            
            return True
        except:
            return False

    def test_feature_definitions(self):
        """Test if new features are defined in the code"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code != 200:
                return False
            
            content = response.text
            
            # Check feature definitions
            checks = [
                "User.addCoins" in content,         # Coin system
                "User.buyCharacter" in content,     # Shop system
                "User.upgradeSkill" in content,     # Skill system
                "class Coin" in content,            # Coin class
                "magnet: { baseCost:" in content,   # Magnet skill
            ]
            
            return all(checks)
        except:
            return False

    def test_localstorage_usage(self):
        """Test if localStorage is used with the new username-based key"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code != 200:
                return False
            
            content = response.text
            
            # Check localStorage usage
            checks = [
                "localStorage.getItem(`fb_game_${username}`)" in content or "localStorage.getItem('fb_game_' + username)" in content or "fb_game_" in content,
                "localStorage.setItem(`fb_game_${this.username}`)" in content or "fb_game_" in content,
            ]
            
            return all(checks)
        except:
            return False

def main():
    print("🎮 Starting Flappy Adventure Backend Tests")
    print("=" * 60)
    
    # Setup
    tester = FlappyAdventureTester()
    
    # Run tests
    tester.run_test("Server Availability", tester.test_server_availability)
    tester.run_test("HTML Content Validation", tester.test_html_content)
    tester.run_test("Feature Definitions", tester.test_feature_definitions)
    tester.run_test("LocalStorage Usage", tester.test_localstorage_usage)
    
    # Print results
    print(f"\n📊 Backend Tests Summary:")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All backend tests passed! Game server is working correctly.")
        return 0
    else:
        print("⚠️  Some backend tests failed. Check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())