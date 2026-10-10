# ngrok URLs et points de contact

Ce fichier liste temporairement les URLs ngrok et endpoints locaux que vous avez utilisées pour le développement. Ne stockez jamais de secrets (authtokens) dans le dépôt.

URLs fournies :

- URL publique ngrok : https://spoof-upright-backyard.ngrok-free.dev

Endpoints locaux :

- Dashboard ngrok local : http://127.0.0.1:4040
- Backend local : http://localhost:8000/
- Health (suggestion) : http://localhost:8000/health

Notes :

- L'URL publique ngrok change à chaque redémarrage si vous utilisez le plan gratuit. Pour un domaine fixe, souscrire au plan payant ngrok et réserver un sous-domaine.
- N'ajoutez pas votre `ngrok.yml` ou tokens au dépôt. Si vous avez besoin d'authtoken, configurez-le localement via `ngrok config add-authtoken <TOKEN>`.
- Après utilisation, vous pouvez supprimer ce fichier si vous préférez ne pas garder d'URL publiques dans le repo.

Historique :

- 2026-10-03 : ajouté par l'outil d'aide, URL active et renvoyant HTTP 200.

Notes d'utilisation :

- Pour démarrer rapidement le serveur et ngrok : `./scripts/start-dev.sh` depuis la racine du projet.
- Vérifier le health via : `curl -i http://localhost:8000/health` ou `curl -i https://<PUBLIC_NGROK>/health`.
