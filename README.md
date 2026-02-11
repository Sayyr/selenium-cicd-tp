## 1. Avantages observés :
- Quels sont les avantages de l'automatisation des tests que vous avez constatés ?
c'est une routine pour savoir qu'est ce qui ne fonctionne pas et avant de push sur main, donc en prod
c'est utile de fou pour faire des test cases généraux

- Comment le CI/CD améliore-t-il la qualité du code ?
il donne des règles de ce qui est accepté ou non, évitant ainsi les erreurs d'inatention en plus
d'être facilement modulable et extensible (ajouter d'autres navigateurs au test cases)


2. Défis rencontrés :
- Quelles difficultés avez-vous rencontrées avec Selenium ?

les imports sont capricieux, parfois on a des erreurs sur des trucs un peu stupide et du code qui semble
avoir un délai de vérification
Voici quelques liens vers les différents problèmes que j'ai eu : 

- https://stackoverflow.com/questions/62515478/selenium-python-is-there-some-way-to-send-out-an-e-mail-or-sms-if-a-certain-eve

- https://stackoverflow.com/questions/42204897/how-to-set-up-a-selenium-python-environment-for-firefox


- Comment pourriez-vous améliorer la stabilité des tests ?
faire des tests plus généraux pour attendre un résultat plus qu'une méthode


3. Métriques :
- Quelles métriques sont les plus importantes pour votre projet ?
Le temps mis dessus et la fiabilité des résultats.

- Comment mesurer l'efficacité de votre pipeline CI/CD ?
le temps gagné en fonction de ta taille du groupe de dév qui sont sur le projet
la pipeline devrait empêcher le plus de fictions possible entre les différents membres d'un groupe
de dev pour ainsi faire en sorte de produire du code de meilleur qualité et plus vite.