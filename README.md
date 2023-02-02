# UD_Esperanto-ETB


Esperanto-korpuso en CONLL-U formato kaj kelkaj iloj por redakti kaj krei gxin.

Deveno de datumo:
1) Tekstaro de Esperanto (precize, Fundamentaj Ekzercaro kaj Krestomatio) https://tekstaro.com
2) Tekstoj de Complete Grammar of Esperanto, Ivy Kellerman Reed https://www.gutenberg.org/ebooks/7787

Instrukcioj pri formato kaj rekomendajxoj pri markumado: https://universaldependencies.org/  
Guidlines for Universal Dependencies ankaux estas en https://github.com/Arbaletos/UD_guidelines

## Celo
La celo estas fari tekstaron de Esperanto en UD (Universal Dependencies) por efektivigi la uzadon de Esperanto en interlingvaj esploroj uzante UD, kaj, tialmaniere, disvastigi Esperanton.  
  
## Taskoj 
1) Disigilo -- Ekzistas en regul-bazita versio (`tools/disigilo.py`), kaj en UD-Pipe modelo `models/ud_pipe_1_ab_0.1.2.pt` 
2) Morfologia analizilo -- Ekzistas en du versioj: regul-bazita (`tools/morf.py`), kaj statistika (`models/ud_pipe_1_ab_0.1.2.pt`)
3) Sintaksa analizilo -- Ekzistas nur en formo de UDP modelo (`models/ud_pipe_1_ab_0.1.2.pt`)
4) Morfema analizilo -- Por nun ne necesas, malestas.  
5) CONLL redaktilo -- Estas en baza formo por python kun npyscreen.  

Por uzi disigilon, morfologianalizilon kaj sintaksanalizilon de UDP, necesas instali gxin: `https://ufal.mff.cuni.cz/udpipe/1/install`.  
Cxi modelo (`models/ud_pipe_1_ab_0.1.2.pt`) estis trajnita bazite sur Arbobanko -- http://catalog.elra.info/en-us/repository/browse/ELRA-W0129/ -- sed funkcias ne tre bone, pro diversajxoj inter UD sistemo, kaj CG3 sistemo en Arbobanko. Pro tio, cxi modelo estas uzata per mi nur por unua, "kruda" markumado de teksto, post kiu sekvas mana markumado.  
Instrukcio por uzi UDP: `https://ufal.mff.cuni.cz/udpipe/1/users-manual#run_udpipe`  
Morfanalizilo de UDP modelo produktas nur UPOS (kaj kelkaj FEATS), sen XPOS. Mia analizilo (tools/morf.py) produktas ankaux XPOS, sed ilia aro estas ankoraux pripensata
 kaj povas sxangxigxi.    
 
## Nuna stato
Fundamenta ekzercaro: mankontrolitaj morfologiaj markoj (UPOS, XPOS), sed sen multaj "FEATS" variajxoj.  
Mankontrolado de DEPREL markoj en fundamenta ekzercaro estas en progreso.  


Por detala informo pri iloj, specialaj markoj kaj datumo legu na wiki.  
