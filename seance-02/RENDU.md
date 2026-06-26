\# Rendu - Séance 2



\*\*Nom et prénom :\*\* Ama kwatcha

\*\*Identifiant GitHub :\*\* Mabelle95

\*\*Date de soumission :\*\* 26/06/2026



\## Résumé de la séance



Dans cette séance, j'ai écrit un Dockerfile pour conteneuriser un script PySpark d'analyse du référentiel

Anfa, construit et exécuté l'image obtenue, observé le fonctionnement du cache Docker, puis orchestré une

stack à 3 services (MinIO, Jupyter, mon image custom) avec Docker Compose. J'ai enfin exploré les données

de MinIO depuis un notebook Jupyter via boto3 et pandas.



\## Étapes principales



1\. Écriture du Dockerfile et construction de l'image `anfa-analyse:v1` (taille observée : 1.17 Go).

2\. Mise en place du `.dockerignore` et observation du cache de Docker : un rebuild sans modification

&#x20;  est quasi instantané (toutes les couches `CACHED`) ; une modification du code ne réinvalide que la

&#x20;  dernière couche (`COPY . .`), pas l'installation de PySpark.

3\. Écriture du `docker-compose.yml` orchestrant MinIO, Jupyter, et l'image custom `anfa-app`, avec un

&#x20;  healthcheck MinIO (`mc ready local`) et un `depends\_on: condition: service\_healthy` pour Jupyter.

4\. Rechargement du référentiel dans le nouveau volume MinIO via le script de la séance 1.

5\. Création du notebook `exploration\_minio.ipynb` qui lit les données depuis MinIO via boto3 et pandas.



\## Captures d'écran



\### docker compose ps



!\[docker compose ps](captures/docker-ps.png)



\### Notebook Jupyter



!\[Notebook Jupyter](captures/jupyter-pandas.png)



\## Bonus multi-stage (optionnel)



Non réalisé pour cette séance.



\## Réponses aux exercices d'application



(à compléter si des exercices sont fournis pour cette séance)



\## Difficultés rencontrées



\- Conflit de port/nom de conteneur `anfa-minio` : un conteneur du même nom existait déjà depuis la

&#x20; séance 1, résolu avec `docker stop anfa-minio` puis `docker rm anfa-minio`.

\- Problème réseau/DNS sur ma machine empêchant Docker de résoudre `auth.docker.io` (donc impossible

&#x20; de télécharger les images) : résolu en configurant le DNS de ma carte réseau sur 8.8.8.8 / 8.8.4.4.

\- Erreur `IndentationError` après une modification manuelle du script Python pour tester le cache

&#x20; Docker : corrigée en réécrivant la fonction `main()` avec une indentation cohérente (4 espaces).

\- Le stack Compose utilisant un nouveau volume nommé (`seance-02\_minio-data`, différent de celui de la

&#x20; séance 1), le bucket `anfa-raw` était vide au premier lancement : il a fallu recréer l'alias `mc`, le

&#x20; bucket, la clé applicative, et relancer le script d'upload du référentiel.

