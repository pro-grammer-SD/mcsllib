import mcsl

server = mcsl.ServerEntity()
server.launch(loader_type="fabric", gui=True, min_mem=512, max_mem=2048)
