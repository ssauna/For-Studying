import graphviz

# Graphviz 객체 생성
dot = graphviz.Digraph()

# UTF-8 인코딩 설정 및 폰트 지정
dot.attr(fontname='Malgun Gothic')
dot.attr('node', fontname='Malgun Gothic')
dot.attr('graph', charset='UTF-8')

# 노드 생성 (표준 순서도 기호 사용, 색상 및 크기 조정)
dot.node('A', '시작', shape='ellipse', style='filled', color='lightblue', width='1.5')
dot.node('B', '현재 날짜와\n내일 날짜 구하기', shape='box', style='filled', color='lightgreen', width='2')
dot.node('C', '날짜 형식을\n영문식으로 변환', shape='box', style='filled', color='lightgreen', width='2')
dot.node('D', '메시지 박스 생성', shape='parallelogram', style='filled', color='lightyellow', width='2')
dot.node('E', '사용자 확인', shape='diamond', style='filled', color='lightcoral', width='2')
dot.node('F', '내일 날짜 이름으로\n파일 복사', shape='box', style='filled', color='lightgreen', width='2')
dot.node('G', '생성된 파일 열기', shape='box', style='filled', color='lightgreen', width='2')
dot.node('H', '문서의 모든 단락에서\n날짜 변경', shape='box', style='filled', color='lightgreen', width='2')
dot.node('I', '문서의 모든 테이블에서\n날짜 변경', shape='box', style='filled', color='lightgreen', width='2')
dot.node('J', '변경된 내용 저장', shape='box', style='filled', color='lightgreen', width='2')
dot.node('K', '성공 메시지 출력', shape='parallelogram', style='filled', color='lightyellow', width='2')
dot.node('L', '종료', shape='ellipse', style='filled', color='lightblue', width='1.5')
dot.node('M', '작업 취소', shape='box', style='filled', color='lightgray', width='2')
dot.node('N', '오류 발생 시', shape='diamond', style='filled', color='lightcoral', width='2')
dot.node('O', '오류 메시지 출력\n및 사용자 입력 대기', shape='parallelogram', style='filled', color='lightyellow', width='2')

# 엣지(경로) 생성
dot.edges(['AB', 'BC', 'CD', 'DE'])
dot.edge('E', 'F', label='Yes')
dot.edge('F', 'G')
dot.edge('G', 'H')
dot.edge('H', 'I')
dot.edge('I', 'J')
dot.edge('J', 'K')
dot.edge('K', 'L')
dot.edge('E', 'M', label='No')
dot.edge('M', 'L')
dot.edge('A', 'N')
dot.edge('N', 'O')
dot.edge('O', 'L')

# 순서도 파일 생성 및 저장
dot.render('flowchart', format='png', cleanup=True)
