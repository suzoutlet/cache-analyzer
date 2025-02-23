# Cache Analyzer - Website Caching & Hosting Checker

A simple web tool to analyze website caching layers, detect WP Rocket, Cloudflare, and other caching mechanisms, and identify hosting providers.

## Features

✔ **Detects page caching** (WP Rocket) and determines whether caching is active.

✔ **Identifies additional caching layers**, such as:
   - Cloudflare  
   - Proxy cache  
   - Varnish  
   - FastCGI cache  
   - Other server-side caching solutions  

✔ **Retrieves hosting provider information** by:
   - Resolving the website’s IP address.  
   - Querying **IPInfo API** for detailed hosting information.  

## How to use
- Go to https://cache-analyzer.onrender.com/
- Enter your URL, for example, `https://www.mysite.com/`, and click the **Analyze** Button
- You can also test with Ramdon sites by using the "**Test a Random Site**" button

##  Installation/Contribution

1. **Clone the repository**  
   ```bash
   git clone https://github.com/suzoutlet/cache-analyzer.git
   cd cache-analyzer
