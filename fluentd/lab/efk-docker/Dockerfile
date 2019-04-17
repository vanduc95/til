FROM fluent/fluentd:v1.2

RUN apk add --update --virtual .build-deps \
    build-base ruby-dev \
 && gem install \
       fluent-plugin-elasticsearch \
       fluent-plugin-rewrite-tag-filter \
 && gem sources --clear-all \
 && apk del .build-deps \
 && rm -rf /var/cache/apk/* \
           /home/fluent/.gem/ruby/2.4.0/cache/*.gem