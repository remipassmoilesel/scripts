# Utiliser un proxy HTTP d'entreprise

## Remarques diverses

Pour éviter un prompt inutile de mot de passe, utiliser une commande utilisant le proxy avec les identifiants:

	$ curl -v --proxy-basic \
	        --proxy-user GSB427:Heybobhowareyou123 http://wikipedia.fr \
	        --proxy http://proxy-g2s.intra.groupama.fr:8080/
   

## Pour APT

    $ sudo vim /etc/apt/apt.conf.d/40proxy
    
    Acquire::http::Proxy "http://$USER:$PASSWORD@proxy.intra.fr:8090/";
    Acquire::https::Proxy "http://$USER:$PASSWORD@proxy.intra.fr:8090/";
  
    
## Global au système (hors exceptions)

    $ sudo vim /etc/environment
    
    http_proxy=http://$USER:$PASSWORD@proxy.intra.fr:8090/
    https_proxy=http://$USER:$PASSWORD@proxy.intra.fr:8090/
    ftp_proxy=http://$USER:$PASSWORD@proxy.intra.fr:8090/
    no_proxy=localhost,127.0.0.1,*intra.fr
    

## Docker 
    
Coté client:    
    
    $ vim ~/.docker/config.json
    
    {
      "proxies": {
        "default": {
          "httpProxy": "http://$USER:$PASSWORD@proxy.intra.fr:8090/",
          "httpsProxy": "http://$USER:$PASSWORD@proxy.intra.fr:8090/"
        }
      }
    }
    

Coté serveur:

    $ sudo mkdir -p /etc/systemd/system/docker.service.d
    $ sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
    
    [Service]
    Environment="HTTP_PROXY=http://$USER:$PASSWORD@proxy.intra.fr:8090/" "NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
    
    $ sudo systemctl daemon-reload
    $ sudo systemctl restart docker
    $ systemctl show --property=Environment docker
    

## SSH

Se connecter via un proxy HTTP:

    $ ssh -v destination -o "ProxyCommand=nc -X connect -x proxy.domain.fr:8090 %h %p"
    
    
Pour Git (dépôt spécifique ou configuration spéciale par SSH):

    $ vim ~/.ssh/config
    
    Host domain.proxy
    	Hostname XX.XX.XX.XX
    	Port 443
    	IdentityFile ~/.ssh/id_rsa
    	IdentitiesOnly yes
        ProxyCommand nc -X connect -x proxy.intra.fr:8080 %h %p


Configuration exemple pour Github:
    
    Host github.proxy
        Hostname github.com
        User git
        IdentityFile ~/.ssh/github.com/id_rsa
        IdentitiesOnly yes
        ProxyCommand nc -X connect -x proxy.intra.fr:8080 %h %p
    

Exemple d'origine github:
    
    $ git remote add origin ssh://github.proxy:/remipassmoilesel/linux-utils.git 
    

## Git

Configuration globale:

    $ git config --global http.proxy http://proxyUsername:proxyPassword@proxy.server.com:port
    
Voir: https://gist.github.com/evantoli/f8c23a37eb3558ab8765    


## Intellij

CTRL MAJ A > Http proxy


## Maven

	$ vim ~/.m2/settings.xml

	<settings>
	  .
	  .
	  <proxies>
	   <proxy>
	      <id>example-proxy</id>
	      <active>true</active>
	      <protocol>http</protocol>
	      <host>proxy.example.com</host>
	      <port>8080</port>
	      <username>proxyuser</username>
	      <password>somepassword</password>
	      <nonProxyHosts>www.google.com|*.example.com</nonProxyHosts>
	    </proxy>
	  </proxies>
	  .
	  .
	</settings>

