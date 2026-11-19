# Onde a fase engana o olho

Conferido em 18/11 e 19/11 com o mesmo peso que alimenta a regra, `yolo26n.pt`, limiar 0,25. Isto não é a comparação de 60% contra um operador.

| Cena | O que a tela faz | Por quê |
| --- | --- | --- |
| trânsito | `PEDESTRE` nos 84 s | o polígono pega a faixa de trás, e um pé lá segura a fase |
| esquina | `PEDESTRE` nos 55 s | os vãos sem gente somam cerca de 2,6 s e não vencem os 5 s |
| faixa | `PEDESTRE` nos 56 s | a zebra não esvazia o bastante, e não há uma segunda via |
| espera | `ABRE VIA` nos 21 s | nenhum pé entra na pintura; a calçada cheia derruba a taxa para 14,0 |
| Londres | segura `PEDESTRE` com a faixa já em 0 | são os 5 s de verde mínimo, antes da troca |

Uma calçada desenhada por cima da pintura conta quem espera como se estivesse atravessando. Um polígono largo demais faz o mesmo com a faixa de trás. Os dois casos deixam o letreiro em `PEDESTRE` com a zebra da frente vazia. A correção é o polígono, não a regra dos 5 segundos.
