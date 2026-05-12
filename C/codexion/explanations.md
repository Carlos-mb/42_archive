
El subject exige que los mensajes no se mezclen entre sí.
Esto puede pasar porque hay hilos ejecutándose en paralelo y, si dos de ellos intentan escribir en el log (pantalla) sus mensajes se mezclaran. Hay que bloquear el log con un mutex para que no suceda.
