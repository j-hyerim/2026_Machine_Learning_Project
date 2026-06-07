import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# [수칙 1] 한글 깨짐 방지 폰트 설정 (본인의 OS에 맞는 것 한 줄만 남기세요)
# =========================================================
plt.rc('font', family='Malgun Gothic')  # 윈도우(Windows) 사용자용
# plt.rc('font', family='AppleGothic')  # 맥(Mac) 사용자용
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


# 1. 데이터 로드 및 수치 변환
df = pd.read_csv('most_viewed_videos_1000.csv')

def convert_to_number(val):
    val = str(val).strip().upper()
    if 'B' in val: return float(val.replace('B', '')) * 1_000_000_000
    elif 'M' in val: return float(val.replace('M', '')) * 1_000_000
    elif 'K' in val: return float(val.replace('K', '')) * 1_000
    else: return float(val) if val.isdigit() else 0.0

df['views_num'] = df['views'].apply(convert_to_number)
df['likes_num'] = df['likes'].apply(convert_to_number)


# 2. [한국어 변환 수칙] 영어 데이터를 한국어 직관적인 단어로 매핑
df['영상 포맷'] = df['is_short'].map({0: '롱폼 (Longs)', 1: '쇼츠 (Shorts)'})
df['like_ratio'] = (df['likes_num'] / df['views_num']) * 100



# 3. 쇼츠 vs 롱폼 '제목 길이' 분포 비교 (박스 플롯)
plt.figure(figsize=(9, 5))
sns.set_theme(style="whitegrid", font='Malgun Gothic') # seaborn 환경에도 한글 폰트 지정

# 깔끔한 파스텔톤 컬러로 변경
sns.boxplot(x='영상 포맷', y='title_length', data=df, palette='pastel')

# 영어로 되어 있던 라벨들을 모두 한국어로 변경
plt.title('영상 포맷별 제목 글자 수 분포 비교', fontsize=15, fontweight='bold', pad=15)
plt.xlabel('영상 포맷', fontsize=12)
plt.ylabel('제목 글자 수 (자)', fontsize=12)
plt.tight_layout()
plt.show()

# 4. [두 번째 사진 수정] 쇼츠 vs 롱폼 '조회수 대비 좋아요 비율' 비교 (바 차트)
plt.figure(figsize=(9, 5))

# 바 차트 그리기 (errorbar=None으로 깔끔하게 막대만 표기)
ax = sns.barplot(x='영상 포맷', y='like_ratio', data=df, palette='Set2', errorbar=None)

# [수칙 2] 막대 그래프 위에 실제 수치(%)를 직접 적어주어 가독성 극대화
for p in ax.patches:
    ax.annotate(f"{p.get_height():.3f}%", 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 8), 
                textcoords='offset points', 
                fontsize=11, fontweight='bold')

plt.title('영상 포맷별 평균 좋아요 비율 (%) 비교', fontsize=15, fontweight='bold', pad=15)
plt.xlabel('영상 포맷', fontsize=12)
plt.ylabel('조회수 대비 좋아요 비율 (%)', fontsize=12)

# y축 범위를 살짝 넓혀서 숫자 라벨이 잘리지 않게 조절
plt.ylim(0, df.groupby('영상 포맷')['like_ratio'].mean().max() * 1.15) 
plt.tight_layout()
plt.show()