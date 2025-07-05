import datetime
import requests
import os
import json
from typing import Dict, Any, List
from urllib.parse import quote_plus


def get_time() -> str:
    """Get the current time and date."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_weather(city: str = "London") -> Dict[str, Any]:
    """
    Get weather information for a city.
    
    Args:
        city (str): City name to get weather for
        
    Returns:
        Dict containing weather information
    """
    try:
        # Using a free weather API (OpenWeatherMap would require API key)
        # For now, return a mock response
        weather_data = {
            "city": city,
            "temperature": "22°C",
            "condition": "Partly Cloudy",
            "humidity": "65%",
            "wind_speed": "12 km/h",
            "timestamp": get_time()
        }
        return weather_data
    except Exception as e:
        return {
            "error": f"Unable to fetch weather data: {str(e)}",
            "city": city,
            "timestamp": get_time()
        }


def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Perform a web search using DuckDuckGo Instant Answer API.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        Dict containing search results
    """
    try:
        # Using DuckDuckGo Instant Answer API (free, no API key required)
        url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        results = {
            "query": query,
            "abstract": data.get("Abstract", "No abstract available"),
            "abstract_source": data.get("AbstractSource", ""),
            "abstract_url": data.get("AbstractURL", ""),
            "related_topics": []
        }
        
        # Add related topics (limited to max_results)
        if "RelatedTopics" in data:
            for topic in data["RelatedTopics"][:max_results]:
                if isinstance(topic, dict) and "Text" in topic:
                    results["related_topics"].append({
                        "text": topic["Text"],
                        "url": topic.get("FirstURL", "")
                    })
        
        return results
        
    except Exception as e:
        return {
            "error": f"Unable to perform web search: {str(e)}",
            "query": query,
            "timestamp": get_time()
        }


def save_file(content: str, filename: str, file_type: str = "txt") -> Dict[str, Any]:
    """
    Save content to a file.
    
    Args:
        content (str): Content to save
        filename (str): Name of the file (without extension)
        file_type (str): Type of file (txt, json, csv, etc.)
        
    Returns:
        Dict containing save result
    """
    try:
        # Create data directory if it doesn't exist
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Generate filename with timestamp to avoid conflicts
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"{filename}_{timestamp}.{file_type}"
        file_path = os.path.join(data_dir, full_filename)
        
        # Save content based on file type
        if file_type.lower() == "json":
            # If content is a string that looks like JSON, parse it
            try:
                if isinstance(content, str):
                    json_content = json.loads(content)
                else:
                    json_content = content
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(json_content, f, indent=2, ensure_ascii=False)
            except json.JSONDecodeError:
                # If not valid JSON, save as string
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            "success": True,
            "filename": full_filename,
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "timestamp": get_time()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Unable to save file: {str(e)}",
            "filename": filename,
            "timestamp": get_time()
        }


def list_saved_files() -> Dict[str, Any]:
    """
    List all saved files in the data directory.
    
    Returns:
        Dict containing list of saved files
    """
    try:
        data_dir = "data"
        if not os.path.exists(data_dir):
            return {
                "files": [],
                "message": "No data directory found. No files have been saved yet."
            }
        
        files = []
        for filename in os.listdir(data_dir):
            file_path = os.path.join(data_dir, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                files.append({
                    "filename": filename,
                    "size": file_stat.st_size,
                    "created": datetime.datetime.fromtimestamp(file_stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                    "modified": datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # Sort by modification time (newest first)
        files.sort(key=lambda x: x["modified"], reverse=True)
        
        return {
            "files": files,
            "total_files": len(files),
            "timestamp": get_time()
        }
        
    except Exception as e:
        return {
            "error": f"Unable to list files: {str(e)}",
            "timestamp": get_time()
        }


def read_saved_file(filename: str) -> Dict[str, Any]:
    """
    Read content from a saved file.
    
    Args:
        filename (str): Name of the file to read
        
    Returns:
        Dict containing file content
    """
    try:
        data_dir = "data"
        file_path = os.path.join(data_dir, filename)
        
        if not os.path.exists(file_path):
            return {
                "error": f"File '{filename}' not found",
                "timestamp": get_time()
            }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "filename": filename,
            "content": content,
            "file_size": len(content),
            "timestamp": get_time()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Unable to read file: {str(e)}",
            "filename": filename,
            "timestamp": get_time()
        }
