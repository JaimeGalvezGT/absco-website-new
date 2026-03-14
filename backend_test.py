import requests
import sys
import json
from datetime import datetime

class ABSCOAPITester:
    def __init__(self, base_url="https://absco-cleaning-la.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_base}/{endpoint}" if endpoint else f"{self.api_base}/"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_json = response.json()
                    print(f"   Response: {json.dumps(response_json, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")

            return success, response.json() if response.status_code == 200 else {}

        except requests.RequestException as e:
            print(f"❌ Failed - Network Error: {str(e)}")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_root(self):
        """Test API root endpoint"""
        return self.run_test(
            "API Root",
            "GET",
            "",
            200
        )

    def test_contact_submission_valid(self):
        """Test contact form submission with valid data"""
        test_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "(213) 000-0000",
            "service_type": "floor-cleaning",
            "message": "This is a test message for ABSCO cleaning services."
        }
        
        success, response = self.run_test(
            "Contact Form (Valid Data)",
            "POST",
            "contact",
            200,
            data=test_data
        )
        
        # Validate response structure
        if success and response:
            required_fields = ["id", "status", "message"]
            has_all_fields = all(field in response for field in required_fields)
            if has_all_fields and response.get("status") == "success":
                print(f"   ✅ Response structure valid")
                return True
            else:
                print(f"   ❌ Invalid response structure or status")
                return False
        return success

    def test_contact_submission_invalid_email(self):
        """Test contact form with invalid email"""
        test_data = {
            "name": "Test User",
            "email": "invalid-email",
            "phone": "(213) 000-0000",
            "service_type": "floor-cleaning",
            "message": "This is a test message."
        }
        
        return self.run_test(
            "Contact Form (Invalid Email)",
            "POST",
            "contact",
            422,  # Validation error expected
            data=test_data
        )

    def test_contact_submission_missing_required(self):
        """Test contact form with missing required fields"""
        test_data = {
            "email": "test@example.com"
            # Missing name and message (required fields)
        }
        
        return self.run_test(
            "Contact Form (Missing Required)",
            "POST",
            "contact",
            422,  # Validation error expected
            data=test_data
        )

    def test_contact_submission_minimal(self):
        """Test contact form with minimal required data"""
        test_data = {
            "name": "Minimal Test",
            "email": "minimal@test.com",
            "message": "Minimal test message"
        }
        
        return self.run_test(
            "Contact Form (Minimal Valid Data)",
            "POST",
            "contact",
            200,
            data=test_data
        )

def main():
    """Run all backend API tests"""
    print("🚀 Starting ABSCO Backend API Tests...")
    print("=" * 50)
    
    tester = ABSCOAPITester()
    
    # Run all tests
    tests = [
        tester.test_api_root,
        tester.test_contact_submission_valid,
        tester.test_contact_submission_minimal,
        tester.test_contact_submission_invalid_email,
        tester.test_contact_submission_missing_required,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            tester.tests_run += 1

    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    success_rate = (tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0
    print(f"🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 Backend tests mostly successful!")
        return 0
    elif success_rate >= 50:
        print("⚠️  Backend has some issues but core functionality works")
        return 1
    else:
        print("❌ Backend has significant issues")
        return 2

if __name__ == "__main__":
    sys.exit(main())