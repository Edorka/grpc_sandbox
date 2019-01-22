GOPATH := ${GOPATH}

GATEWAY_FLAGS := -I. -I/usr/local/include -I$(GOPATH)/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis -I/usr/local/include -I./proto/

GRPC_FLAGS := --python_out=. --grpc_python_out=.

code:
	python -m grpc_tools.protoc $(GRPC_FLAGS) $(GATEWAY_FLAGS) ./proto/*.proto

gw:
	echo ${GOPATH}
	protoc $(GATEWAY_FLAGS) \
        --go_out=Mgoogle/api/annotations.proto=github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis/google/api,plugins=grpc:. \
		--plugin=protoc-gen-grpc-gateway=$(GOPATH)/bin/protoc-gen-grpc-gateway \
        --grpc-gateway_out=logtostderr=true:. \
        proto/poi.proto

api:
	protoc $(GATEWAY_FLAGS) \
		--plugin=protoc-gen-swagger=$(GOPATH)/bin/protoc-gen-swagger \
		--swagger_out=logtostderr=true:. \
        proto/poi.proto


deps:
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
	go get -u github.com/golang/protobuf/protoc-gen-go


resources:
	wget http://bulk.openweathermap.org/sample/hourly_16.json.gz
