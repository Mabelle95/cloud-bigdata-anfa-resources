"""
Séance 05 — Projet Anfa
========================
Lit le référentiel Anfa depuis la zone "raw" de MinIO (connecteur S3A),
calcule des statistiques globales et les heures de pointe,
puis écrit les résultats dans la zone "processed" (pattern data lake).

Usage local (sur la machine hôte, hors cluster) :
    spark-submit \
        --packages org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
        jobs/anfa_job.py --master local[*]

Usage cluster (dans le conteneur spark-master) :
    docker exec -it spark-master spark-submit \
        --master spark://spark-master:7077 \
        --packages org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
        /opt/bitnami/spark/jobs/anfa_job.py --master spark://spark-master:7077
"""

import argparse
import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

RAW_PATH = "s3a://anfa-raw/passages.csv"
PROCESSED_STATS_PATH = "s3a://anfa-processed/stats_globales"
PROCESSED_PEAK_PATH = "s3a://anfa-processed/heures_pointe"


def build_spark_session(master_url: str) -> SparkSession:
    """Crée la SparkSession avec la configuration S3A pour MinIO."""
    spark = (
        SparkSession.builder
        .appName("AnfaJob-Seance05")
        .master(master_url)
        .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


def run_job(spark: SparkSession):
    t0 = time.time()

    # ------------------------------------------------------------
    # 1. Lecture du référentiel depuis la zone "raw"
    # ------------------------------------------------------------
    print(f"[INFO] Lecture du référentiel depuis {RAW_PATH}")
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(RAW_PATH)
    )
    df.cache()
    print(f"[INFO] Nombre de lignes lues : {df.count()}")
    df.printSchema()

    # ------------------------------------------------------------
    # 2. Statistiques globales
    # ------------------------------------------------------------
    stats_globales = df.describe()

    # ------------------------------------------------------------
    # 3. Calcul des heures de pointe
    #    Colonne "horaire" (timestamp) et "nb_voyageurs" à agréger.
    # ------------------------------------------------------------
    df_heures = df.withColumn("heure", F.hour(F.col("horaire")))

    heures_pointe = (
        df_heures
        .groupBy("heure")
        .agg(
            F.count("*").alias("nb_passages"),
            F.sum("nb_voyageurs").alias("total_voyageurs"),
        )
        .orderBy(F.desc("total_voyageurs"))
    )

    print("[INFO] Top heures de pointe :")
    heures_pointe.show(10, truncate=False)

    # ------------------------------------------------------------
    # 4. Écriture des résultats dans la zone "processed"
    # ------------------------------------------------------------
    print(f"[INFO] Écriture des statistiques globales vers {PROCESSED_STATS_PATH}")
    stats_globales.write.mode("overwrite").parquet(PROCESSED_STATS_PATH)

    print(f"[INFO] Écriture des heures de pointe vers {PROCESSED_PEAK_PATH}")
    heures_pointe.write.mode("overwrite").parquet(PROCESSED_PEAK_PATH)

    duree = time.time() - t0
    print(f"[INFO] Job terminé en {duree:.2f} secondes")
    return duree


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--master",
        default="local[*]",
        help="URL du master Spark : local[*] ou spark://spark-master:7077",
    )
    args = parser.parse_args()

    spark = build_spark_session(args.master)
    try:
        run_job(spark)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()