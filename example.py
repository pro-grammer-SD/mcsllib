import mcsl

server = mcsl.ServerEntity(wm=True)

# suggest papermc
server.launch(loader_type="papermc", gui=True, min_mem=512, max_mem=2048, online=True, lgui=True)