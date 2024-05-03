Created with ChatGPT

# Pinnacle Sports Odds Tracker

Simple odds movement tracker.

## Description

The Pinnacle Sports Odds Tracker leverages the RapidAPI to obtain up-to-date odds for various sports events across multiple disciplines.
This tool is particularly useful for users who need to track odds for large volumes of matches or across different sports, providing a robust interface for data collection, storage, and alert mechanisms.

### Key Features:
- **Automated Data Fetching**: Scheduled tasks retrieve the latest odds and event data automatically, ensuring that the data remains current without manual intervention.
- **Database Integration**: All fetched data is stored in a structured MySQL database, allowing for complex queries and long-term data analysis.
- **Real-time Alerts**: Utilizes auditory signals to alert users to significant changes in odds, enabling quick reactions to market movements.
- **Extensible Framework**: Designed with modularity in mind, allowing for easy integration of additional sports, data points, or alternative data sources.

The tool is built using Python and integrates several technologies, including requests for API interaction, MySQL for database management, and the Windows-specific `winsound` library for audio alerts. The architecture is designed to be robust yet flexible, accommodating potential expansions or modifications tailored to specific user needs.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- Windows operating system (due to dependency on `winsound`)
- Access to RapidAPI and a valid API key

### Useful links

- https://www.rebelbetting.com/blog/difference-soft-sharp-bookmakers
- https://rapidapi.com/tipsters/api/pinnacle-odds
- https://www.techopedia.com/gambling-guides/value-betting
