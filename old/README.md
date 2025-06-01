Para coletar os dados de treinamento e prepará-los para a IA, seguimos um fluxo de processo bem estruturado, dividido em três etapas principais:

Geramos 200 imagens de rostos humanos inexistentes utilizando o site thispersondoesnotexist.com, garantindo assim uma base diversificada e isenta de questões de direitos autorais.

Em seguida, dividimos cada imagem em duas partes distintas – watermarkTop e watermarkBottom – para identificar separadamente as regiões onde as marcas d’água estão presentes.

Por fim, realizamos cortes precisos para remover completamente as marcas d’água das imagens, assegurando que os dados de treinamento não contenham elementos que possam induzir vieses ou interferir no aprendizado da IA.

Todo o tratamento foi implementado em Python, com códigos otimizados para performance e organização, e os scripts estão disponíveis no repositório.
