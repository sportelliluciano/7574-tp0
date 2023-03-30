StorageServer -> Guarda estado compartido (ganadores y agencias abiertas)
BetServer -> Maneja las apuestas (guardar a disco, calcular ganadores, etc)
ClientWorker -> Maneja la conexión con un cliente


ClientWorker -- envia requests --> BetServer
     |--- intercambia información con --> StorageServer

Guardar al storage: push to queue
Leer de storage: 