\# Rendu Séance 1



\*\*Nom et prénom :\*\* Ama kwatcha



\## Résumé de la séance



Dans cette séance, j'ai installé et vérifié Docker, forké le dépôt du cours, lancé MinIO localement,

créé un bucket de stockage objet (`anfa-raw`), généré une paire de clés applicatives, et écrit un

script Python qui dépose le référentiel d'Anfa (lignes, arrêts, bus, tarifs) dans ce bucket via l'API S3.



\## Étapes principales



1\. Vérification de l'installation de Docker (`docker --version`, `docker compose version`).

2\. Fork du dépôt `cloud-bigdata-anfa-resources` et création de la branche `seance-01`.

3\. Téléchargement et lancement de l'image MinIO (`docker run`).

4\. Configuration de l'alias `mc`, création du bucket `anfa-raw` et de la clé applicative `anfa-app-key`.

5\. Écriture et exécution du script `upload\_referentiel.py` pour uploader les 4 CSV du référentiel.

6\. Vérification visuelle dans la console MinIO.



\## Capture d'écran



!\[Bucket anfa-raw](captures/bucket-anfa-raw.png)



\## Difficultés rencontrées



\- (décrivez ici les difficultés que vous avez réellement eues, par exemple : confusion entre le port 9000

&#x20; et 9001, ou le copier-coller de commandes multi-lignes dans PowerShell qui nécessite l'accent grave

&#x20; (`` ` ``) au lieu du backslash (`\\`) utilisé sous Linux/macOS).



\## Exercices d'application



(à compléter)



