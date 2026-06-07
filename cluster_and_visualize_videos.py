import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 깨짐 방지 설정 (Windows 기준 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def cluster_and_visualize_videos():
    print("데이터를 불러오고 분석을 시작합니다. 잠시만 기다려주세요...\n")
    
    # 1. 데이터 불러오기
    df = pd.read_csv("most_viewed_videos_1000.csv")
    
    # 제목(title) 데이터가 없는 행(결측치) 안전하게 제거
    df = df.dropna(subset=['title']).copy()

    # 2. 텍스트 벡터화 (TF-IDF)
    # 글자를 컴퓨터가 계산할 수 있는 숫자(벡터)로 변환합니다.
    # stop_words='english'를 통해 'the', 'a', 'is' 같은 의미 없는 영어 단어는 제외합니다.
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(df['title'])

    # 3. K-Means 클러스터링
    # 비슷한 제목들끼리 5개의 그룹(클러스터)으로 묶습니다. (숫자는 원하시는 대로 변경 가능)
    num_clusters = 5
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)

    # 4. 시각화를 위한 차원 축소 (PCA)
    # 텍스트 벡터는 차원이 너무 높아 2차원 그래프(x, y)에 그릴 수 없으므로 차원을 압축합니다.
    pca = PCA(n_components=2, random_state=42)
    scatter_data = pca.fit_transform(X.toarray())
    
    df['x'] = scatter_data[:, 0]
    df['y'] = scatter_data[:, 1]

    # 5. 각 클러스터별 샘플 제목 3개씩 터미널에 출력 확인
    print("=== 클러스터링 결과 미리보기 ===")
    for i in range(num_clusters):
        print(f"\n[클러스터 {i}]")
        sample_titles = df[df['cluster'] == i]['title'].head(3).tolist()
        for title in sample_titles:
            print(f" - {title}")
            
    print("\n그래프 창을 띄웁니다!")

    # 6. Matplotlib & Seaborn 시각화
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        x='x', y='y',
        hue='cluster',           # 클러스터 번호에 따라 색상 다르게 지정
        palette='Set2',          # 색상 테마
        data=df,
        alpha=0.7,               # 점 투명도
        s=50                     # 점 크기
    )
    
    plt.title('유튜브 영상 제목 클러스터링 결과 (K-Means)', fontsize=16)
    plt.xlabel('특성 1 (PCA 1)')
    plt.ylabel('특성 2 (PCA 2)')
    plt.legend(title='그룹(Cluster)')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # 그래프를 화면에 출력
    plt.show()
    
# 파이썬 스크립트 실행 시 함수 호출
if __name__ == "__main__":
    cluster_and_visualize_videos()
    