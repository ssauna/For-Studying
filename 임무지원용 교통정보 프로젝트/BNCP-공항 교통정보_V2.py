import requests
import json
import ctypes
import sys
import os
import webbrowser
import re

def get_traffic_info(api_key, origin, destination, waypoints):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': origin,
        'destination': destination,
        'waypoints': waypoints,
        'key': api_key,
        'departure_time': 'now',
        'traffic_model': 'best_guess'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def show_message(title, message):
    # Adjust the message box parameters
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_traffic_summary(data, start_name, end_name):
    if data['status'] == 'OK':
        route = data['routes'][0]
        leg = route['legs'][0]

        total_distance = leg['distance']['text']
        estimated_duration = leg['duration']['text']
        
        # Handle missing 'duration_in_traffic' key
        traffic_duration = leg.get('duration_in_traffic', {}).get('text', 'N/A')

        # 경로상의 모든 정체 구간 찾기
        traffic_jams = []
        for step in leg['steps']:
            if 'congestion' in step and step['congestion']:
                traffic_jams.append({
                    "distance": step['distance']['text'],
                    "duration": step['duration']['text'],
                    "location": (step['start_location']['lat'], step['start_location']['lng']),
                    "instructions": clean_html(step['html_instructions'])
                })

        summary = f"출발지: {start_name}\n"
        summary += f"도착지: {end_name}\n"
        summary += f"총 거리: {total_distance}\n"
        summary += f"예상 소요 시간: {estimated_duration}\n"
        summary += f"교통 상황을 반영한 소요 시간: {traffic_duration}\n"

        if traffic_jams:
            summary += "\n정체 구간:\n"
            for jam in traffic_jams:
                summary += f"- 거리: {jam['distance']}, 예상 소요 시간: {jam['duration']}, 위치: {jam['location']}, 지침: {jam['instructions']}\n"
        else:
            summary += "\n정체 구간이 없습니다.\n"

        return summary
    else:
        return "경로를 찾을 수 없습니다."

def create_map_url(origin, destination, waypoints):
    base_url = "https://www.google.com/maps/dir/?api=1"
    url = f"{base_url}&origin={origin}&destination={destination}&waypoints={waypoints.replace(' ', '')}&travelmode=driving"
    return url

# 여기에 API 키를 넣으세요
api_key = 'AIzaSyBx8OOLj0aJR_HsYu8c8SoqAWMISjB20BU'

# 출발지와 도착지를 지정합니다
origin = '33.1724215401309, 44.61841481816676'  # BNCP (SVCC 입구)
destination = '33.27786573280721, 44.27263746542602'  # BIAP (공항 CP)
waypoints = '33.23954368730357, 44.37126316833631'  # 경유지의 위도, 경도

# 출발지와 도착지의 이름 설정
start_name = 'BNCP (SVCC 입구)'
end_name = 'BIAP (공항 CP)'

# 실시간 교통 정보를 가져옵니다
traffic_info = get_traffic_info(api_key, origin, destination, waypoints)
if traffic_info:
    traffic_summary = get_traffic_summary(traffic_info, start_name, end_name)
    map_url = create_map_url(origin, destination, waypoints)
    traffic_summary += f"\n\n경로 보기:\n{map_url}"
    show_message("교통 정보", traffic_summary)
    # 메시지 박스를 닫으면 브라우저로 URL을 엽니다.
    webbrowser.open(map_url)
else:
    show_message("오류", "실시간 교통 정보를 가져오지 못했습니다.")

# 콘솔 창 자동 닫기
sys.stdout.flush()
os._exit(0)
