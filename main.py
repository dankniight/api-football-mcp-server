import os
from fastmcp import FastMCP
from dotenv import load_dotenv
import requests

load_dotenv()

mcp = FastMCP("API-Football MCP")

API_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = os.getenv("API_FOOTBALL_HOST", "https://v3.football.api-sports.io")

def make_api_request(endpoint: str, params: dict = None) -> dict:
    if not API_KEY:
        return {"error": "API key not configured"}
    
    url = f"{API_HOST}/{endpoint}"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params or {})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_leagues(country: str = None, season: int = None) -> dict:
    params = {}
    if season:
        params["season"] = season
    if country:
        params["country"] = country
    
    return make_api_request("leagues", params)

@mcp.tool()
def get_teams(league_id: int, season: int = None) -> dict:
    params = {
        "league": league_id
    }
    if season:
        params["season"] = season
    return make_api_request("teams", params)

@mcp.tool()
def get_team_stats(team_id: int, league_id: int, season: int = None) -> dict:
    params = {
        "team": team_id,
        "league": league_id
    }
    if season:
        params["season"] = season
    return make_api_request("teams/statistics", params)

@mcp.tool()
def get_team_id_by_name(team_name: str, league_id: int = None, season: int = None) -> dict:
    """Get team ID by team name, optionally filtered by league and season"""
    params = {}
    if league_id:
        params["league"] = league_id
    if season:
        params["season"] = season
    
    teams_response = make_api_request("teams", params)
    if "error" in teams_response:
        return teams_response
    
    if "response" in teams_response:
        for team in teams_response["response"]:
            if team.get("name", "").lower() == team_name.lower():
                return {"team_id": team["id"], "team": team}
        return {"error": f"Team '{team_name}' not found"}
    
    return {"error": "Invalid response from teams API"}

@mcp.tool()
def get_players(team_id: int, season: int) -> dict:
    params = {
        "team": team_id
    }
    if season:
        params["season"] = season
    return make_api_request("players", params)

@mcp.tool()
def get_player_stats(player_id: int, season: int) -> dict:
    params = {
        "id": player_id
    }
    if season:
        params["season"] = season
    return make_api_request("players", params)

@mcp.tool()
def get_fixtures(league_id: int = None, team_id: int = None, season: int = None, 
                date: str = None, next: int = None, last: int = None) -> dict:
    params = {}
    
    if season:
        params["season"] = season
    if league_id:
        params["league"] = league_id
    if team_id:
        params["team"] = team_id
    if date:
        params["date"] = date
    if next:
        params["next"] = next
    if last:
        params["last"] = last
    
    return make_api_request("fixtures", params)

@mcp.tool()
def get_fixture_stats(fixture_id: int) -> dict:
    params = {"id": fixture_id}
    return make_api_request("fixtures/statistics", params)

@mcp.tool()
def get_standings(league_id: int, season: int) -> dict:
    params = {
        "league": league_id
    }
    if season:
        params["season"] = season
    return make_api_request("standings", params)

@mcp.tool()
def get_top_scorers(league_id: int, season: int) -> dict:
    params = {
        "league": league_id
    }
    if season:
        params["season"] = season
    return make_api_request("players/topscorers", params)

@mcp.tool()
def get_top_assists(league_id: int, season: int) -> dict:
    params = {
        "league": league_id
    }
    if season:
        params["season"] = season
    return make_api_request("players/topassists", params)

@mcp.tool()
def get_venue(venue_id: int) -> dict:
    params = {"id": venue_id}
    return make_api_request("venues", params)

@mcp.tool()
def get_team_transfers(team_id: int) -> dict:
    params = {"team": team_id}
    return make_api_request("transfers", params)

@mcp.tool()
def get_injuries(team_id: int, player_id: int, season: int) -> dict:
    params = {}
    if season:
        params["season"] = season
    if team_id:
        params["team"] = team_id
    if player_id:
        params["player"] = player_id
    
    return make_api_request("injuries", params)

@mcp.tool()
def get_predictions(fixture_id: int) -> dict:
    params = {"fixture": fixture_id}
    return make_api_request("predictions", params)

@mcp.tool()
def get_head_to_head(team1_id: int, team2_id: int) -> dict:
    params = {
        "h2h": f"{team1_id}-{team2_id}"
    }
    return make_api_request("fixtures/headtohead", params)

@mcp.tool()
def get_countries() -> dict:
    return make_api_request("countries")

@mcp.tool()
def get_league_info(league_id: int) -> dict:
    params = {"id": league_id}
    return make_api_request("leagues", params)

if __name__ == "__main__":
    mcp.run()