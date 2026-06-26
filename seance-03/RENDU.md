\# Rendu Séance 3



\*\*Nom et prénom :\*\* Ama kwatcha

\*\*Identifiant GitHub :\*\* Mabelle95

\*\*Date de soumission :\*\* 26/06/2026



\## Résumé de la séance



Dans cette séance, j'ai installé Kind et kubectl, créé un cluster Kubernetes local nommé `anfa`, configuré un

namespace dédié, puis déployé MinIO via 3 manifestes YAML (PVC, Deployment, Service). J'ai observé concrètement

le self-healing en supprimant un pod manuellement, scalé le Deployment de 1 à 3 replicas puis inversement, et

activé l'Ingress Controller nginx.



\## Étapes principales



1\. Installation de Kind (v0.32.0) et kubectl (v1.32.2), création du cluster `anfa` (image kindest/node:v1.35.1).

2\. Création du namespace `anfa` et configuration de kubectl pour l'utiliser par défaut.

3\. Déploiement de MinIO via 3 manifestes YAML (PVC 2Gi, Deployment, Service NodePort 30900/30901).

4\. Accès à la console MinIO via `kubectl port-forward` (le NodePort de Kind n'étant pas accessible directement).

5\. Observation du self-healing après suppression manuelle d'un pod : Kubernetes en a recréé un nouveau

&#x20;  automatiquement, sans aucune intervention de ma part.

6\. Scaling du Deployment de 1 à 3 replicas, puis retour à 1.

7\. Activation de l'Ingress Controller nginx (aperçu, sans configuration HTTP complète).



\## Captures d'écran



\### Console MinIO accessible via port-forward



!\[Console MinIO](captures/console-minio.png)



\### Self-healing observé



!\[Pod recréé](captures/self-healing.png)



\### Scaling à 3 replicas



!\[3 replicas MinIO](captures/scaling-3-replicas.png)



\## Réponses aux exercices d'application



\### Exercice 1 : QCM conceptuel



1.1 → \*\*B\*\*. Kubernetes ne fournit pas son propre moteur de conteneurs ; il délègue l'exécution à un container

runtime (containerd, CRI-O, etc.) via l'interface CRI.



1.2 → \*\*B (etcd)\*\*. C'est la base de données clé-valeur qui stocke l'état complet et la source de vérité du cluster.



1.3 → \*\*C (Scheduler)\*\*. Il décide du placement des pods sur les nœuds selon les ressources disponibles.



1.4 → \*\*C (API Server)\*\*. kubectl ne parle jamais directement à etcd, au Scheduler ou aux pods ; tout passe par

l'API Server.



1.5 → \*\*B\*\*. Le Deployment (via son ReplicaSet) recrée immédiatement un nouveau pod pour respecter l'état souhaité.



1.6 → \*\*B (NodePort)\*\*. Il ouvre un port fixe sur chaque nœud du cluster, sans nécessiter de load balancer cloud.



1.7 → \*\*B\*\*. Cette commande modifie l'état souhaité à 5 replicas ; Kubernetes converge ensuite vers ce nombre.



1.8 → \*\*B\*\*. Un Namespace isole logiquement les ressources (équipe, environnement, application).



1.9 → \*\*B\*\*. Avec Kind, chaque "nœud" du cluster est en réalité un conteneur Docker — je l'ai vérifié avec

`docker ps`, qui montre le conteneur `anfa-control-plane`.



\### Exercice 2 : Lecture et interprétation d'un manifeste



2.1 Le `selector.matchLabels` indique au Deployment quels pods il doit gérer (créer, surveiller, remplacer) :

seuls les pods dont les labels correspondent à ce sélecteur sont sous sa responsabilité. Les pods créés à

partir de `template.metadata.labels` portent exactement ces labels, donc le Deployment les reconnaît

automatiquement comme siens.



2.2 2 pods seront créés (`replicas: 2`). Si l'un meurt, le ReplicaSet détecte l'écart entre l'état observé et

l'état souhaité, et recrée automatiquement un nouveau pod.



2.3 `minio` fonctionne grâce au DNS interne du cluster (CoreDNS) : un Service nommé `minio` obtient

automatiquement une entrée DNS résolvable depuis n'importe quel pod du même namespace, ce qui évite de coder

une IP de pod (éphémère).



2.4 Sans Service, l'API n'a aucune adresse stable ni point d'entrée réseau cohérent ; les autres pods ne

peuvent pas la joindre de façon fiable, et il n'y a aucun load-balancing entre les replicas.



2.5

```yaml

apiVersion: v1

kind: Service

metadata:

&#x20; name: anfa-api

&#x20; namespace: anfa

spec:

&#x20; selector:

&#x20;   app: anfa-api

&#x20; ports:

&#x20;   - port: 80

&#x20;     targetPort: 8000

&#x20; type: ClusterIP

```



\### Exercice 3 : Diagnostic



3.1

a. `ImagePullBackOff` signifie que Kubernetes n'arrive pas à télécharger l'image et réessaie avec un délai

croissant (backoff exponentiel).

b. Coquille dans le nom de l'image : `minio/miniooo:latest` n'existe pas, c'est une faute de frappe pour

`minio/minio:latest`.

c. `kubectl describe pod minio-7d9f8b6c5-x2k9p` (section Events).



3.2

a. `Pending` signifie que la PVC n'a pas encore été liée à un PersistentVolume correspondant à sa demande.

b. Sur un cluster Kind local, le provisioner local ne dispose probablement pas de 500 Gi de stockage

disponible sur le disque hôte.

c. `kubectl describe pvc data-pvc` et `kubectl get storageclass`.



3.3

a. `port-forward` a besoin d'un pod en cours d'exécution (`Running`) pour rediriger le trafic ; ici le pod

est encore `Pending`.

b. `kubectl describe pod <nom-du-pod>`.

c. Ordre logique : 1) appliquer les manifestes, 2) vérifier que le pod passe en `Running`, 3) lancer le

port-forward.



\### Exercice 4 : De Docker Compose à Kubernetes



4.1 Au minimum 3 manifestes : un Deployment (conteneur MinIO), un Service (exposition réseau), et une

PersistentVolumeClaim (persistance, remplace le volume nommé Docker).



4.2 Un volume Docker nommé est géré par le moteur Docker sur une seule machine. Une PVC Kubernetes est une

demande abstraite de stockage, liée dynamiquement à un PersistentVolume par le cluster, ce qui découple la

demande de stockage du nœud physique sur lequel le pod est planifié.



4.3 En Compose, tout tourne sur un seul hôte donc le port est lié directement. Avec Kind, les nœuds sont

eux-mêmes des conteneurs Docker : un NodePort expose un port sur ces nœuds, pas directement sur localhost,

d'où le besoin du port-forward. Pour un accès direct, il faudrait configurer des `extraPortMappings` à la

création du cluster Kind, ou utiliser MetalLB.



4.4 Deux apports observés concrètement : (1) l'auto-réparation (self-healing) : un pod supprimé est recréé

automatiquement ; (2) le scaling déclaratif : `kubectl scale --replicas=N` ajuste le nombre d'instances en

une commande, capacité absente de Compose.



\### Exercice 5 : Mini-cas d'architecture



5.1

\- `pipeline-anfa` → \*\*CronJob\*\* : tâche planifiée (2h du matin), durée fixe, qui se termine.

\- `anfa-api` → \*\*Deployment\*\* : service permanent, sans état persistant, scalable.

\- `anfa-dashboard` → \*\*Deployment\*\* : service long-running, sans besoin de stockage avec état.



5.2 `minReplicas: 2`, `maxReplicas: 10`, métrique cible : utilisation CPU \~65-70%. Le ratio creux/pic

(\~5 req/s à \~50 req/s) justifie une fourchette large, avec un minimum garantissant la disponibilité.



5.3 \*\*LoadBalancer\*\* — cluster managé chez un fournisseur cloud, nécessaire pour une IP stable accessible

depuis les applications mobiles des conducteurs.



5.4 Kubernetes utilise par défaut une stratégie de Rolling Update : il crée de nouveaux pods avec la

nouvelle image tout en gardant les anciens actifs, ne bascule le trafic qu'une fois les nouveaux `Ready`,

puis retire les anciens progressivement — évitant une coupure complète.



5.5

```yaml

apiVersion: apps/v1

kind: Deployment

metadata:

&#x20; name: anfa-api

spec:

&#x20; replicas: 3

&#x20; selector:

&#x20;   matchLabels:

&#x20;     app: anfa-api

&#x20; template:

&#x20;   metadata:

&#x20;     labels:

&#x20;       app: anfa-api

&#x20;   spec:

&#x20;     containers:

&#x20;       - name: api

&#x20;         image: anfa/api:v1

&#x20;         ports:

&#x20;           - containerPort: 8000

&#x20;         env:

&#x20;           - name: MINIO\_ENDPOINT

&#x20;             value: "http://minio:9000"

```



\## Difficultés rencontrées



\- Le PVC est resté en statut `Pending` juste après sa création : comportement normal lié au mode

&#x20; `WaitForFirstConsumer` du StorageClass de Kind (le volume n'est provisionné qu'au moment où un pod

&#x20; l'utilise réellement), il est passé en `Bound` dès le déploiement du pod MinIO.

\- Le NodePort n'est pas directement accessible depuis l'hôte avec Kind : j'ai dû utiliser

&#x20; `kubectl port-forward` dans deux terminaux séparés (un par port) pour accéder à la console MinIO.

\- Difficulté à retrouver mes captures d'écran prises avec Win+Maj+S : l'outil copie l'image dans le

&#x20; presse-papiers sans créer de fichier automatiquement, il faut la coller dans Paint puis l'enregistrer

&#x20; explicitement.



