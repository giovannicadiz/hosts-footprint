# hosts-footprint
Map Hosts on Network; Create Footprint; Login and query inside Hosts; Graph all Infos on Dashboard ;-)


### docker variables for hostfootprint

|              | value                                  | description                      |
|--------------|:--------------------------------------:|:---------------------------------|
| COUNTRIES    | US BR CL                               |  countries where there are sites |
| ENGINE       | django.db.backends.postgresql	        |  django db engine                |
| DBNAME       | database                               |  database name                   |
| DBUSER       | user                                   |  database user                   |
| DBPASSWORD   | password                               |  database password               |
| DBHOST       | db_hostname                            |  database host                   |
| DBPORT       | 5432                                   |  database port                   |

### docker variables for kali

|                | value                                  | description                      |
|----------------|:--------------------------------------:|:---------------------------------|
| COUNTRY        | Brazil                                 | kali country                     |
| DOMAIN         | BLACKTOURMALINE.CORP                   | corporation domain               |
| MAPUSER        | _sysmap%pass                           | system user                      |
| ELASTICSEARCH  | es.blacktourmaline.corp                | elasticsearch server             |

developer workstation

```
docker run --name btkali -e COUNTRY='Brazil' -e DOMAIN='blacktourmaline.corp' -e MAPUSER='_sysmap%pass' -e ELASTICSEARCH='es.blacktourmaline.corp' --rm -d blacktourmaline/kali:tag ping localhost
docker exec -ti btkali /bin/bash
```
