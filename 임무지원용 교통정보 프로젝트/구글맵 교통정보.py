import requests
import json
import ctypes

def get_traffic_info(api_key, origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': origin,
        'destination': destination,
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
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

def get_traffic_summary(data):
    if data['status'] == 'OK':
        route = data['routes'][0]
        leg = route['legs'][0]

        total_distance = leg['distance']['text']
        estimated_duration = leg['duration']['text']
        traffic_duration = leg['duration_in_traffic']['text']

        # 정체 구간 찾기
        traffic_jams = []
        for step in leg['steps']:
            if 'traffic_speed_entry' in step and step['traffic_speed_entry']:
                traffic_jams.append({
                    "distance": step['distance']['text'],
                    "duration": step['duration']['text'],
                    "instructions": step['html_instructions']
                })

        summary = f"출발지: {leg['start_address']}\n"
        summary += f"도착지: {leg['end_address']}\n"
        summary += f"총 거리: {total_distance}\n"
        summary += f"예상 소요 시간: {estimated_duration}\n"
        summary += f"교통 상황을 반영한 소요 시간: {traffic_duration}\n"

        if traffic_jams:
            summary += "\n정체 구간:\n"
            for jam in traffic_jams:
                summary += f"- 거리: {jam['distance']}, 예상 소요 시간: {jam['duration']}, 지침: {jam['instructions']}\n"
        else:
            summary += "\n정체 구간이 없습니다.\n"

        return summary
    else:
        return "경로를 찾을 수 없습니다."

# 여기에 API 키를 넣으세요
api_key = 'AIzaSyBx8OOLj0aJR_HsYu8c8SoqAWMISjB20BU'

# 출발지와 도착지를 지정합니다
origin = 'المدخل الشمالي لشركة هانوا, 5JF9+2M، الشموس، Diyala Governorate'
destination = '33.30106261959987, 44.37754697785645'

# 실시간 교통 정보를 가져옵니다
traffic_info = get_traffic_info(api_key, origin, destination)
if traffic_info:
    traffic_summary = get_traffic_summary(traffic_info)
    show_message("교통 정보", traffic_summary)
else:
    show_message("오류", "실시간 교통 정보를 가져오지 못했습니다.")