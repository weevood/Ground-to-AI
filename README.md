<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="160" height="160">
  </a>

  <h3 align="center"> Ground-to-AI </h3>

  <p align="center">
    ***Architecture to collect sensors data from ground and using it to train and develop artificial intelligence models.***
    
    NOTE: This documentation is still being drafted
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<div align="center">
    <img src="images/goal.png" alt="Logo">
</div>

The aim of "Ground-to-AI" is to offer a simple and low-cost architecture that offer the way of collecting data in the field, transferring and transforming this data via a pipeline and analysing it using a Machine Learning model.


### Architecture

<div align="center">
    <img src="images/technologies.png" alt="technologies">
</div>


#### Built With

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



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```



<!-- USAGE EXAMPLES -->
## Usage

<div align="center">
    <img src="images/dth11.jpeg" alt="Sensor" width=20%>
    <img src="images/grafana.png" alt="Grafana" width=80%>
</div>

For example, you can use this framework to collect data from a temperature sensor and display it in Grafana. Afterwards, the results of a model's predictions can then be obtained via a simple Telegram notification.

*Refer to the scripts below for more details.*

### Scripts

Scripts are organised into three categories and stored in the corresponding folders.

1. [Raspberry Pi](Raspberry%20Pi) : all the scripts run on the Raspberry Pi to manage interactions with physical elements.
2. [Configurations](Configurations) : the configuration files required for the various services.
3. [Azure](Azure) : all the scripts needed to deploy the Azure function enabling predictive maintenance to be carried out.

#### Raspberry Pi

- File [pixtend.py](Raspberry%20Pi/pixtend.py) : permanently executed on the « *PiXtend* » Raspberry. It is used to manage the control panel and the various PLCs needed to run the compressors, as well as logging related events. It is launched as soon as the Raspberry is booted by a superuser startup script configured via the « /etc/rc.local » file.
- File [event.py](Raspberry%20Pi/event.py) : permanently executed on the Master Raspberry Pi. It is used to check whether a new event has occurred on the installation. In this case, it is capable of triggering a call to an *Azure* function for predictive maintenance calculations.
- Dossier [utils](Raspberry%20Pi/utils) : contains the functions needed for the main scripts to work properly. In particular, they can be used to establish a connection with the *MySQL* database, order relays, etc.

#### Configurations

- [downsample_climates_to_influxdb_cloud.json](Configurations/downsample_climates_to_influxdb_cloud.json) : Export of the replication task in *JSON* format and of the subsampling of the "*sensors*" bucket between the local *Influx* database and the *Influx Cloud* one.

#### Azure

- [requirements.txt](Azure/requirements.txt) which manages the dependencies of essential libraries, modules and packages.
- [Dockerfile](Azure/Dockerfile) document texte qui contient tous les appels nécessaires à l'assemblage de l'image de construction.
- [\_\_init\_\_.py](Azure/HttpTrigger/__init__.py) which stores the function code executed during a call via the Azure service. It is in this File that the ML model is defined and maintenance predictions are calculated.



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

- [@weevood](https://github.com/weevood)
- Project Link: [https://github.com/weevood/Ground-to-AI](https://github.com/weevood/Ground-to-AI)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
