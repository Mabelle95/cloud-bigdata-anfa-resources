\# Rendu - SÃ©ance 4



\*\*Nom et prÃ©nom :\*\* Ama kwatcha

\*\*Identifiant GitHub :\*\* Mabelle95

\*\*Date de soumission :\*\* 30/06/2026



\## RÃ©sumÃ© de la sÃ©ance



Dans cette sÃ©ance, j'ai installÃ© Terraform et Ã©crit mon premier fichier main.tf, maÃ®trisÃ© le workflow

init/plan/apply/destroy, compris le rÃ´le du fichier terraform.tfstate et pourquoi il ne se commit jamais,

dÃ©crit une stack complÃ¨te (rÃ©seau, volume, conteneur MinIO) en HCL, observÃ© des changements incrÃ©mentaux,

puis refactorisÃ© le code avec des variables et un fichier terraform.tfvars.



\## Ã‰tapes principales



1\. Installation de Terraform (v1.15.7) et Ã©criture du premier `main.tf` minimal (image + conteneur MinIO).

2\. MaÃ®trise du workflow `init` -> `plan` -> `apply` -> `destroy`.

3\. Observation du fichier `terraform.tfstate` (contient les secrets en clair) et mise en place du `.gitignore`

   Terraform pour ne jamais le committer.

4\. Stack complÃ¨te : ajout d'un rÃ©seau Docker et d'un volume nommÃ©, conteneur MinIO attachÃ© aux deux.

5\. Test d'un changement incrÃ©mental : modification du mot de passe MinIO -> Terraform recrÃ©e uniquement le

   conteneur (les variables d'environnement ne sont pas modifiables a chaud), le rÃ©seau et le volume sont

   conservÃ©s.

6\. Refactoring en variables (`variables.tf`), valeurs fournies via `terraform.tfvars` (ignorÃ© par Git) et

   `terraform.tfvars.example` (versionnÃ©).

7\. Destruction propre de toute l'infrastructure avec `terraform destroy`.



\## Captures d'Ã©cran



\### terraform plan (crÃ©ation initiale)



!\[terraform plan](captures/terraform-plan.png)



\### terraform apply rÃ©ussi



!\[terraform apply](captures/terraform-apply.png)



\### Console MinIO crÃ©Ã©e par Terraform



!\[Console MinIO](captures/console-minio-tf.png)



\### terraform destroy





\## RÃ©ponses aux exercices d'application



\### Exercice 1 : QCM conceptuel



1.1 -> \*\*B\*\*. L'IaC ne remplace pas la nÃ©cessitÃ© de comprendre l'infrastructure sous-jacente ; c'est un outil

qui automatise et fiabilise sa crÃ©ation, pas un substitut Ã  la comprÃ©hension de ce qu'on dÃ©ploie.



1.2 -> \*\*B\*\*. Le dÃ©claratif dÃ©crit l'Ã©tat souhaitÃ© (ce qu'on veut obtenir), l'impÃ©ratif dÃ©crit la sÃ©quence

d'actions Ã  exÃ©cuter pour y arriver.



1.3 -> \*\*B\*\*. Une opÃ©ration idempotente produit le mÃªme rÃ©sultat peu importe le nombre de fois oÃ¹ elle est

appliquÃ©e -- exactement ce qu'on a observÃ© avec `terraform apply` relancÃ© sans changement (`No changes`).



1.4 -> \*\*B\*\*. Un provider est un plugin qui sait communiquer avec une API spÃ©cifique (ici Docker), permettant

Ã  Terraform de crÃ©er/modifier/dÃ©truire des ressources via cette API.



1.5 -> \*\*B\*\*. Terraform compare le state au code, ne voit aucun Ã©cart, et n'effectue aucune action --

confirmÃ© concrÃ¨tement dans le TP avec le message `No changes. Your infrastructure matches the configuration.`



1.6 -> \*\*C\*\*. Le `terraform.tfstate` mÃ©morise ce que Terraform a crÃ©Ã© (IDs, attributs) pour pouvoir calculer

les changements incrÃ©mentaux lors des prochains `plan`/`apply`.



1.7 -> \*\*B\*\*. Il peut contenir des secrets en clair (vu concrÃ¨tement : le mot de passe MinIO apparaissait dans

mon `terraform.tfstate`), et des commits concurrents sur ce fichier JSON peuvent le corrompre.



1.8 -> \*\*B (`terraform plan`)\*\*. C'est la commande qui prÃ©visualise les changements sans rien appliquer.



1.9 -> \*\*B\*\*. OpenTofu est un fork open source de Terraform, crÃ©Ã© aprÃ¨s le changement de licence de

HashiCorp en 2023 (passage du MPL Ã  la BUSL).



1.10 -> \*\*B\*\*. Terraform provisionne l'infrastructure (crÃ©er des machines, rÃ©seaux, conteneurs...), Ansible

configure des machines dÃ©jÃ  existantes (installer des paquets, gÃ©rer des fichiers de config...) -- les deux

sont complÃ©mentaires, pas concurrents.



\### Exercice 2 : Lecture et interprÃ©tation d'un fichier Terraform



2.1 Les 4 resources :

- `docker\_network.back` : crÃ©e le rÃ©seau Docker `anfa-backend`.

- `docker\_volume.data` : crÃ©e le volume nommÃ© `postgres-data` pour la persistance.

- `docker\_image.postgres` : tÃ©lÃ©charge/rÃ©fÃ©rence l'image `postgres:15`.

- `docker\_container.db` : crÃ©e le conteneur PostgreSQL, attachÃ© au rÃ©seau et au volume, avec ses variables

  d'environnement et son port exposÃ©.



2.2 `docker\_image.postgres.image\_id` est une rÃ©fÃ©rence Ã  l'attribut `image\_id` de la resource

`docker\_image.postgres` dÃ©finie plus haut dans le fichier. Par rapport Ã  Ã©crire `image = "postgres:15"`

directement, cette rÃ©fÃ©rence crÃ©e une dÃ©pendance explicite entre les deux resources : Terraform sait qu'il

doit crÃ©er/mettre Ã  jour l'image avant le conteneur, et utilise l'ID rÃ©el de l'image construite (le digest),

ce qui garantit que le conteneur redÃ©marre automatiquement si l'image change, sans avoir Ã  le faire

manuellement.



2.3 Terraform crÃ©era dans cet ordre : `docker\_network.back` et `docker\_volume.data` et `docker\_image.postgres`

en parallÃ¨le (aucune dÃ©pendance entre eux), puis `docker\_container.db` en dernier, car il rÃ©fÃ©rence les trois

autres resources (rÃ©seau, volume, image) via leurs attributs. Terraform construit ce graphe de dÃ©pendances

automatiquement Ã  partir des rÃ©fÃ©rences dans le code.



2.4 Le problÃ¨me principal est le mot de passe `POSTGRES\_PASSWORD=secret123` Ã©crit \*\*en clair\*\* directement

dans le code source, qui sera donc versionnÃ© dans Git si ce fichier est commitÃ©. Correction concrÃ¨te :

extraire le mot de passe dans une variable sensible, fournie via un fichier `.tfvars` ignorÃ© par Git.



```hcl

variable "postgres\_password" {

  description = "Mot de passe de la base PostgreSQL"

  type        = string

  sensitive   = true

}



\# Dans le conteneur :

env = \[

  "POSTGRES\_DB=anfa",

  "POSTGRES\_USER=anfa\_user",

  "POSTGRES\_PASSWORD=${var.postgres\_password}",

]

```



2.5 AprÃ¨s `terraform destroy`, plus aucune resource n'existe (state vide). En modifiant `external = 5432` en

`external = 5433` puis en relanÃ§ant `terraform apply`, Terraform va recrÃ©er \*\*toute l'infrastructure\*\* depuis

zÃ©ro (les 4 resources), puisque le destroy prÃ©cÃ©dent a tout supprimÃ© -- ce n'est pas un changement incrÃ©mental

dans ce cas prÃ©cis, juste une recrÃ©ation complÃ¨te avec la nouvelle configuration de port.



\### Exercice 3 : Diagnostic



3.1 - DÃ©pendance circulaire

a. Cette erreur signifie que Terraform a dÃ©tectÃ© un cycle dans le graphe de dÃ©pendances : `docker\_container.a`

dÃ©pend de `docker\_container.b` (pour son nom) et `docker\_container.b` dÃ©pend de `docker\_container.a` -- aucun

des deux ne peut donc Ãªtre crÃ©Ã© en premier.

b. Terraform construit un graphe de dÃ©pendances acyclique pour dÃ©terminer l'ordre de crÃ©ation des ressources.

Un cycle rend cet ordre impossible Ã  calculer : il faudrait crÃ©er A avant B, et B avant A simultanÃ©ment.

c. Solution : casser le cycle en supprimant la rÃ©fÃ©rence directe entre les deux conteneurs. Par exemple,

utiliser des noms fixes (chaÃ®nes littÃ©rales) au lieu de rÃ©fÃ©rences croisÃ©es, ou introduire une Ã©tape

intermÃ©diaire (comme un rÃ©seau partagÃ© nommÃ©) Ã  laquelle les deux conteneurs se rÃ©fÃ¨rent indÃ©pendamment.



3.2 - RecrÃ©ation du conteneur

a. Terraform marque `-/+` (recrÃ©ation) plutÃ´t que `\~` (modification en place) parce que Docker ne permet pas

de modifier les variables d'environnement d'un conteneur dÃ©jÃ  crÃ©Ã© sans le redÃ©marrer entiÃ¨rement -- c'est

une limitation du moteur Docker lui-mÃªme, pas de Terraform.

b. Non, les donnÃ©es ne seront pas perdues, Ã  condition que le volume soit un volume nommÃ© Docker sÃ©parÃ©

(comme `docker\_volume.minio\_data` dans notre TP) : le conteneur est dÃ©truit et recrÃ©Ã©, mais le volume qui lui

est attachÃ© persiste indÃ©pendamment du cycle de vie du conteneur.

c. Non, ce n'est pas totalement "gratuit" en production : la recrÃ©ation entraÃ®ne une \*\*coupure de service\*\*

le temps que l'ancien conteneur s'arrÃªte et que le nouveau dÃ©marre (quelques secondes Ã  quelques dizaines de

secondes selon l'image). Pour un service critique avec exigence de haute disponibilitÃ©, il faudrait prÃ©voir

plusieurs replicas ou une stratÃ©gie de dÃ©ploiement progressif pour Ã©viter cette interruption.



3.3 - State corrompu

a. Le problÃ¨me de sÃ©curitÃ© immÃ©diat est que tous les secrets contenus dans le state (mots de passe, clÃ©s,

tokens) sont dÃ©sormais \*\*exposÃ©s publiquement\*\* sur GitHub, visibles par quiconque a accÃ¨s au dÃ©pÃ´t (ou au

monde entier si le dÃ©pÃ´t est public).

b. Le risque technique est que d'Ã©ventuelles modifications locales sur la machine d'Awa (resources crÃ©Ã©es ou

dÃ©truites entre-temps) ne soient pas reflÃ©tÃ©es dans ce state rÃ©cupÃ©rÃ© : Terraform pourrait tenter de

recrÃ©er des resources dÃ©jÃ  existantes, ou de dÃ©truire des resources que ce state ignore, menant Ã  des

conflits ou Ã  la perte/duplication de ressources.

c. La solution pÃ©renne est d'utiliser un \*\*remote backend\*\* partagÃ© (par exemple Terraform Cloud, ou un

bucket S3 avec verrouillage via DynamoDB), qui centralise le state, gÃ¨re les accÃ¨s concurrents avec un

systÃ¨me de verrouillage (lock), et ne nÃ©cessite jamais de committer le fichier dans Git.



\### Exercice 4 : Adaptation Compose -> Terraform



```hcl

terraform {

  required\_providers {

    docker = {

      source  = "kreuzwerker/docker"

      version = "\~> 3.0"

    }

  }

}



provider "docker" {}



variable "minio\_root\_password" {

  description = "Mot de passe administrateur MinIO"

  type        = string

  sensitive   = true

}



resource "docker\_network" "anfa\_net" {

  name = "anfa-network"

}



resource "docker\_volume" "minio\_data" {

  name = "minio-data"

}



resource "docker\_image" "minio" {

  name = "minio/minio:latest"

}



resource "docker\_image" "jupyter" {

  name = "jupyter/scipy-notebook:latest"

}



resource "docker\_container" "minio" {

  name    = "anfa-minio"

  image   = docker\_image.minio.image\_id

  command = \["server", "/data", "--console-address", ":9001"]



  ports {

    internal = 9000

    external = 9000

  }

  ports {

    internal = 9001

    external = 9001

  }



  env = \[

    "MINIO\_ROOT\_USER=anfa-admin",

    "MINIO\_ROOT\_PASSWORD=${var.minio\_root\_password}",

  ]



  volumes {

    volume\_name    = docker\_volume.minio\_data.name

    container\_path = "/data"

  }



  networks\_advanced {

    name = docker\_network.anfa\_net.name

  }

}



resource "docker\_container" "jupyter" {

  name  = "anfa-jupyter"

  image = docker\_image.jupyter.image\_id



  ports {

    internal = 8888

    external = 8888

  }



  env = \[

    "JUPYTER\_TOKEN=anfa-token",

  ]



  networks\_advanced {

    name = docker\_network.anfa\_net.name

  }



  depends\_on = \[docker\_container.minio]

}

```



\### Exercice 5 : Mini-cas d'architecture



5.1 Au moins 4 types de resources : un \*\*bucket de stockage objet\*\* (pour les CSV et logs GPS chez OVHcloud,

souverainetÃ© des donnÃ©es), un \*\*cluster Kubernetes managÃ©\*\* (pour hÃ©berger Spark avec Ã©lasticitÃ©), un

\*\*groupe de sÃ©curitÃ© / pare-feu rÃ©seau\*\* (pour contrÃ´ler les accÃ¨s), et une \*\*adresse IP publique / load

balancer\*\* (pour exposer le dashboard Grafana publiquement).



5.2 Je recommande l'option \*\*B (plusieurs fichiers sÃ©parÃ©s)\*\*. Un seul fichier de 800 lignes devient vite

difficile Ã  lire, Ã  parcourir et Ã  faire relire par l'Ã©quipe (code review) ; sÃ©parer par domaine fonctionnel

(rÃ©seau, stockage, calcul, supervision) facilite la navigation, rÃ©duit les risques de conflits Git lors du

travail Ã  plusieurs, et permet de comprendre rapidement oÃ¹ se trouve telle ou telle resource sans tout

parcourir.



5.3 Deux mÃ©canismes Terraform pour gÃ©rer plusieurs environnements : (1) des \*\*fichiers `.tfvars` sÃ©parÃ©s par

environnement\*\* (`dev.tfvars`, `prod.tfvars`), appliquÃ©s via `terraform apply -var-file=...` ; (2) les

\*\*workspaces Terraform\*\* (`terraform workspace new dev`), qui permettent de maintenir des states distincts

pour chaque environnement avec la mÃªme base de code.



5.4 La migration ne sera \*\*pas triviale\*\*, mais ne sera pas non plus une rÃ©Ã©criture totale. Ce qui se

transpose facilement : la structure gÃ©nÃ©rale du code (resources, variables, dÃ©pendances) et la logique

mÃ©tier de l'infrastructure restent les mÃªmes conceptuellement. Ce qui demande du travail : chaque provider

cloud (OVHcloud, AWS) a ses propres types de resources, noms d'attributs et mÃ©canismes d'authentification --

il faudra rÃ©Ã©crire concrÃ¨tement chaque bloc `resource` avec le provider AWS, et potentiellement adapter

certains concepts qui n'ont pas d'Ã©quivalent direct (un bucket OVH n'est pas configurÃ© exactement comme un

bucket S3 AWS, par exemple).



5.5 Trois bonnes pratiques pour une Ã©quipe de 4 personnes : (1) mettre en place un \*\*remote backend partagÃ©

avec verrouillage\*\* (Terraform Cloud ou S3+DynamoDB) pour Ã©viter les conflits de state et les Ã©tats

corrompus ; (2) imposer une \*\*revue de code (pull request)\*\* systÃ©matique avant tout `terraform apply` en

production, avec le `terraform plan` joint Ã  la review pour visualiser l'impact ; (3) dÃ©finir une

\*\*convention de nommage et de structure de fichiers\*\* commune (comme network.tf/storage.tf/compute.tf) dÃ¨s

le dÃ©part, documentÃ©e dans un README, pour que chacun sache oÃ¹ ajouter ou trouver une resource.



\## DifficultÃ©s rencontrÃ©es



- AprÃ¨s l'installation de Terraform via winget, la commande `terraform` n'Ã©tait pas reconnue mÃªme aprÃ¨s

  rÃ©ouverture du terminal (PATH non mis Ã  jour) : rÃ©solu en crÃ©ant un alias PowerShell pointant directement

  vers le binaire installÃ©.

- Plusieurs fois, mes modifications dans Notepad ne semblaient pas s'enregistrer (le fichier gardait son

  ancien contenu) : rÃ©solu en vÃ©rifiant systÃ©matiquement le contenu du fichier avec `Get-Content` juste

  aprÃ¨s chaque Ã©dition, avant de relancer une commande Terraform.

- Le comportement de `terraform plan` lors de l'ajout du rÃ©seau et du volume au conteneur existant a montrÃ©

  une recrÃ©ation complÃ¨te (`-/+`) plutÃ´t qu'une simple modification, Ã  cause de la limitation de Docker sur

  les attributs modifiables Ã  chaud -- comportement normal et documentÃ© dans le TP.

- La capture d'Ã©cran de `terraform destroy` n'a pas pu Ãªtre rÃ©cupÃ©rÃ©e correctement (fichier introuvable

  aprÃ¨s plusieurs tentatives) ; la sortie complÃ¨te de la commande a Ã©tÃ© incluse en texte dans le RENDU Ã  la

  place.


