\# Rendu Séance 1



\*\*Nom et prénom :\*\* Ma Belle



\## Résumé de la séance



Dans cette séance, j'ai installé et vérifié Docker, forké le dépôt du cours, lancé MinIO localement,

créé un bucket de stockage objet (`anfa-raw`), généré une paire de clés applicatives, et écrit un

script Python qui dépose le référentiel d'Anfa (lignes, arrêts, bus, tarifs) dans ce bucket via l'API S3.



\## Étapes principales



1\. Vérification de l'installation de Docker (`docker --version`, `docker compose version`).

2\. Fork du dépôt `cloud-bigdata-anfa-resources` et création de la branche `seance-01`.

3\. Téléchargement et lancement de l'image MinIO (`docker run`).

4\. Configuration de l'alias `mc`, création du bucket `anfa-raw` et de la clé applicative `anfa-app-key`.

5\. Écriture et exécution du script `upload\\\_referentiel.py` pour uploader les 4 CSV du référentiel.

6\. Vérification visuelle dans la console MinIO.



\## Capture d'écran





\## Difficultés rencontrées



\-  confusion entre le port 9000

&#x20; et 9001,





\## Exercices d'application



Exercice 1 : QCM conceptuel

1.1 → D

1.2 → C 

1.3 → D 

1.4 → C 

1.5 → B

1.6 → C



Exercice 2



\-Google Compute Engine : IaaS (Infrastructure as a Service). Fournit une machine virtuelle brute. L'utilisateur gère lui-même le système d'exploitation, les logiciels et les applications.

\-AWS Lambda : FaaS (Function as a Service). Permet d'exécuter du code en réponse à des événements sans avoir à gérer de serveurs.

\-Snowflake : PaaS (Platform as a Service). Plateforme de données entièrement gérée sur laquelle les utilisateurs créent et exécutent des requêtes, analyses et pipelines de données.

\-Heroku : PaaS (Platform as a Service). Offre un environnement de déploiement d'applications sans nécessiter la gestion de l'infrastructure sous-jacente.

\-Microsoft 365 : SaaS (Software as a Service). Ensemble d'applications prêtes à l'emploi accessibles directement par l'utilisateur final.

\-Databricks : PaaS (Platform as a Service). Plateforme managée permettant l'exécution de traitements Big Data, Spark et Machine Learning, où l'utilisateur se concentre sur le développement du code.

\-Azure Functions : FaaS (Function as a Service). Service de fonctions serverless de Microsoft, déclenchées par des événements, similaire à AWS Lambda.

\-Tableau Online : SaaS (Software as a Service). Solution de Business Intelligence accessible via un navigateur web, sans installation ni gestion d'infrastructure.



Exercice 3 : Lecture et interprétation

3.1 



\-d : lance le conteneur en arrière-plan (mode détaché)

\--name analyse-anfa : nomme le conteneur "analyse-anfa"

\-p 8888:8888 : expose le port 8888 du conteneur sur le port 8888 de la machine hôte

\-v /home/koffi/notebooks:/notebooks : monte le dossier hôte dans le conteneur pour que les notebooks persistent même après l'arrêt du conteneur

\-e JUPYTER\_TOKEN=anfa-token : définit le token d'authentification pour accéder à Jupyter

jupyter/pyspark-notebook : l'image utilisée (Jupyter avec PySpark préinstallé)



Synthèse : Cette commande lance en arrière-plan un environnement Jupyter+PySpark accessible sur http://localhost:8888 avec le token anfa-token. Les notebooks créés sont sauvegardés sur la machine hôte grâce au montage du volume, donc ils survivent à l'arrêt ou la suppression du conteneur.

3.2



a. http://localhost:9000 (API S3) et http://localhost:9001 (console web)

b. Non, les données ne sont pas perdues. Elles sont stockées dans le volume nommé minio-data, qui existe indépendamment du conteneur. Supprimer le conteneur ne supprime pas le volume ; quand docker compose up -d recrée le conteneur, celui-ci remonte le même volume et retrouve toutes les données.

c. Le mot de passe (secret) est écrit en clair dans le fichier YAML — s'il est versionné sur Git, n'importe qui ayant accès au dépôt connaît les identifiants root du serveur. Il faudrait externaliser ce secret (variable d'environnement non commitée, gestionnaire de secrets).



Exercice 4 : Diagnostic



a. Le script utilise anfa-admin / anfa-password-2026 — les identifiants root du serveur — comme aws\_access\_key\_id/aws\_secret\_access\_key, alors que l'API S3 attend la clé applicative créée spécifiquement pour cet usage (anfa-app-key / anfa-app-secret-2026).

b. Remplacer dans le code :



python  aws\_access\_key\_id="anfa-app-key",

&#x20; aws\_secret\_access\_key="anfa-app-secret-2026",



c. Le compte root sert à l'administration du serveur (console web, gestion globale), tandis que les comptes de service (access key/secret key) sont les identifiants dédiés aux applications pour l'API S3. Ce sont deux mécanismes d'authentification différents, ce qui explique que les premiers identifiants fonctionnent pour la console mais pas pour les appels programmatiques.



Exercice 5 : Mini-cas d'architecture

a. Deux limites de l'architecture actuelle :



Un export CSV mensuel ne permet pas des prédictions "quasi temps réel chaque heure" : les données sont déjà obsolètes d'un mois.

Un PC personnel ne peut ni absorber les pics de charge, ni offrir un accès partagé simultané à plusieurs analystes, ni garantir une disponibilité continue.



b. Besoin → caractéristique NIST :



Pics de charge (vendredi soir, fêtes) → Élasticité rapide : la capacité de calcul s'ajuste automatiquement à la demande.

Tableau de bord partagé sans installation → Accès réseau étendu : accessible depuis n'importe quel appareil via le réseau.

Maîtrise des coûts → Service mesuré (pay-as-you-go) : on paie uniquement ce qu'on consomme.

Prédictions chaque heure sans intervention humaine → Self-service à la demande : les traitements se déclenchent automatiquement.



c. Modèles de service :



(i) Tableau de bord partagé → SaaS

(ii) Calcul des prédictions à l'heure → FaaS 

(iii) Stockage des données clients → IaaS 



d. Modèle de déploiement : Cloud hybride. Les données clients sensibles restent dans un environnement privé/contrôlé pour respecter la conformité, tandis que les traitements non sensibles (calcul, tableau de bord) profitent de l'élasticité du cloud public.

e. Trois stratégies anti-vendor-lock-in :



Utiliser des standards ouverts (API S3, compatible MinIO/AWS/GCP).

Conteneuriser les applications (Docker) pour faciliter la portabilité entre fournisseurs.

Privilégier les briques open source (PostgreSQL, Kafka, MinIO) plutôt que des services propriétaires sans équivalent.



