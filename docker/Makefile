.PHONY: run stop restart mcp stop-mcp agent stop-agent dev stop-dev

dev:
	echo "Running stack dev ..."
	docker-compose -p kgrag-agent --profile dev up -d

stop-dev:
	echo "Stopping stack dev ..."
	docker-compose -p kgrag-agent --profile dev down

mcp:
	echo "Running stack mcp ..."
	docker-compose -p kgrag-agent --profile mcp up -d

stop-mcp:
	echo "Stopping stack mcp ..."
	docker-compose -p kgrag-agent --profile mcp down

agent:
	echo "Running stack agent ..."
	docker-compose -p kgrag-agent --profile agent up -d

stop-agent:
	echo "Stopping stack agent ..."
	docker-compose -p kgrag-agent --profile agent down

run:
	echo "Running stack agent ..."
	docker-compose -p kgrag-agent --profile all up -d

stop:
	echo "Stopping qdrant ..."
	docker-compose -p kgrag-agent --profile all down

restart: stop run
	echo "All services are restarted"