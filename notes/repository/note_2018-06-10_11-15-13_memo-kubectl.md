# Mémo Kubectl

## Commandes générales

    $ kubectl apply deploymentname
    $ kubectl apply -f https://...
    $ kubectl apply -f path/to/local

    $ kubectl proxy
    $ xdg-open http://127.0.0.1:8001/ui	     
    
    $ kubectl get pods
    $ kubectl get pod podname     
    $ kubectl logs -f podname     

    $ kubectl exec -ti podname ash
    $ kubectl port-forward -n $namespace $pod_name_or_service $host_port:$target_port 
    
    $ kubectl get jobs     
    $ kubectl get secrets     
    $ kubectl get configmaps     

    $ kubectl config view
    $ kubectl config get-contexts
    $ kubectl config use-context context-name

## Pods

Afficher les pods:

	$ kubectl get pods

Obtenir un shell:

	$ kubectl exec -ti podname bash

Inspecter un pod:

	$ kubectl get pods podname -o json 

Obtenir les logs d'un pod:

	$ kubectl logs podname  

## Deployments

Scaler un deployment

    $ kubectl scale deployment --replicas 3 kubernetes-dashboard -n kube-system     

## Services

Afficher et décrire un service:

    $ kubectl get services
    $ kubectl describe service servicename

Créer un service:

    $ kubectl expose 

Afficher un déploiement:

    $ kubectl describe deployment kubernetes-dashboard -n kube-system

## Configuration

Afficher la configuration courante:
 
    $ kubectl config view
            
## Proxy et port forward

### Proxy 

Créer un proxy vers l'API Kubernetes:

    $ kubectl proxy --port=8080 &    
    
    $ curl http://localhost:8080/api/
    {
      "versions": [
        "v1"
      ]
    }
 
On peut utiliser ensuite le dashboard à l'addresse: http://127.0.0.1:8001/ui/

### Forward

Forward de port vers un pod:

    # /!\ Très sensible au namespace

    $ kubectl port-forward -n $namespace $pod_name_or_service $host_port:$target_port 
    $ kubectl port-forward -n spring-k8s-demo gateway-release1-spring-k8s-demo-5ccb7d9f5d-cqg77 8080:8080 


