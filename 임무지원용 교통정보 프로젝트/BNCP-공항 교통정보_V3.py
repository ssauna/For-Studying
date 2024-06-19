import requests
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import re

# API 키를 직접 코드에 포함
api_key = 'AIzaSyBx8OOLj0aJR_HsYu8c8SoqAWMISjB20BU'

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

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_traffic_summary(data, start_name, end_name):
    if data['status'] == 'OK':
        route = data['routes'][0]
        total_distance = 0
        estimated_duration = 0
        traffic_duration = 0

        for leg in route['legs']:
            total_distance += leg['distance']['value']
            estimated_duration += leg['duration']['value']
            traffic_duration += leg.get('duration_in_traffic', {}).get('value', leg['duration']['value'])

        total_distance /= 1000  # 총 거리 (km 단위로 변환)
        estimated_duration /= 60  # 예상 소요 시간 (분 단위로 변환)
        traffic_duration /= 60  # 교통 상황을 반영한 소요 시간 (분 단위로 변환)

        summary = f"출발지: {start_name}\n"
        summary += f"도착지: {end_name}\n"
        summary += f"총 거리: {total_distance:.1f} km\n"
        summary += f"예상 소요 시간: {estimated_duration:.0f} mins\n"
        summary += f"교통 상황을 반영한 소요 시간: {traffic_duration:.0f} mins\n"

        traffic_jams = []
        for leg in route['legs']:
            for step in leg['steps']:
                if 'congestion' in step and step['congestion']:
                    traffic_jams.append({
                        "distance": step['distance']['text'],
                        "duration": step['duration']['text'],
                        "location": (step['start_location']['lat'], step['start_location']['lng']),
                        "instructions": clean_html(step['html_instructions'])
                    })

        if traffic_jams:
            summary += "\n정체 구간:\n"
            for jam in traffic_jams:
                summary += f"- 거리: {jam['distance']}, 예상 소요 시간: {jam['duration']}, 위치: {jam['location']}, 지침: {jam['instructions']}\n"
        else:
            summary += "\n정체 구간이 없습니다.\n"

        return summary
    else:
        return "경로를 찾을 수 없습니다."

def create_static_map_url(api_key, polyline):
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        'size': '600x400',
        'maptype': 'roadmap',
        'path': f'color:0x0000ff|weight:5|enc:{polyline}',
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    print("Static Map URL:", response.url)  # 디버그: 요청 URL 확인
    if response.status_code == 200:
        return response.content
    else:
        print("Static Map Request Error:", response.text)  # 디버그: 오류 메시지 확인
        return None

def show_traffic_info(api_key, origin, destination, waypoints, start_name, end_name):
    traffic_info = get_traffic_info(api_key, origin, destination, waypoints)
    if traffic_info:
        traffic_summary = get_traffic_summary(traffic_info, start_name, end_name)
        polyline = traffic_info['routes'][0]['overview_polyline']['points']
        map_image_data = create_static_map_url(api_key, polyline)

        # Create the main window
        root = tk.Tk()
        root.title("BNCP->공항 실시간 교통정보")

        # Create a text widget to display the summary
        text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, traffic_summary)

        # Display the map image if available
        if map_image_data:
            image = Image.open(io.BytesIO(map_image_data))
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(root, image=photo)
            label.image = photo
            label.pack(padx=10, pady=10)
        else:
            text.insert(tk.END, "\n\n지도를 로드하는 데 실패했습니다.")

        # Run the application
        root.mainloop()
    else:
        messagebox.showerror("오류", "실시간 교통 정보를 가져오지 못했습니다.")

# 출발지와 도착지를 지정합니다
origin = '33.1724215401309, 44.61841481816676'  # BNCP (SVCC 입구)
destination = '33.27786573280721, 44.27263746542602'  # BIAP (공항 CP)
waypoints = '33.23954368730357, 44.37126316833631'  # 경유지의 위도, 경도

# 출발지와 도착지의 이름 설정
start_name = 'BNCP (SVCC 입구)'
end_name = 'BIAP (공항 CP)'

# 실시간 교통 정보를 가져와서 GUI로 표시합니다
show_traffic_info(api_key, origin, destination, waypoints, start_name, end_name)
