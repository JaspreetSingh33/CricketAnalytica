# CricketAnalytica

CricketAnalytica is a cricket analysis and player comparison platform that uses API-based data retrieval and LLM-based analysis to compare player performances.

The current version retrieves player statistics through the ESPN API and presents them in a simple and interactive interface. It focuses on comparing the batting performances of two players, allowing users to view their statistics side by side and receive a written comparison generated using the Google Gemini API.

The project is being developed as a broader cricket analysis platform, with the current implementation serving as the first version.

## Features

- Compare two cricket players
- Search for player information and statistics
- Compare batting performances
- View overall player statistics
- View home performance
- View overseas performance
- Compare runs, batting average, strike rate, hundreds, fifties, and highest score
- Highlight better statistical values between players
- Generate a written statistical comparison
- Responsive and interactive web interface
- Loading animation while player data and analysis are being retrieved

## System Architecture

The system is divided into a frontend, backend, data retrieval layer, and analysis component.

```text
                         CricketAnalytica
                                |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
     Frontend             Flask Backend          External Services
        |                       |                       |
        |                       |              +--------+--------+
        |                       |              |                 |
        v                       v              v                 v
  HTML/CSS/JS              app.py          ESPN API         Gemini API
                                |
                 +--------------+--------------+
                 |                             |
                 v                             v
          cricket_data.py              gemini_analysis.py
                 |                             |
                 v                             v
          Player Statistics             Statistical Analysis
                 |                             |
                 +--------------+--------------+
                                |
                                v
                         Comparison Result
                                |
                                v
                             Frontend

 ```
## Main Components

### Frontend

The frontend is implemented using HTML, CSS, JavaScript, and Jinja2 templates. It handles the user interface, player input, comparison tables, tabs, loading animation, and presentation of the analysis.

### Flask Backend

`app.py` acts as the main application controller. It receives the player's names from the frontend, requests player data, sends the retrieved information for analysis, and returns the results to the webpage.

### Player Data Layer

`cricket_data.py` handles player searching and retrieval of player statistics through the ESPN data source. It prepares the information required by the application for comparison.

### Analysis Layer

`gemini_analysis.py` prepares the relevant player statistics and sends them to the Gemini API. The returned response is used to generate the written statistical comparison.

### External Services

The application currently uses an ESPN data source for player information and statistics and the Google Gemini API for the written statistical analysis.

## Application Workflow

The current application follows this workflow:

```text
User enters two player names
            |
            v
    Flask receives request
            |
            v
       Player search
            |
            v
    ESPN API retrieves data
            |
            v
      Player statistics
            |
            v
    Statistics displayed
            |
            v
      Players compared
            |
            v
Relevant statistics sent to Gemini
            |
            v
  Statistical analysis generated
            |
            v
   Analysis displayed to user

```
## How the Comparison Works

When the user enters two player names, the application first searches for the players and retrieves their available information and statistics.

The retrieved statistics are organized into categories such as:

- Overall performance
- Home performance
- Overseas performance

The application then displays the relevant statistics side by side.

For comparable statistics, JavaScript checks the values of both players and highlights the higher value.

The application also sends the relevant player statistics to the Gemini API. Gemini generates a written comparison based on the statistics provided by the application.

The analysis is instructed to use the available statistics rather than inventing additional information or making unsupported claims.

## Technology Stack

### Backend

- Python
- Flask

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2

### Data

- ESPN API / ESPN cricket data

### Analysis

- Google Gemini API

### Development Tools

- Git
- GitHub
- Python virtual environment

## API Usage

The application uses two external services as part of its current implementation.

### ESPN Data

The application retrieves player information and statistics from the ESPN cricket data source.

### Google Gemini

The retrieved statistics are passed to the Gemini API to generate a written comparison between the selected players.

The Gemini analysis is based on the statistics supplied by the application.

## Current Scope

The current version of CricketAnalytica is the first implementation of the project.

At this stage, the main focus is player comparison and batting analysis. The platform is designed so that additional cricket analysis features can be added as development continues.

## Limitations

- Player data depends on the availability of the external ESPN data source.
- API requests may take some time depending on network conditions and external server response times.
- Player searches depend on the names recognized by the underlying data source.
- Gemini analysis depends on the availability and usage limits of the Gemini API.
- The current version does not yet provide complete cricket analysis across all aspects of the game.

## Future Improvements

The project will gradually be expanded into a more complete cricket analysis platform.

Planned improvements include:

- Support for additional cricket formats
- Bowling analysis
- Fielding analysis
- More complete player performance analysis
- Improved statistical models
- Better machine learning models
- More detailed player comparisons
- Performance trends and historical analysis
- Interactive graphs and visualizations
- Improved player search and selection
- More advanced comparison features
- A more refined and feature-rich user interface

  ## Project Structure

```text
CricketAnalytica/
│
├── app.py
├── cricket_data.py
├── gemini_analysis.py
├── compare_test.py
├── espn_test.py
├── gemini_test.py
├── test_api.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── .gitignore
├── README.md
└── LICENSE
```

### Main Files

**`app.py`**

Main Flask application. Handles requests from the user, retrieves player data, calls the analysis function, and renders the results.

**`cricket_data.py`**

Handles player searching and retrieval of player information and statistics from the ESPN data source.

**`gemini_analysis.py`**

Prepares the player statistics and sends them to the Gemini API to generate the written comparison.

**`templates/index.html`**

Contains the main user interface, including player input fields, player cards, statistics tables, comparison tabs, loading animation, and JavaScript functionality.

**`requirements.txt`**

Contains the Python dependencies required to run the project.

**`.gitignore`**

Prevents files such as the virtual environment, Python cache files, and environment variables from being uploaded to GitHub.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/JaspreetSingh33/CricketAnalytica.git
cd CricketAnalytica
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

The application requires a Gemini API key.

Create a `.env` file in the project directory:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not upload the `.env` file to GitHub.

The `.gitignore` file already excludes `.env` from version control.

## Running the Application

Start the Flask application:

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000
```

Open the address in a web browser to use CricketAnalytica.

## License

This project is licensed under the MIT License.

