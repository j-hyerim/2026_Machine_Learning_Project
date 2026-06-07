import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def convert_to_number(x):
    if isinstance(x, (int, float)):
        return x

    x = str(x).strip()

    if x.endswith('K'):
        return float(x[:-1]) * 1_000
    elif x.endswith('M'):
        return float(x[:-1]) * 1_000_000
    elif x.endswith('B'):
        return float(x[:-1]) * 1_000_000_000
    else:
        try:
            return float(x)
        except:
            return 0


def ClusteringFunc(csv_file="most_viewed_videos_1000.csv", n_clusters=3, show_plot=True):

    df = pd.read_csv(csv_file)

    df['views'] = df['views'].apply(convert_to_number)
    df['likes'] = df['likes'].apply(convert_to_number)

    features = ['views', 'likes']
    df_clean = df[features].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    result_df = df.loc[df_clean.index].copy()
    result_df['Cluster'] = labels

    # ✔ 결과 출력
    print("\n===== 클러스터 결과 =====")
    print(result_df[['views', 'likes', 'Cluster']].head(20))

    # ✔ 시각화
    if show_plot:
        plt.figure(figsize=(8, 6))

        for c in range(n_clusters):
            cluster_data = result_df[result_df['Cluster'] == c]
            plt.scatter(
                cluster_data['views'],
                cluster_data['likes'],
                label=f'Cluster {c}',
                alpha=0.6
            )

        plt.xlabel("Views")
        plt.ylabel("Likes")
        plt.title("K-Means Clustering (Views vs Likes)")
        plt.legend()
        plt.grid(True)
        plt.show()

    return result_df


if __name__ == "__main__":
    ClusteringFunc()