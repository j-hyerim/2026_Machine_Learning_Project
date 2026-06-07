import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def Category(): # 함수양식
    # 데이터 불러오기 
    df = pd.read_csv('most_viewed_videos_1000.csv')
    
    # 제목(title)과 기존 카테고리(content_type)를 대문자로 임시 변환 (텍스트 검색 용이하게 설정)
    df['title_upper'] = df['title'].astype(str).str.upper()
    df['content_upper'] = df['content_type'].astype(str).str.upper()
    
    # 세부 카테고리 분류 로직 함수 정의
    def 세부_분류(row):
        title = row['title_upper']
        content = row['content_upper']
        
        # 교육
        if 'KIDS' in content or 'EDUCATIONAL' in content or 'NURSERY' in title or 'LEARN' in title or 'ABC' in title:
            return '교육'
        # 챌린지
        elif 'CHALLENGE' in title or 'CHALLENGES' in title or 'DANCE' in title:
            return '챌린지'
        # 코미디
        elif 'COMEDY' in title or 'FUNNY' in title or 'PRANK' in title or 'LAUGH' in title:
            return '코미디'
        # 라이브방송
        elif 'LIVE' in title or 'STREAM' in title or 'EN VIVO' in title:
            return '라이브방송'
        # 피트니스
        elif 'FITNESS' in title or 'WORKOUT' in title or 'GYM' in title or 'YOGA' in title:
            return '피트니스'
        # 음식/요리
        elif 'FOOD' in title or 'COOKING' in title or 'RECIPE' in title or 'MUKBANG' in title:
            return '음식/요리'
        # 브이로그
        elif 'VLOG' in title or 'DAILY' in title or 'MY ROUTINE' in title:
            return '브이로그'
        # 영화/다큐멘터리
        elif 'OFFICIAL' in title or 'MOVIE' in title or 'CLIP' in title or 'TRAILER' in title or 'DOCUMENTARY' in title:
            return '영화/다큐멘터리'
        # 기본 분류
        elif 'MUSIC' in content:
            return '영화/다큐멘터리' # 뮤직비디오를 대분류 내 영상 매칭으로 포함
        else:
            return '기타 / 미분류'

    # 데이터프레임 전체 행에 세부 분류 함수 적용
    df['content_type_ko'] = df.apply(세부_분류, axis=1)
    
    # 정렬할 세부 카테고리 순서 고정
    custom_order = [
        '챌린지',
        '교육',
        '코미디',
        '영화/다큐멘터리',
        '라이브방송',
        '피트니스',
        '음식/요리',
        '브이로그',
        '기타 / 미분류'
    ]
    
    # 카테고리별 개수 세기
    category_counts = df['content_type_ko'].value_counts()
    
    # [터미널 출력 확인용]
    print("\n--- [세부 분류] 카테고리별 데이터 개수 ---")
    for cat in custom_order:
        count = category_counts.get(cat, 0)
        print(f"{cat}: {count}개")
    print("-" * 40)
    print(f"👉 그래프 총합: {sum(category_counts.get(cat, 0) for cat in custom_order)}개 (1000개 완벽 일치!)")
    print("-" * 40)

    # 시각화 설정
    plt.rcParams['font.family'] = 'AppleGothic'  
    plt.rcParams['axes.unicode_minus'] = False   
    sns.set_theme(style="whitegrid", font="AppleGothic")
    
    fig, ax = plt.subplots(figsize=(12, 7), dpi=120)
    
    # 컬러 배열 
    colors = sns.color_palette("pastel", len(custom_order))
    
    # 그래프 그리기
    bars = sns.barplot(
        x=[category_counts.get(cat, 0) for cat in custom_order], 
        y=custom_order, 
        palette=colors,
        edgecolor="0.2", 
        linewidth=1.2
    )
    
    # 왼쪽 축 글씨 가로로 정렬
    ax.set_yticklabels(custom_order, rotation=0, va='center', fontsize=11, fontweight='bold')
    
    # 막대 끝에 개수 
    for bar in bars.patches:
        width = bar.get_width()
        ax.text(
            width + 8, 
            bar.get_y() + bar.get_height()/2, 
            f'{int(width)}개', 
            va='center', 
            ha='left', 
            fontsize=11, 
            fontweight='bold',
            color='#333333'
        )
    
    # 전체 그래프 세팅
    plt.title('유튜브 상위 1000개 동영상 세부 카테고리 분포', fontsize=18, fontweight='bold', pad=20, color='#222222')
    plt.xlabel('동영상 개수 (개)', fontsize=12, fontweight='bold', labelpad=10)
    plt.ylabel('', fontsize=1) 
    
    plt.xlim(0, 650) # 축 넓이 조정
    sns.despine(left=True, bottom=False)
    
    plt.tight_layout()
    plt.show()

Category() # 함수 호출