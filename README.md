# ssl_defender_viewer 


## Utilisation 
Afin de pouvoir utiliser notre application vous devez rendre le main.py exécutable, s'il ne l'est pas déjà utiliser la commande " chmod +X main.py" dans le terminal à l'endroit où se trouve le fichier pour palier à ce problème.

### Pour générer une solution simple taper : 
  - ```./main.py 2 <probleme_file.json> <solution_file.json> -<algo>```
### Pour générer une solution avec un goal taper : 
  - ```./main.py 3 <probleme_file.json> <solution_file.json> -<algo>```
  
Actuellement pour le choix de l'alogorithme il y a deux possibilités:
  - l'algorithme exact : -e,
  - l'algorithme glouton : -g. 

# Pour exécuter le programme taper : 
  - ```./main.py 1 <probleme_file.json>  <solution_file.json>```
