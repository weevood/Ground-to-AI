# Ground-to-AI

###### Architecture to collect sensors data from ground and using it to train and develop artificial intelligence models.

## Goal

![Ground-to-AI goal](images/goal.png)

The aim of "Ground-to-AI" is to offer a simple and low-cost architecture that offer the way of collecting data in the field, transferring and transforming this data via a pipeline and analysing it using a Machine Learning model.

### Architecture

![Architecture technologies](images/technologies.png)

### Technologies

- [DHT11 Temperature-Humidity Sensor](https://www.waveshare.com/temperature-humidity-sensor.htm)
- [PiXtend V2 Controller](https://www.pixtend.de/pixtend-v2/hardware-v2/pixtend-v2-l-controller/)
- [Raspberry Pi](https://www.raspberrypi.org/)
- [MariaDB](https://mariadb.com/)
- [InfluxDB OSS](https://www.influxdata.com/) & [InfluxDB Cloud](https://www.influxdata.com/products/influxdb-cloud/)
- [Grafana](https://grafana.com/)
- [Teltonika RUT240](https://teltonika-networks.com/de/products/routers/rut240)
- [Google Looker Studio](https://lookerstudio.google.com/u/0/)
- [Docker](https://docker.com/) & [Docker Hub](https://hub.docker.com/)
- [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Python](https://docs.python.org/) & [Darts](https://unit8co.github.io/darts/index.html)

## Scripts

Les scripts sont organisés en trois catégories et rangés dans les dossiers correspondants.

1. [Raspberry Pi](Raspberry%20Pi) : tous les scripts exécutés sur les 4 Raspberry Pi permettant de gérer les interactions avec les éléments physiques de la station de gonflage.
2. [Configurations](Configurations) : les fichiers de configuration nécessaires aux différents services.
3. [Azure](Azure) : tous les scripts nécessaires au déploiement de la Azure function permettant d'exécuter la maintenance prédictive.

### Azure

Les deux fichiers les plus intéréssants sont les fichiers :

- [requirements.txt](Azure/requirements.txt) qui permet de gérer les dépendances des bibliothèques, modules et paquets indispensables.
- [\_\_init\_\_.py](Azure/HttpTriggerFrisub/__init__.py) qui stocke le code de la fonction exécuté lors d'un appel via le service Azure. C'est dans ce fichier que le modèle de ML est défini et que les prédictions de maintenance sont calculées.

### Configurations

- [Grafana-PiXtend-Alert.yaml](Configurations/Grafana-PiXtend-Alert.yaml) : Export *YAML* de l'alerte de pression basse dans les bouteilles tampons Nitrox réalisé avec *Grafana*. Cet export est importable tel quel lors d'une nouvelle configuration.
- [Grafana-PiXtend-Dashboard.json](Configurations/Grafana-PiXtend-Dashboard.json) : Export *JSON* du tableau de bord réalisé avec *Grafana*. Cet export est importable tel quel lors d'une nouvelle configuration.
- [downsample_climates_to_influxdb_cloud.json](Configurations/downsample_climates_to_influxdb_cloud.json) : Export de la tâche au format *JSON* de réplication et du sous-échantillonnage du bucket « *sensors* » entre la base de données *Influx* local et cloud.
- [downsample_pressures_to_influxdb_cloud.json](Configurations/downsample_pressures_to_influxdb_cloud.json) : Export de la tâche au format *JSON* de réplication et du sous-échantillonnage du bucket « *pressures* » entre la base de données *Influx* local et cloud.
- [frisub.sql](Configurations/frisub.sql) : Script *SQL* de définition de la base de données relationnelle.
- [kiosk.sh](Configurations/kiosk.sh) : Fichier de configuration executé au démarrage d'un Raspberry devait fonctionneé en mode « *kiosk* », actuelement utilisé sur le Raspberry « *PiMaster* » pour afficher le tabelau de bord *Grafana* de manière permanente.
- [telegraf.conf](Configurations/telegraf.conf) : Fichier de configuration du service « *Telegraf* » permettant de récolter les données de manière périodique. Il indique notamment les accès à la base de données *Influx* et le *bucket* à utiliser.

### Raspberry Pi

- Dossier [libraries](Raspberry%20Pi/libraries) : contient les libraries nécessaires à la lecture des tag *RFID* et à la commande des relais.
- Dossier [models](Raspberry%20Pi/models) : contient les modèles de la base de données relationnel ainsi que des méthodes d’abstractions permettant de réaliser les actions CRUD nécessaires pour chaque table sur la base de données.
- Dossier [utils](Raspberry%20Pi/utils) : contient des fonctions nécessaire au bon fonctionnement des scripts principaux. Ils permettent notamment d’établir une connexion avec la base de données *MySQL*, de commander des relais, etc.
- Fichier [door.py](Raspberry%20Pi/door.py) : exécuté en permanence sur le Raspberry « *PiDoor* ». Il permet de vérifier les accès, de déclencher l’ouverture de la porte d’entrée et de loguer les évènements liés. Son exécution est lancée dès le démarrage du Raspberry par un système de contrôle.
- Fichier [event.py](Raspberry%20Pi/event.py) : exécuté en permanence sur le Raspberry « *PiMaster* ». Il permet de vérifier si un nouvel événement a eu lieu sur l’installation. Dans ce cas, il est capable de déclencher un appel à une fonction *Azure* permettant de réaliser des calculs de maintenance prédictive. Ce script pourrait s’exécuter sur n’importe quel système Linux et n’est pas fortement lié au Raspberry « *PiMaster* ».
- Fichier [inflate.py](Raspberry%20Pi/inflate.py) : exécuté en permanence sur le Raspberry « *PiNflate* ». Il permet de vérifier les possibilités de gonflage de l’utilisateur, de déclencher l’ouverture des solénoïdes et de loguer les évènements liés. Son exécution est lancée dès le démarrage du Raspberry par un script de démarrage du superutilisateur configuré via le fichier « /etc/rc.local ».
- Fichier [pixtend.py](Raspberry%20Pi/pixtend.py) : exécuté en permanence sur le Raspberry « *PiXtend* ». Il permet de contrôler le tableau de commandes et les différents automates nécessaires à la gestion des compresseurs ainsi que de de loguer les évènements liés. Son exécution est lancée dès le démarrage du Raspberry par un script de démarrage du superutilisateur configuré via le fichier « /etc/rc.local ».
- Fichier [add_tag.py](Raspberry%20Pi/add_tag.py) : ce fichier nécéssite une execution manuelle sur le Raspberry « *PiMaster* ». Il permet d'ajouter simplement un tag RFID dans la base de données.