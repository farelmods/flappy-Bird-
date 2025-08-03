#!/usr/bin/env python3
"""
Backend Test for Flappy Bird & Dragon Game
Since this is a client-side HTML game, we test the web server serving the game.
"""

import requests
import sys
from datetime import datetime

class FlappyBirdGameTester:
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
                "Flappy Bird & Dragon",  # Game title
                "Burung",  # Bird character
                "Naga",    # Dragon character
                "Mulai Game",  # Start game button
                "Main Lagi",   # Play again button
                "gameCanvas",  # Canvas element
                "selectCharacter",  # Character selection function
                "startGame",   # Start game function
                "gravity: 0.2",  # Bird gravity
                "gravity: 0.15", # Dragon gravity (slower)
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

    def test_character_properties(self):
        """Test if character properties are correctly defined"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code != 200:
                return False
            
            content = response.text
            
            # Check character properties
            checks = [
                "gravity: 0.2" in content,  # Bird gravity
                "gravity: 0.15" in content, # Dragon gravity (slower)
                "width: 34" in content,     # Character width
                "height: 24" in content,    # Character height
                "jumpPower: -4.5" in content, # Jump power
            ]
            
            return all(checks)
        except:
            return False

    def test_localstorage_usage(self):
        """Test if localStorage is used for saving game data"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code != 200:
                return False
            
            content = response.text
            
            # Check localStorage usage
            checks = [
                "localStorage.getItem('flappyBestScore')" in content,
                "localStorage.getItem('selectedCharacter')" in content,
                "localStorage.setItem('selectedCharacter'" in content,
                "localStorage.setItem('flappyBestScore'" in content,
            ]
            
            return all(checks)
        except:
            return False

    def test_game_controls(self):
        """Test if game controls are properly implemented"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code != 200:
                return False
            
            content = response.text
            
            # Check control implementations
            checks = [
                "addEventListener('keydown'" in content,  # Keyboard listener
                "e.code === 'Space'" in content,         # Space key handling
                "addEventListener('click'" in content,    # Mouse click listener
                "flap()" in content,                     # Flap function
            ]
            
            return all(checks)
        except:
            return False

    def test_collision_detection(self):
        """Test if collision detection is implemented"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code != 200:
                return False
            
            content = response.text
            
            # Check collision detection
            checks = [
                "checkCollisions" in content,
                "gameOver()" in content,
                "player.x + player.width > pipe.x" in content,  # Collision logic
            ]
            
            return all(checks)
        except:
            return False

def main():
    print("🎮 Starting Flappy Bird & Dragon Game Backend Tests")
    print("=" * 60)
    
    # Setup
    tester = FlappyBirdGameTester()
    
    # Run tests
    tester.run_test("Server Availability", tester.test_server_availability)
    tester.run_test("HTML Content Validation", tester.test_html_content)
    tester.run_test("Character Properties", tester.test_character_properties)
    tester.run_test("LocalStorage Usage", tester.test_localstorage_usage)
    tester.run_test("Game Controls", tester.test_game_controls)
    tester.run_test("Collision Detection", tester.test_collision_detection)
    
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