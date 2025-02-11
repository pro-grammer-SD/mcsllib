import mcsl

server = mcsl.ServerEntity()
# suggest papermc
server.launch(loader_type="papermc", gui=True, min_mem=512, max_mem=2048)
