# FoodFinder

A location-based restaurant recommendation app that finds the best dining options near you using intelligent scoring algorithms.

## Features

- **Smart Recommendations**: Get categorized suggestions for best overall, best value, and hidden gems
- **Location-Based**: Uses your current location to find nearby restaurants
- **Customizable Radius**: Adjust search distance from 500m to 50km
- **Real-Time Data**: Powered by Google Places API for up-to-date restaurant information

## Quick Start

1. **Clone and Install**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up API Key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google Places API key
   ```

3. **Run**
   ```bash
   uvicorn main:app --reload
   ```

4. **Open** http://localhost:8000

## API Key Setup

Get a Google Places API key from [Google Cloud Console](https://console.cloud.google.com/) and add it to your `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: Bootstrap, Vanilla JS
- **API**: Google Places API