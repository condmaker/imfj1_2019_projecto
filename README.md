# Introdução à Matemática e Física Para Videojogos I - Relatório do Projeto Final

Feito por [Marco Domingos][md], a21901309 e [Daniel Fernandes][df], a21902752.

Este relatório irá relatar o trabalho feito para este projeto, e a contribuição indivídual de cada um dos participantes.

---

## *Features* feitas

O repositório contém as seguintes funções relatadas no enunciado:
* Aplicação *"Viewer"* (3dviewer.py)
  
  Feita por Marco Domingos.

  Todas as funções de rotação de câmera e de objecto estão a funcionar.
  O novo modelo feito nesta aplicação é um *Tetraedro.*. Não utiliza ficheiros *JSON* para a sua construção-- é feito totalmente em código (o próximo ficheiro utiliza isto, porém).

* Aplicação *FPS (First Person)* (fps.py)
  
  Feita por Marco Domingos e Daniel Fernandes. 

  - Ambiênte e movimentação da câmara pelo rato
  
    Feita por Daniel Fernandes.

    A movimentação da câmara pelo rato, e a movimentação do jogador (ou da posição da câmara em relação ao eixo), foram ambas feitas por Daniel Fernandes. É dada uma opção de sensibilidade do rato no inicio do ficheiro, e controla normalmente como um jogo *First-Person*, com a única diferença sendo que é possível virar a câmara em todas as direções, sem limites.

  - Verificação e desrenderização de objetos atrás da câmara
  
    Feito por Marco Domingos.

    Funciona por utilização da normal da câmara e o produto interno de um vetor que sempre segue a posição da câmara, fazendo com que se o "plano" da câmara fique "de costas" ao objeto, este não será renderizado, retirando-o da fronteira de objectos. 

  - Geometria cheia e reposição do *wireframe*
  
    Feita por Daniel Fernandes.

    Funciona por apanhar a largura das linhas e utilizar o número default *0*, que enche as formas geométricas. Enquanto isto funciona, as formas ainda podem sobrepor-se umas as outras.

  - Utilização de ficheiros JSON
  
    Feita por Daniel Fernandes e Marco Domingos.

    São utilizados ficheiros JSON para definição dos pontos dum objecto e o conjunto de pontos que formam as respetivas faces de cada polígono. A construção do programa e do objecto "cube" foram feitas por Daniel Fernandes, e a construção do objecto "pyramid foi feita por Marco Domingos.   

## *Postmortem*

  O trabalho feito neste projecto foi tumultuoso-- Porém conseguimos implementar a maioria das *features* pedidas. A parte da aplicação de visualização foi feita facilmente, porém a construção da segunda parte do trabalho foi complicada, com a movimentação da câmara com o rato a dar problemas de movimentação de eixo, onde a câmara movimentava-se em torno do eixo z, porém esta foi retificada por Daniel Fernandes. 
  
  Um outro problema, este mais for falta de atenção, foi a implementação da desrenderização do objecto quando este está atrás da câmara. Foi tentado retirar o objecto da cena quando este estava fora do alcance da câmara em sí-- não apenas quando este estava atrás, que levou a uma tentativa de implementação de matrizes PRS para rotação da normal de objectos, mas após a realização de que isto era desnecessário, o método original de criar um vetor que aponta sempre para a posição da câmara foi utilizado novamente. A implementação de geometria foi relativamente fácil.

  A aplicação de *backface culling* foi tentada, como é possível ver no branch *fps_marco*, mas no final não havia tempo para ser aplicada, visto que ainda estava com vários *bugs* e erros (muito provavelmente nas equações) que impediam-a de funcionar corretamente.


[md]:https://github.com/condmaker
[df]:https://github.com/dtfernandes
