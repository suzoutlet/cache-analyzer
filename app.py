from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
from socket import gethostbyname
import requests
import json
from ipinfo import getHandler  # Corrected import
import os
import logging

app = Flask(__name__)

# Enable debugging logs in Flask
logging.basicConfig(level=logging.DEBUG)

# Function to detect WP Rocket caching
def detect_wp_rocket(url):
    try:

        # Start
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"❌ Failed to load page, status: {response.status_code}")
            return "Failed to fetch page"

        body = response.text
        headers = response.headers

        # Debugging: Log response status, headers, and first 500 characters of body
        print(f"🔹 Response Status Code: {response.status_code}")
        print(f"🔹 Response Headers: {headers}")
        print(f"🔹 First 500 Characters of Response Body:\n{body[:500]}")

        # End
        response = requests.get(url, timeout=10)
 
        # Default values to prevent errors
        cache_timestamp = None
        cache_timestamp_link = None

        if "Performance optimized by WP Rocket" in response.text:
            if "Debug: cached@" in response.text:
                # Extract the cache timestamp correctly
                import re
                match = re.search(r"Debug: cached@(\d+)", response.text)
                if match:
                    cache_timestamp = match.group(1)

                    # Generate the correct link for Epoch Converter
                    cache_timestamp_link = f"https://suzoutlet.github.io/timestamp-converter/?timestamp={cache_timestamp}"
                    return "WP Rocket cache detected with active caching.", cache_timestamp, cache_timestamp_link

                return "WP Rocket detected, but timestamp not found.", cache_timestamp, cache_timestamp_link
            else:
                return "WP Rocket detected and Optimized, but no cache timestamp found. Optimized but not cached.", cache_timestamp, cache_timestamp_link
            
        # Debugging: Log WP Rocket detection status
        print(f"🔹 WP Rocket Detection: {cache_status}")

        return cache_status
    except Exception as e:
        print(f"Error fetching the page: {e}")
    return "No WP Rocket cache detected.", cache_timestamp, cache_timestamp_link

# Load the updated cache details and headers from the JSON file
def load_cache_info():
    json_path = os.path.join(os.path.dirname(__file__), 'cache_headers.json')
    with open(json_path, 'r') as file:
        return json.load(file)


# Function to get the hosting provider info
def get_hosting_provider(ip):
    try:
        handler = getHandler("37d7957a4040da")  # Replace with your actual ipinfo.io API token
        details = handler.getDetails(ip)
        return details.org
    except Exception as e:
        return str(e)

def analyze_headers(url):
    try:
        # Send a HEAD request to get response headers
        response = requests.head(url, allow_redirects=True)
        headers = response.headers

        # Load cache information from the JSON file
        cache_info = load_cache_info()

        # Store formatted response headers
        print(f"Fetched Headers for {url}: {headers}")

        # Properly format headers for display
        formatted_headers = [{"header": key, "value": value, "explanation": cache_info['cache_details'].get(key, {}).get('explanation', "No explanation available.")} for key, value in headers.items()]

        # Page Caching Analysis
        wp_rocket_detection = detect_wp_rocket(url)
        if isinstance(wp_rocket_detection, tuple):
            wp_rocket_status, cache_timestamp, cache_timestamp_link = wp_rocket_detection
        else:
            wp_rocket_status = wp_rocket_detection
            cache_timestamp = None
            cache_timestamp_link = None


        # Detect additional cache layers
        additional_cache_layers = []
        for header in cache_info['cache_headers']:
            header_name = header['name']
            if header_name in headers:
                header_value = headers[header_name]
                cache_values = cache_info['cache_details'].get(header_name, {}).get('values', {})
                value_explanation = cache_values.get(header_value, f"Unknown value: {header_value}")
                additional_cache_layers.append(f"{header_name}: {header_value} ({value_explanation})")

        # Identify hosting provider
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        ip = gethostbyname(domain)
        hosting_provider = get_hosting_provider(ip)

        # Return structured data to display in HTML
        return {
            "headers": formatted_headers,
            "wp_rocket": wp_rocket_status,
            "cache_timestamp": cache_timestamp,
            "cache_timestamp_link": cache_timestamp_link,
            "additional_cache_layers": additional_cache_layers,
            "hosting_provider": hosting_provider,
            "ip_address": ip,
            "url": url
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching the URL: {e}"}

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        url = request.form["url"]
        result = analyze_headers(url)  # Previously was only printing, now it's returning a dictionary
    return render_template("index.html", result=result)

# Handles GET requests to /analyze
@app.route("/analyze", methods=["GET"])
def analyze():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    print(f"🔹 Received request for URL: {url}")  # Debugging

    # Perform cache analysis before returning response
    cache_status = detect_wp_rocket(url)

    result = {
        "message": "Cache analysis successful",
        "url": url,
        "cache_status": cache_status
    }

    print(f"🔹 API Response: {result}")  # Debugging
    return jsonify(result)

#  This allows you to host the app and make it accessible locally

# if __name__ == "__main__":
#     app.run(debug=True)

#  This allows Render to host the app and make it accessible publicly
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Detects port assigned by Render
    app.run(host="0.0.0.0", port=port)

