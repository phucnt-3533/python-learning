#!/usr/bin/env python
"""
Quick test script for RealWorld API
Run this after starting the server with: python manage.py runserver
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    print("Testing RealWorld API...")

    # 1. Register a user
    print("\n1. Registering a new user...")
    response = requests.post(f"{BASE_URL}/users/", json={
        "user": {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    })
    print_response("USER REGISTRATION", response)

    # 2. Login
    print("\n2. Logging in...")
    response = requests.post(f"{BASE_URL}/users/login/", json={
        "user": {
            "email": "test@example.com",
            "password": "password123"
        }
    })
    print_response("USER LOGIN", response)

    if response.status_code == 200:
        token = response.json()["user"]["token"]
        headers = {"Authorization": f"Token {token}"}

        # 3. Get current user
        print("\n3. Getting current user...")
        response = requests.get(f"{BASE_URL}/user/", headers=headers)
        print_response("CURRENT USER", response)

        # 4. Create an article
        print("\n4. Creating an article...")
        response = requests.post(f"{BASE_URL}/articles/",
            headers=headers,
            json={
                "article": {
                    "title": "How to Build REST APIs with Django",
                    "description": "A comprehensive guide to Django REST Framework",
                    "body": "Django REST Framework is an amazing toolkit for building Web APIs...",
                    "tagList": ["django", "python", "api"]
                }
            }
        )
        print_response("CREATE ARTICLE", response)

        if response.status_code == 201:
            article_slug = response.json()["article"]["slug"]

            # 5. Get all articles
            print("\n5. Getting all articles...")
            response = requests.get(f"{BASE_URL}/articles/")
            print_response("LIST ARTICLES", response)

            # 6. Get single article
            print(f"\n6. Getting single article (slug: {article_slug})...")
            response = requests.get(f"{BASE_URL}/articles/{article_slug}/")
            print_response("GET ARTICLE", response)

            # 7. Add a comment
            print("\n7. Adding a comment...")
            response = requests.post(f"{BASE_URL}/articles/{article_slug}/comments/",
                headers=headers,
                json={
                    "comment": {
                        "body": "Great article! Very helpful."
                    }
                }
            )
            print_response("ADD COMMENT", response)

            # 8. Get comments
            print("\n8. Getting comments...")
            response = requests.get(f"{BASE_URL}/articles/{article_slug}/comments/")
            print_response("LIST COMMENTS", response)

            # 9. Favorite article
            print("\n9. Favoriting article...")
            response = requests.post(f"{BASE_URL}/articles/{article_slug}/favorite/", headers=headers)
            print_response("FAVORITE ARTICLE", response)

            # 10. Get tags
            print("\n10. Getting all tags...")
            response = requests.get(f"{BASE_URL}/tags/")
            print_response("LIST TAGS", response)

    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60)
    print("\nVisit http://127.0.0.1:8000/api/schema/swagger-ui/ for interactive API documentation")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the server.")
        print("Make sure the Django server is running with: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
