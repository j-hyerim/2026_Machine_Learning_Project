import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import numpy as np

# ---------------------------------------------------
# 1. 폰트 및 시각화 환경 설정
# ---------------------------------------------------
# OS에 따른 한글 폰트 설정 (조장님의 컴퓨터 환경에 맞춰서 작동합니다)
if platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'

plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# ---------------------------------------------------
# 2. 데이터 불러오기
# ---------------------------------------------------
file_path = r"most_viewed_videos_1000.csv"
df = pd.read_csv(file_path)

# ---------------------------------------------------
# 3. 데이터 전처리 (B, M 등의 단위를 숫자로 변환)
# ---------------------------------------------------
# '16.8B', '46.4M' 같은 문자열을 계산 가능한 실수형 숫자로 바꾸는 함수
def syl():
    def convert_to_number(value):
        if pd.isna(value):
            return np.nan
        
        value_str = str(value).strip().upper()
        
        # 0인 경우 그대로 반환
        if value_str == '0':
            return 0.0
            
        try:
            if value_str.endswith('B'):
                return float(value_str[:-1]) * 1_000_000_000 # 십억
            elif value_str.endswith('M'):
                return float(value_str[:-1]) * 1_000_000     # 백만
            elif value_str.endswith('K'):
                return float(value_str[:-1]) * 1_000         # 천
            else:
                return float(value_str)
        except ValueError:
            return np.nan # 변환할 수 없는 이상한 값은 결측치 처리

    # 실제 컬럼명('views', 'likes')에 함수 적용하여 새로운 숫자형 컬럼 생성
    df['views_num'] = df['views'].apply(convert_to_number)
    df['likes_num'] = df['likes'].apply(convert_to_number)

    # 결측치가 있는 행 제거
    df_clean = df.dropna(subset=['views_num', 'likes_num'])

    # ---------------------------------------------------
    # 4. 상관관계 분석
    # ---------------------------------------------------
    correlation = df_clean['views_num'].corr(df_clean['likes_num'])
    print("=" * 50)
    print(f"📌 [분석 결과] 조회수와 좋아요 수의 상관계수: {correlation:.4f}")

    if correlation > 0.7:
        print("   -> 강한 양의 상관관계가 있습니다. (조회수가 높을수록 좋아요도 많음)")
    elif correlation > 0.3:
        print("   -> 약한 양의 상관관계가 있습니다.")
    else:
        print("   -> 상관관계가 거의 없거나 추가 분석이 필요합니다.")
    print("=" * 50)

    # ---------------------------------------------------
    # 5. 데이터 시각화 (산점도 및 회귀선)
    # ---------------------------------------------------
    plt.figure(figsize=(10, 6))

    # 숫자 단위가 너무 커서 보기 힘들 수 있으므로, 단위를 '백만(Million)' 단위로 스케일링해서 시각화합니다.
    df_clean['views_million'] = df_clean['views_num'] / 1_000_000
    df_clean['likes_million'] = df_clean['likes_num'] / 1_000_000

    # 산점도 및 추세선 그리기
    sns.regplot(x='views_million', y='likes_million', data=df_clean, 
                scatter_kws={'alpha': 0.5, 'color': '#2ca02c', 's': 30}, 
                line_kws={'color': 'red', 'linewidth': 2})

    plt.title('유튜브 영상 조회수와 좋아요 수의 관계 분석', fontsize=16, pad=15)
    plt.xlabel('조회수 (단위: 백만)', fontsize=12)
    plt.ylabel('좋아요 수 (단위: 백만)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)

    # ---------------------------------------------------
    # 6. 결과 저장 및 출력
    # ---------------------------------------------------
    output_image = 'youtube_views_likes_correlation.png'
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"📊 시각화 그래프가 '{output_image}' 파일로 저장되었습니다.")

    # 화면에 그래프 띄우기
    plt.show()


syl()