# syntax=docker/dockerfile:1

# build 阶段负责把原始文本转换成 Nginx 最终要提供的网页文件。
FROM alpine:3.23 AS build
WORKDIR /src
COPY message.txt .
RUN mkdir -p /out \
    && tr '[:lower:]' '[:upper:]' < message.txt > /out/index.html

# 最终阶段只接收构建产物，不携带前一阶段的转换工具和中间文件。
FROM nginx:1.31.6-alpine
COPY --from=build /out/index.html /usr/share/nginx/html/index.html
EXPOSE 80
